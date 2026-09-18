"""Hardware adapter for the Freenove 4WD kit on Raspberry Pi 5.

Names VERIFIED against Freenove's repo, Code/Server, commit a49db4b (12 March 2026).
Behaviour UNVERIFIED on real hardware: nothing has been run on the car yet.
Everything else in robot/ talks only to this file.

Freenove modules used (one Code/Server folder now serves Pi 3, 4 and 5):
  motor.py       -> Ordinary_Car().set_motor_model(fl, bl, fr, br)  -4095..4095, + is forward
  ultrasonic.py  -> Ultrasonic().get_distance()                     cm, or None on a bad read
  infrared.py    -> Infrared().read_all_infrared()                  3 bits: left, centre, right
  servo.py       -> Servo().set_servo_pwm('0' or '1', angle)        '0' pan, '1' tilt

Checked against Freenove's own line follower (car.py, mode_infrared): value 2 (centre only)
drives straight, 4 (left only) turns left, 1 (right only) turns right, 7 stops. So 1 = sees
the black line, and bit 2 is the left sensor.
"""
import sys, os

FREENOVE_CODE = os.path.expanduser("~/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/Code/Server")


class Robot:
    def __init__(self, dry_run=False):
        self.dry = dry_run
        if dry_run:
            return
        sys.path.insert(0, FREENOVE_CODE)
        from motor import Ordinary_Car
        from ultrasonic import Ultrasonic
        from infrared import Infrared
        from servo import Servo
        self.motor, self.sonar, self.line, self.servo = Ordinary_Car(), Ultrasonic(), Infrared(), Servo()

    # speed in -100..100 per side
    def drive(self, left, right):
        l, r = int(left * 40.95), int(right * 40.95)
        if self.dry:
            print(f"[drive] L={left:4d} R={right:4d}")
            return
        self.motor.set_motor_model(l, l, r, r)

    def stop(self):
        self.drive(0, 0)

    def distance_cm(self):
        """Distance to the nearest object. A failed read returns 0, so callers stop to be safe."""
        if self.dry:
            return 100.0
        d = self.sonar.get_distance()
        return 0.0 if d is None else float(d)

    def line_bits(self):
        """Returns (left, centre, right) as 0/1, 1 = sees the black line."""
        if self.dry:
            return (0, 1, 0)
        v = int(self.line.read_all_infrared())
        return ((v >> 2) & 1, (v >> 1) & 1, v & 1)

    def head(self, pan_deg=90, tilt_deg=90):
        if self.dry:
            return
        self.servo.set_servo_pwm("0", pan_deg)
        self.servo.set_servo_pwm("1", tilt_deg)
