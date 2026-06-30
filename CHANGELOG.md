# IQ.Pilot User Changelog

This changelog is written for everyday drivers and focuses on what you will notice on the road.

## IQ.Pilot 1.0c


**Navigate on IQ.Pilot**

Navigate on IQ.Pilot is here. Search for a destination, pick from route alternatives, and let IQ.Pilot guide you turn by turn with live rerouting when you miss an exit. Along with on-screen-maps, you can see your position, the route, and upcoming turns all at once without leaving the driving view. Speed, turn, and highway exit handling are route-aware, so IQ.Pilot knows what's coming before you do. Mapbox is included at no cost to you for enhanced online map data and routing. On supported vehicles, Navigate on IQ.Pilot will command turn signals automatically based on the route. Map Curve speed control pulls limit data from OpenStreetMaps when offline and Mapbox when available.

When approaching a highway exit, IQ.Pilot now initiates the lane change toward the exit. If your car has Blind Spot Monitoring (BSM), it can perform the lane change fully automatically, there's no blinker nudge required. Without BSM, you confirm with a brief blinker push and IQ.Pilot takes it from there.

**Speed Limit Control (SLC)**

IQ.Pilot can now read and act on speed limits from your car's dash, Mapbox, TomTom, HERE, (included at no cost to our users!) and offline maps. You pick what mode you want in settings: display only, warn you when you're over, or actually adjust your cruise speed. You also pick which source wins when they disagree (dash, Mapbox, map data, highest, or lowest reported limit). There's a look ahead setting so IQ.Pilot can start reacting to an upcoming speed change before you hit the sign to decelerate to the limit before crossing into the new speed limit. 

SLC can now also raise your cruise speed automatically when the speed limit increases, not just lower it. Toggle "confirm higher speed limit" off to enable this, SLC will adjust up to a higher accepted limit with a small prompt, without any confirmation input needed.

**Camera Alerts (Speed Cameras, Red Light Cameras, and Surveillance / ALPR Cameras)**

IQ.Pilot now detects upcoming speed cameras, red light cameras, and ALPR/surveillance cameras (including Flock Safety cameras) sourced from OpenStreetMap's and alerts you before you reach them. Each camera type has its own toggle so you can pick what you want to be warned about. Speed cameras can also trigger a speed reduction to the limit when detected if enabled. Camera data is sourced from OSM and is updated periodically.

**IQ.Dynamic and Driving Behavior**

In IQ.Dynamic blended mode, when IQ.Pilot sees a stop light ahead, the model agrees you need to stop, and there's no lead car to track, it will now commit to stopping on its own — no lead car required. Gas pedal overrides it instantly. The stop prediction horizon is adjustable in IQ.Dynamic settings. Behavior for curves, low-speed driving, stopped leads, speed-limit fallbacks, and vision-based stops is now configurable. On-device IQ.Dynamic tuning is accessible by double-tapping IQ.Dynamic in longitudinal mode selection. An optional lane planner is available to reduce freeway ping-pong, tunable both on-device and in the Konn3kt app.

Force Stops now include "Smooth Stops" under the same toggle thank's to SpysyWeeb! With Force Stops on, all stops including model predicted stops at signs and lights now use the smooth landing law, so every stop settles gently rather than dropping in hard. The minimum force stop distance slider enforces minimum distance when configured.

IQ.Dynamic on supported Volkswagen platforms including MQB, and PQ now support blending OEM Stock Radar ACC with IQ.Dynamic to allow for a blended longitudinal experience while maintaining E2E IQ.Pilot functionality. 

**Driving Models**

IQ.Pilot updated to a new default driving model, `Pop!`

IQ.Pilot also has the latest bleeding-edge models, as always, including the latest TobyRL model, NoPP model, DeeperRL model, DeepRLv3/4/5 models, OP Model 16 Deep, and all future RL models as they are released.

IQ.Pilot maintains supports for all legacy models like `Notre Dame (v1/3)`, `FarmVille`, `WD40`, etc.

**Dashcam, Live View, and Alerts**

- WebSSH now connects in under 15 seconds and connects the first time, every time.
- Live View in the Konn3kt app now processes full-resolution HDR input from the Comma 4 driver camera for a noticeably sharper, and more accurate picture. Live View performance was optimized, and microphone audio (one way) streaming is now included.
- You can fully disable dashcam recording from the Konn3kt app. Turning it off stops all recording, no logs, no video, no audio, full stop.
- Audible alerts now ramp in volume smoothly instead of cutting in abruptly for enhanced auditory alerts. 
- WebRTC live streaming added. Stream your camera feed live through the Konn3kt app without routing through comma's servers. Onroad choppiness fixed — the stream now locks onto the correct feed and doesn't reset the decoder every frame. Keyframe-on-demand is also added for instant stream starts and camera switches.
- Konn3kt can now take a snapshot from any camera (road, driver, or wide) on-demand, both onroad and offroad, and returns it as a JPEG instantly.

**Volkswagen**

Volkswagen support got a significant overhaul this release:

