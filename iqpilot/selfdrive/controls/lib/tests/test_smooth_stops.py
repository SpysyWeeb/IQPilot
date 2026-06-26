"""
Copyright © IQ.Lvbs, apart of Project Teal Lvbs, All Rights Reserved, licensed under https://konn3kt.com/tos

Original concept and implementation by SpysyWeeb (github.com/SpysyWeeb)
"""
from types import SimpleNamespace

from openpilot.iqpilot.selfdrive.controls.lib.smooth_stops import (
  SmoothStops,
  ACTIVATION_SPEED,
  SMOOTHNESS_K,
  SMOOTHNESS_C,
  CREEP_FLOOR_DECEL,
  read_smooth_stops_enabled,
)


def _lead(status=False, dRel=100.0, vLead=0.0):
  return SimpleNamespace(status=status, dRel=dRel, vLead=vLead)


def _build(enabled=True):
  ss = SmoothStops.__new__(SmoothStops)
  ss.enabled = enabled
  ss.active = False
  ss._v_min = float("inf")
  ss._stall_frames = 0
  return ss


def test_unified_toggle_reads_force_stops():
  # Smooth landing is part of Force Stops now: it follows IQForceStops, not a
  # separate IQSmoothStops toggle.
  seen = {}

  class FakeParams:
    def get_bool(self, key):
      seen["key"] = key
      return True

  assert read_smooth_stops_enabled(FakeParams()) is True
  assert seen["key"] == "IQForceStops"


def test_softens_surplus_braking_on_no_lead_stop():
  ss = _build(enabled=True)
  v_ego = 2.0
  out = ss.apply(a_target=-3.0, v_ego=v_ego, lead_one=_lead(status=False), plan_min_v=0.0)
  # surplus braking is capped to the exponential landing law
  assert out == -(SMOOTHNESS_K * v_ego + SMOOTHNESS_C)
  assert ss.active


def test_creep_floor_guarantees_decel_near_standstill():
  ss = _build(enabled=True)
  out = ss.apply(a_target=-0.05, v_ego=0.5, lead_one=_lead(status=False), plan_min_v=0.0)
  # never coast against transmission creep torque in the final crawl
  assert out <= -CREEP_FLOOR_DECEL
  assert ss.active


def test_no_op_when_disabled():
  ss = _build(enabled=False)
  out = ss.apply(a_target=-3.0, v_ego=2.0, lead_one=_lead(status=False), plan_min_v=0.0)
  assert out == -3.0
  assert not ss.active


def test_no_op_above_activation_speed():
  ss = _build(enabled=True)
  out = ss.apply(a_target=-3.0, v_ego=ACTIVATION_SPEED + 1.0, lead_one=_lead(status=False), plan_min_v=0.0)
  assert out == -3.0


def test_no_op_when_plan_is_not_stopping():
  ss = _build(enabled=True)
  # plan bottoms out above the stop-intent speed: this is a slowdown, not a stop
  out = ss.apply(a_target=-3.0, v_ego=2.0, lead_one=_lead(status=False), plan_min_v=5.0)
  assert out == -3.0


def test_close_lead_keeps_full_braking_authority():
  ss = _build(enabled=True)
  out = ss.apply(a_target=-3.0, v_ego=2.0, lead_one=_lead(status=True, dRel=3.0, vLead=0.0), plan_min_v=0.0)
  # within MIN_LEAD_DISTANCE the cap turns transparent so the gap is never starved
  assert out == -3.0
