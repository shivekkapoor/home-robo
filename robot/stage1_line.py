#!/usr/bin/env python3
"""Stage 1: follow a black tape line and stop for obstacles.

Run on the Pi:  python3 stage1_line.py            (real robot)
Dry run anywhere: python3 stage1_line.py --dry-run (prints what it would do)

Control loop, 50 times a second:
  read the three line sensors and the distance
  if something is closer than STOP_CM: stop, wait, retry
  else steer toward the sensor that sees the line
"""
import argparse, time
from hw import Robot

BASE = 35          # cruising speed, 0..100. Start low.
TURN = 25          # how hard to steer
STOP_CM = 20
LOOP_S = 0.02


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    bot = Robot(dry_run=args.dry_run)
    bot.head(90, 90)
    lost_since = None
    try:
        while True:
            if bot.distance_cm() < STOP_CM:
                bot.stop()
                print("obstacle, waiting")
                time.sleep(0.5)
                continue
            l, c, r = bot.line_bits()
            if c and not l and not r:
                bot.drive(BASE, BASE); lost_since = None
            elif l and not r:
                bot.drive(BASE - TURN, BASE + TURN); lost_since = None   # line is to the left: turn left
            elif r and not l:
                bot.drive(BASE + TURN, BASE - TURN); lost_since = None   # line is to the right: turn right
            elif l and c and r:
                bot.stop(); print("junction or end marker, stopping"); break
            else:
                # lost the line: creep forward briefly, then stop
                if lost_since is None:
                    lost_since = time.time()
                if time.time() - lost_since < 1.0:
                    bot.drive(BASE // 2, BASE // 2)
                else:
                    bot.stop(); print("line lost, stopped"); break
            time.sleep(LOOP_S)
            if args.dry_run and time.time() % 5 < LOOP_S:
                pass
    except KeyboardInterrupt:
        pass
    finally:
        bot.stop()


if __name__ == "__main__":
    main()
