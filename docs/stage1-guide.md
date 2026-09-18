# Stage 1 guide: the car follows a black tape line and stops for a hand

One page. Start here only after stage 0 has passed (`docs/pi-setup.md`): every Freenove test worked and their laptop client drove the car.

**Pass test:** three laps of a 2 m taped loop without leaving the tape, and a stop about 20 cm from a hand placed in front. Film it.

## 1. What you need

- The built car, cells charged, Pi on Wi-Fi, laptop that can `ssh pi@robo1.local`.
- Black electrical tape, 18 to 19 mm wide, one roll. From home.
- About 1.5 m by 1.5 m of plain floor with a light, matte surface. Pale tiles, wood or a light rug work. Avoid dark floors, glossy black tiles and strong sunlight patches, which the sensors read as tape.
- Our code on the Pi, from section 7 of the setup doc: `~/home-robo/robot`.

## 2. Lay the track (15 minutes)

1. Make a loop about 2 m around: a rounded rectangle roughly 70 cm by 50 cm. Keep every bend gentle, no tighter than a 25 cm radius, so the outer wheels can follow. No sharp corners, no crossings for now.
2. Lay the tape in one continuous run, pressed flat, no gaps or overlaps at joins.
3. Optionally add a short crossbar of tape across the line at one point. All three sensors see tape at once there, and the code treats that as an end marker and stops. Leave it out for the lap test; add it later to test the stop.

## 3. Sensor check before driving (5 minutes)

Car on the track, wheels on the floor, S1 on, S2 off so nothing moves. SSH in:

```
cd ~/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/Code/Server
sudo python3 test.py Infrared
```

Slide the car sideways across the tape by hand. It should print Left, then Middle, then Right as each sensor crosses the tape. If it prints nothing or prints constantly, the sensors need adjusting: each has a small screw on top. Turn it a quarter turn at a time until plain floor is silent and tape triggers. Ctrl+C when done.

## 4. First run, wheels up (5 minutes)

Car on a box, wheels free, S1 and S2 on:

```
cd ~/home-robo/robot
sudo python3 stage1_line.py
```

Hold a strip of tape under the centre sensor: both sides of wheels turn forward at the same speed. Move it under the left sensor: left wheels slow, right wheels speed up. Under the right: the reverse. Nothing under any sensor: it creeps for one second, then stops and prints `line lost, stopped`. Hand in front of the ultrasonic sensor at 15 cm: it prints `obstacle, waiting` and the wheels stop. Ctrl+C ends it and the wheels stop.

If any of these is wrong, paste me the full terminal output and describe which wheels moved. Do not go to the floor until all five behave.

## 5. On the track (the rest of the session)

Place the car on the tape, centre sensor over the line, pointing along it. Run the same command. Stand ready to lift it.

What you will probably see, and the one knob to turn each time, at the top of `stage1_line.py`:

| Symptom | Change |
|---|---|
| Runs off the outside of bends | `TURN` up by 5. If it still runs wide at `TURN = 35`, go to 45: the inner wheels then reverse, which is how Freenove's own line follower turns. |
| Wobbles side to side on straights | `TURN` down by 5, or `BASE` down by 5. |
| Too slow to be interesting | `BASE` up by 5 once laps are clean. Above 50 the sensors lag the wheels; expect to raise `TURN` with it. |
| Stops on a straight with `line lost` | A gap in the tape, or the floor is dark there. Check the tape, or re-run the section 3 check at that spot. |
| Stops at a bend with `junction or end marker` | The bend is tight enough that all three sensors see tape. Widen the bend. |
| Stops for no obstacle | Sunlight or a soft surface confusing the ultrasonic sensor. Run `test.py Ultrasonic` pointing at the same spot; if it reads 0 or jumps, move the track. |

Change one number, save, run again. Send me a video of a lap and the terminal output when it fails; I read the pattern and tell you the next change.

## 6. Pass test

Three consecutive laps, no hand touching the car, then a hand held at 20 cm in front: the car stops and waits, and moves on when the hand is removed. Film the whole thing in one take. Commit the `BASE` and `TURN` values that passed:

```
cd ~/home-robo
git add robot/stage1_line.py
git commit -m "Stage 1 passed: BASE and TURN tuned on the floor"
git push
```

Then message me "stage 1 passed" with the video. Stage 2, the phone web page, starts from there.

## Rules that stay in force

- Cells charged before every session. A low battery shows up as a car that steers worse every lap.
- Ctrl+C stops the motors. If the terminal freezes, switch S2 off.
- Never lift the car by the camera head.
