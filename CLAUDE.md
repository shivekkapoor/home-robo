# home-robo: project context for Claude (read first)

**Owner:** Shivek, Gurgaon. Product manager focused on distribution, ex-consultant. No coding or hardware experience. Building a robot for fun with Claude as the engineer. Commercial angle later only if it earns it. Wants senior-executive style: data-backed, simple, honest, and welcomes critical assessments.

**Previous project (pigeon deterrent) is dropped.** Do not bring it back unless the owner asks. History lives in the old `Pigeon` repo.

## The robot

Freenove 4WD Smart Car Kit for Raspberry Pi (FNK0043) on a Raspberry Pi 5, 8 GB. Five stages, each a weekend or two:

| Stage | Does | Pass test |
|---|---|---|
| 1. Drives | Follows a black tape line, stops 20 cm from an obstacle | Completes a 2 m loop three times without leaving the tape; stops for a hand |
| 2. Obeys | Phone web page: joystick, come, stop, turn, patrol | Every button does its thing within half a second |
| 3. Follows | Camera keeps the owner centred at a set distance. Colour marker first, person detection second | Follows a slow walk around a room for 2 minutes without losing them |
| 4. Listens | USB mic, speech-to-text, a language model turns "come to the kitchen" into robot commands | Ten spoken commands, eight executed correctly |
| 5. Remembers | Recognises the owner's face, remembers named places and routes | Drives to a named place on request |

Genuine learning from experience (reinforcement learning) is out of scope. Say so if asked.

## Status

- Parts ordered 18 Sep 2026, see the "What was actually ordered" table in `docs/order-list.md`. Pi 5 8 GB chosen because the 4 GB was out of stock everywhere. robu.in items arrive within a week; the Freenove kit from Amazon.in is due 5 Oct 2026 and gates assembly. Nothing assembled or flashed yet.
- `robot/hw.py` names verified against Freenove's `Code/Server` (commit a49db4b, 12 Mar 2026). Still untested on hardware.
- Docs for stage 0 (`docs/pi-setup.md`) and stage 1 (`docs/stage1-guide.md`) are written from Freenove's tutorial PDF and installer, 18 Sep 2026. Unverified on hardware; expect small fixes on first use.
- The owner's next message will be "kit arrived, starting stage 0" with a photo of the unboxed parts. Respond by checking the photo against the order list, then walking `docs/pi-setup.md` one section at a time.

## How the owner starts a session

`cd ~/home-robo && claude`, so this file loads. Sessions have network access; use it for Freenove's repo and shop pages.

## First things a new session should do

1. `git log` and `docs/plan.md` to see where things stand.
2. If Freenove's repo has new commits since a49db4b, re-check `robot/hw.py` against `Code/Server` (motor.py, ultrasonic.py, infrared.py, servo.py) and the commands in `docs/pi-setup.md` against `Code/setup.py` and `Code/Server/test.py`. Run `python3 -m py_compile` on everything.
3. Parts are ordered; no more price checks needed unless something is returned.
4. Keep `docs/pi-setup.md` current with the Raspberry Pi OS release the owner will flash.

## Working rules

- Every instruction written for someone who has never done it. Numbered stages, each ending in a test.
- Ask for a photo before power-on. Ask for pasted terminal output on errors.
- The owner runs commands on the Pi over SSH from a laptop; no monitor on the Pi.
- Be honest about what works and what is unverified. Mark unverified code as such in the file header.
- Never put a model identifier in commits or files.
- Docs are the record: when a decision changes, update the doc, README, commit, push.

## Repo map (home-robo)

`README.md` overview. `docs/plan.md` stages and timeline. `docs/order-list.md` parts with Indian links. `docs/pi-setup.md` stage 0: headless Pi setup, Freenove installer, assembly pointers, module tests, laptop-client pass test. `docs/stage1-guide.md` stage 1: track, sensor check, tuning, pass test. `robot/` code: `hw.py` hardware adapter, `stage1_line.py`, later `stage2_web.py`, `stage3_follow.py`, `stage4_voice.py`.
