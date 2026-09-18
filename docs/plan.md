# home-robo plan

**Kit:** Freenove 4WD Smart Car Kit for Raspberry Pi (FNK0043), Raspberry Pi 5 4 GB.
**Started:** 18 September 2026.

## Stages

| Stage | Weeks | What you build | What you learn | Pass test |
|---|---|---|---|---|
| 0. Setup | arrival week | Assemble the kit from Freenove's PDF. Flash Pi OS headless. SSH in from the laptop. Run Freenove's own test to prove motors, servo, camera and sensors | Assembly, Linux basics, SSH | Freenove's demo drives the car from the phone app |
| 1. Drives | 1 to 2 | Our `stage1_line.py`: follow black tape, stop for obstacles | Reading sensors, the simplest control loop, motor speed | Three laps of a 2 m loop; stops 20 cm from a hand |
| 2. Obeys | 3 | `stage2_web.py`: a web page on the robot with joystick and buttons | A tiny web server, events, state | Every button acts within half a second |
| 3. Follows | 4 to 7 | `stage3_follow.py`: camera tracks a colour marker, then a person, and steers to keep it centred | Image capture, detection, proportional control | Follows a slow walk for 2 minutes |
| 4. Listens | 8 to 10 | `stage4_voice.py`: mic, speech-to-text, language-model bridge to commands | Audio, APIs, intent to action | Eight of ten spoken commands executed |
| 5. Remembers | 11+ | Face recognition, named places, saved routes | Persistence, simple maps | Drives to a named place |

## Budget

About ₹30,500 for parts with a Pi 5 4 GB, or ₹37,000 with the 8 GB (live prices, 18 September 2026; see `docs/order-list.md`). Up from ₹18,000 to ₹23,000 in the first draft. Cloud speech and language services for stage 4 cost a few hundred rupees a month at hobby volume.

## Commercial note, parked

A consumer follow-me robot is a dead category. If this ever becomes a business, the plausible path is a STEM education kit with a curriculum for Indian schools. Revisit after stage 4, not before.
