"""Hardware adapter for the Freenove 4WD kit on Raspberry Pi 5.

UNVERIFIED: written before the kit or its library was available. Freenove has changed
class and method names between kit versions. A session with network access must open
Freenove's repo (Code/Server for the Pi 5 version) and fix the imports and method names
below. Everything else in robot/ talks only to this file, so nothing else changes.

Expected Freenove modules (older naming shown; newer versions use lowercase files and
a `Ordinary_Car` class with `set_motor_model`):
  Motor.py       -> Motor().setMotorModel(fl, bl, fr, br)   speeds -4095..4095
  Ultrasonic.py  -> Ultrasonic().get_distance()             cm
  Infrared.py    -> Infrared().read_all_infrared()           3-bit value, or read_one_infrared(n)
  servo.py       -> Servo().setServoPwm(channel, angle)
"""
import sys, os, time

FREENOVE_CODE = os.path.expanduser("~/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/Code/Server")


class Robot:
    def __init__(self, dry_run=False):
        self.dry = dry_run
        if dry_run:
            return
        sys.path.insert(0, FREENOVE_CODE)
        try:
            from Motor import Motor            # older naming
            from Ultrasonic import Ultrasonic
            from Infrared import Infrared
            from servo import Servo
            self.motor, self.sonar, self.line, self.servo = Motor(), Ultrasonic(), Infrared(), Servo()
            self._drive = lambda fl, bl, fr, br: self.motor.setMotorModel(fl, bl, fr, br)
            self._dist = self.sonar.get_distance
            self._line = self.line.read_all_infrared
            self._servo = self.servo.setServoPwm
        except ImportError:
            from motor import Ordinary_Car     # newer naming (verify)
            from ultrasonic import Ultrasonic
            from infrared import Infrared
            from servo import Servo
            self.motor, self.sonar, self.line, self.servo = Ordinary_Car(), Ultrasonic(), Infrared(), Servo()
            self._drive = lambda fl, bl, fr, br: self.motor.set_motor_model(fl, bl, fr, br)
            self._dist = self.sonar.get_distance
            self._line = self.line.read_all_infrared
            self._servo = self.servo.set_servo_pwm

    # speed in -100..100 per side
    def drive(self, left, right):
        l, r = int(left * 40.95), int(right * 40.95)
        if self.dry:
            print(f"[drive] L={left:4d} R={right:4d}")
            return
        self._drive(l, l, r, r)

    def stop(self):
        self.drive(0, 0)

    def distance_cm(self):
        if self.dry:
            return 100.0
        return float(self._dist())

    def line_bits(self):
        """Returns (left, centre, right) as 0/1, 1 = sees the black line."""
        if self.dry:
            return (0, 1, 0)
        v = int(self._line())
        return ((v >> 2) & 1, (v >> 1) & 1, v & 1)

    def head(self, pan_deg=90, tilt_deg=90):
        if self.dry:
            return
        self._servo("0", pan_deg)
        self._servo("1", tilt_deg)
