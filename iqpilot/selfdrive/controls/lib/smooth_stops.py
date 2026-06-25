"""
Copyright © IQ.Lvbs, apart of Project Teal Lvbs, All Rights Reserved, licensed under https://konn3kt.com/tos

Original concept and implementation by SpysyWeeb (github.com/SpysyWeeb)

Enabled together with Force Stops (IQForceStops): the landing law runs on every
stop, so a forced stop at a sign or light also lands smoothly.
"""
from opendbc.car.interfaces import ACCEL_MIN
from openpilot.common.params import Params
from openpilot.common.realtime import DT_CTRL, DT_MDL
from openpilot.iqpilot import PARAMS_UPDATE_PERIOD

ACTIVATION_SPEED = 3.5   # m/s, cap is computed below this; near no-op at the top end
STOP_INTENT_SPEED = 0.5  # m/s, plan must reach below this to count as a stop
MIN_LEAD_DISTANCE = 5.0  # m, full braking authority when a lead is closer than this
LEAD_STOP_MARGIN = 4.0   # m, never block the braking required to stop this far behind the lead

SMOOTHNESS_K = 0.70  # [1/s], landing time constant
SMOOTHNESS_C = 0.30  # [m/s^2], residual decel at standstill

LINGER_SPEED = 0.5  # m/s (~1.1 mph), absolute backstop: arms clamp-to-stop as last resort
LINGER_TIME = 1.0   # s, how long to crawl before the clamp is allowed to finish the stop

# creep floor: below CREEP_FLOOR_SPEED, nudge a_target to at least -CREEP_FLOOR_DECEL.
# Prevents the car from coasting when the MPC is too gentle to overcome transmission
# creep torque — no sudden clamp, just guaranteed consistent deceleration.
CREEP_FLOOR_SPEED = 1.0   # m/s (~2.2 mph), below this enforce minimum commanded decel
CREEP_FLOOR_DECEL = 0.40  # m/s^2, minimum commanded decel at creep speeds

# progress watchdog: while the cap is limiting braking, the car must keep slowing.
# If speed stops decreasing, release the cap progressively until it does
STALL_TIME = 1.0           # s, no progress for this long starts releasing the cap
STALL_PROGRESS = 0.02      # m/s, minimum speed reduction to count as progress
STALL_RELEASE_RATE = 0.15  # m/s^2 of additional allowed braking per second of stall
SETTLE_SMOOTH_SPEED = 1.5  # m/s, jerk-limit the PID output below this
SETTLE_JERK_LIMIT = 2.5    # m/s^3


def read_smooth_stops_enabled(params: Params) -> bool:
  # Smooth landing is part of Force Stops now: one toggle (IQForceStops) both
  # forces a stop where it belongs and feathers every stop to a gentle landing.
  return params.get_bool("IQForceStops")


class SmoothStops:
  def __init__(self):
    self.params = Params()
    self.frame = 0
    self.enabled = False
    self.active = False
    self._v_min = float("inf")
    self._stall_frames = 0
    self.read_params()

  def _reset_watchdog(self) -> None:
    self._v_min = float("inf")
    self._stall_frames = 0

  def read_params(self) -> None:
    self.enabled = read_smooth_stops_enabled(self.params)

  def update(self) -> None:
    if self.frame % int(PARAMS_UPDATE_PERIOD / DT_MDL) == 0:
      self.read_params()
    self.frame += 1

  def apply(self, a_target: float, v_ego: float, lead_one, plan_min_v: float) -> float:
    self.active = False

    if not self.enabled or a_target >= 0. or v_ego > ACTIVATION_SPEED:
      self._reset_watchdog()
      return a_target
    if plan_min_v > STOP_INTENT_SPEED:
      self._reset_watchdog()
      return a_target

    brake_floor = -(SMOOTHNESS_K * v_ego + SMOOTHNESS_C)

    if lead_one.status:
      if lead_one.dRel < MIN_LEAD_DISTANCE:
        self._reset_watchdog()
        return a_target
      closing = max(v_ego - lead_one.vLead, 0.0)
      gap_budget = max(lead_one.dRel - LEAD_STOP_MARGIN, 0.5)
      required = (closing ** 2) / (2.0 * gap_budget)
      brake_floor = max(min(brake_floor, -required), ACCEL_MIN)

    if v_ego < self._v_min - STALL_PROGRESS:
      self._v_min = v_ego
      self._stall_frames = 0
    else:
      self._stall_frames += 1
    stalled_s = max(self._stall_frames * DT_MDL - STALL_TIME, 0.0)
    if stalled_s > 0.0:
      brake_floor = max(brake_floor - STALL_RELEASE_RATE * stalled_s, ACCEL_MIN)

    if a_target < brake_floor:
      self.active = True
      a_target = brake_floor

    if v_ego < CREEP_FLOOR_SPEED:
      creep_limit = -CREEP_FLOOR_DECEL
      if a_target > creep_limit:
        self.active = True
        a_target = creep_limit

    return a_target


class SmoothStopsLongControl:

  def __init__(self):
    self.params = Params()
    self.frame = 0
    self.enabled = False
    self.linger_frames = 0
    self.last_pid_output = 0.0

  def update(self) -> None:
    if self.frame % int(PARAMS_UPDATE_PERIOD / DT_CTRL) == 0:
      self.enabled = read_smooth_stops_enabled(self.params)
    self.frame += 1

  def defer_stopping(self, should_stop: bool, standstill: bool, v_ego: float) -> bool:
    if not self.enabled:
      self.linger_frames = 0
      return should_stop

    if not should_stop or standstill:
      self.linger_frames = 0
      return should_stop

    # if the light settle brake never closes the last bit to standstill, stop
    # deferring and let the clamp finish the stop — the car must never keep
    # rolling when it should be stopped
    if v_ego < LINGER_SPEED:
      self.linger_frames += 1
      if self.linger_frames >= int(LINGER_TIME / DT_CTRL):
        return True
    else:
      self.linger_frames = 0

    return False

  def smooth_pid_output(self, output_accel: float, v_ego: float) -> float:
    if not self.enabled or v_ego > SETTLE_SMOOTH_SPEED:
      self.last_pid_output = output_accel
      return output_accel

    step = SETTLE_JERK_LIMIT * DT_CTRL
    output_accel = min(max(output_accel, self.last_pid_output - step), self.last_pid_output + step)
    self.last_pid_output = output_accel
    return output_accel