- Lateral and longitudinal tuning greatly improved.
- Accelerator override behavior now matches stock feel.
- MQB standstill handling improved for supported non-EPB ACC FtS vehicles.
- IQ.Pilot now supports all VW PQ and MQB CC-only and CC-less cars, including CC-only PQ cars without ECAN.
- VW Passat B7 (TRW450) Stop-and-Go added.
- VW PQ TRW450 Stop-and-Go added.
- CAN-FD integration corrected.
- Model-year ECU fingerprint checks added.
- Konn3kt now checks EPS compatibility and reports LKAS coding status.
- Konn3kt can enable LKAS on supported VW MQB vehicles that didn't ship with factory LKAS — Comma Power must be plugged into the harness.
- Konn3kt toggles added for HCA5/HCA7 and ALC.
- Fully merged Volkswagen ALC into IQ.Pilot release.

**Volkswagen MEB and MQBevo**

IQ.Pilot now officially supports the Volkswagen MEB and MQBevo platforms — including the ID.4, ID.3, ID.5, Golf MK8, and Tiguan 2024+, up to model year 2026, as long as you have a compatible camera or gateway harness. Both LKAS and ACC are supported. This is the foundation of the `release-meb` branch, which is auto-synced from `release` and tailored specifically for these platforms.

**Toyota/Lexus**

New support added for Stop-and-Go and SDSU for Toyota/Lexus vehicles.

**Hyundai/Kia**

Fingerprint coverage expanded to cover more Hyundai/Kia variants that were previously unrecognized.

**UI — Comma 4 (mici)**

The Comma 4's offroad UI has been completely redesigned. The new home screen uses a big-tile launcher with a live status indicator (teal for OK, orange for warnings, red for faults). The settings hub is now a grid-of-pills layout with reorganized categories. A hold-to-customize panel on the right lets you pin Changelog, Stats, Map, or Daily Inspiration. Signal strength icons show Wi-Fi or cellular quality live. Settings have been reorganized across panels — Steering now includes Lane Turn Desires and Live Learning, Models is focused on model management only, and Visuals includes all display settings. This UI is being merged in before release.

**UI — Comma 3x and Comma 3 (tizi/tici)**

The tizi/tici (Comma 3x and Comma 3) onroad and offroad UI has been fully redesigned as well, matching the new IQ.Pilot design language with updated toggle styles, improved map live location tracking, Konn3kt icon, and general layout improvements. This UI is also being merged in before release.

**UI Improvements**

IQ.Pilot's on-road UI got a number of improvements:

- The AOL border now has a lower portion that distinguishes lateral-only engagement from full engagement.
- IQ Long Personality can now be cycled on-road by tapping the driver-monitoring icon on BIG UI devices. The icon color reflects the currently selected personality.
- Synced upstream Comma 4 UI optimizations, anti-aliasing, and augmented-road-view refinements. Augmented road view calibration now invalidates the matrix cache correctly when calibration changes mid-drive.
- Live Konn3kt accent-color sync: whatever color you pick in the Konn3kt app flows to your device UI within a couple of seconds.
- Branch switcher and updater reliability improved.
- The mici pairing flow now pairs directly with Konn3kt instead of comma connect.

**IQ.OS 3.14**

IQ.OS 3.14 is now shipping with IQ.Pilot. IQ.OS is available for all supported devices: Comma 3, Comma 3x, Comma 4, Konik A1/M, and Mr.One C3/C3X lite. It's a lightweight OS based on Ubuntu 24.04, includes Bluetooth (BLE), has a smaller install footprint, and is continuously optimized to remove anything IQ.Pilot doesn't need.

- Konn3kt now stays online regardless of IQ.Pilot's status. If IQ.Pilot fails to boot, Konn3kt remains available so you can switch branches, SSH in, and recover without a physical connection.
- Konn3kt setup time on a fresh install dropped from ~30 minutes to ~10 seconds.
- Bluetooth connectivity with Konn3kt is supported on all IQ.OS devices, including the Comma 3.
- Automatic LocalAPI configuration for faster and more stable Local SSH in Konn3kt.
- Fixed AGNOS Wi-Fi driver crash.
- Fixed Comma 4 green-screen issue.
- Fixed Comma 4 display calibration for accurate colors.

**Updater: Pre-download Mode**

A new "Update Install Mode" setting in Software settings gives you control over how updates are applied:

- **Predownload Only** — updates download in the background but wait for you to tap a button before installing.
- **Predownload + Preinstall** — downloads and installs automatically, same as before.

**Konn3kt Services**

Konn3kt clients have migrated to `app.konn3kt.com` to reduce router and ISP interference. The old `*.teallvbs.xyz` endpoints are now deprecated. Connection stability between Konn3kt and IQ.Pilot (Konn3ktion) is greatly improved. Konn3kt can now control AOL (Always-On Lateral) remotely without needing to go on-device to the settings.

**eSIM**

eSIM detection, provisioning, and profile management groundwork is now built into the device. The app can detect whether your device has an embedded SIM, provision it, and manage profiles without a physical SIM swap. eSIM support requires a compatible data plan — contact IQ.Lvbs support for known working eSIM carriers and plans. Note: eSIM is experimental and generally requires a hotspot-style data plan or an MVNO that does not IMEI filter.

