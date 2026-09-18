# Headless Raspberry Pi 5 setup, no monitor needed

Written before the hardware arrived. Verify menu names against the current Raspberry Pi Imager.

## 1. Flash the card (laptop, 15 minutes)

1. Install Raspberry Pi Imager from https://www.raspberrypi.com/software/
2. Insert the microSD. Open Imager.
3. Device: Raspberry Pi 5. OS: Raspberry Pi OS (64-bit), the full desktop version. Storage: your card.
4. Click Next, then Edit Settings:
   - Hostname: `robo1`
   - Username: `pi`, a password you will remember
   - Wi-Fi: your home network name and password, country IN
   - Services tab: enable SSH with password authentication
5. Write. Eject when done.

## 2. First boot (5 minutes)

1. Card into the Pi, cooler fitted, plug the 27 W supply. Wait two minutes.
2. On the laptop: `ssh pi@robo1.local`. If that name does not resolve, find the Pi's IP in your router's device list and use `ssh pi@<ip>`.
3. Once in:
   ```
   sudo apt update && sudo apt full-upgrade -y
   sudo raspi-config
   ```
   In raspi-config: Interface Options, enable I2C and Camera (if listed), then reboot.

## 3. Freenove's library and test

```
cd ~
git clone --depth 1 https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi.git
cd Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/Code
```
Follow the kit PDF's "Test" chapter: it runs motor, servo, ultrasonic, line sensor and camera tests one by one. Every test passing is the end of stage 0.

## 4. Our code

```
cd ~
git clone https://github.com/shivekkapoor/home-robo.git
cd home-robo/robot
python3 stage1_line.py --dry-run
```
