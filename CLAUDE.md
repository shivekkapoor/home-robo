# home-robo: project context for Claude (read first)

**Owner:** Shivek, Gurgaon. Product manager focused on distribution, ex-consultant. No coding or hardware experience. Building a robot for fun with Claude as the engineer. Commercial angle later only if it earns it. Wants senior-executive style: data-backed, simple, honest, and welcomes critical assessments.

**Previous project (pigeon deterrent) is dropped.** Do not bring it back unless the owner asks. History lives in the old `Pigeon` repo.

## The robot

Freenove 4WD Smart Car Kit for Raspberry Pi (FNK0043) on a Raspberry Pi 5, 4 GB. Five stages, each a weekend or two:

| Stage | Does | Pass test |
|---|---|---|
| 1. Drives | Follows a black tape line, stops 20 cm from an obstacle | Completes a 2 m loop three times without leaving the tape; stops for a hand |
| 2. Obeys | Phone web page: joystick, come, stop, turn, patrol | Every button does its thing within half a second |
| 3. Follows | Camera keeps the owner centred at a set distance. Colour marker first, person detection second | Follows a slow walk around a room for 2 minutes without losing them |
| 4. Listens | USB mic, speech-to-text, a language model turns "come to the kitchen" into robot commands | Ten spoken commands, eight executed correctly |
| 5. Remembers | Recognises the owner's face, remembers named places and routes | Drives to a named place on request |

Genuine learning from experience (reinforcement learning) is out of scope. Say so if asked.

## Status

- Parts being ordered per `docs/order-list.md`. Nothing assembled or flashed yet.
- `robot/` holds stage 1 code written WITHOUT access to the kit or the Freenove library. First job of any session with network: read Freenove's GitHub repo for this kit, confirm the Pi 5 library's class and method names, and fix `robot/hw.py` to match.

## First things a new session should do

1. `git log` and `docs/plan.md` to see where things stand.
2. Verify `robot/hw.py` against https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi (the Pi 5 version of their `Code/Server` folder). Fix names. Run `python3 -m py_compile` on everything.
3. Re-verify stock and price on every link in `docs/order-list.md`.
4. Keep `docs/pi-setup.md` current with the Raspberry Pi OS release the owner will flash.

## Working rules

- Every instruction written for someone who has never done it. Numbered stages, each ending in a test.
- Ask for a photo before power-on. Ask for pasted terminal output on errors.
- The owner runs commands on the Pi over SSH from a laptop; no monitor on the Pi.
- Be honest about what works and what is unverified. Mark unverified code as such in the file header.
- Never put a model identifier in commits or files.
- Docs are the record: when a decision changes, update the doc, README, commit, push.

## Repo map (home-robo)

`README.md` overview. `docs/plan.md` stages and timeline. `docs/order-list.md` parts with Indian links. `docs/pi-setup.md` headless Pi setup. `robot/` code: `hw.py` hardware adapter, `stage1_line.py`, later `stage2_web.py`, `stage3_follow.py`, `stage4_voice.py`.
