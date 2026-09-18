# Stage 0: headless Raspberry Pi 5 setup and Freenove's tests, no monitor needed

Written before the hardware arrived, from Freenove's tutorial PDF (`Tutorial(ordinary_wheels).pdf` in their repo, chapters 0 to 3 and 7) and their `Code/setup.py` at commit a49db4b. Verify menu names against the current Raspberry Pi Imager. Send a photo before every first power-on.

Stage 0 is done when Freenove's own tests pass on every module and their laptop client drives the car. Then stage 1 starts: `docs/stage1-guide.md`.

## 1. Flash the card (laptop, 15 minutes)

1. Install Raspberry Pi Imager from https://www.raspberrypi.com/software/
2. Insert the microSD. Open Imager.
3. Device: Raspberry Pi 5. OS: Raspberry Pi OS (64-bit), the full desktop version. Freenove's installer needs the desktop packages even though we never plug in a monitor. Storage: your card.
4. Click Next, then Edit Settings:
   - Hostname: `robo1`
   - Username: `pi`, a password you will remember. Freenove's autostart script assumes the user is `pi`.
   - Wi-Fi: your home network name and password, country IN
   - Services tab: enable SSH with password authentication
5. Write. Eject when done.

## 2. First boot and basic config (10 minutes)

1. Card into the Pi, cooler fitted, plug the official 27 W supply into the Pi's USB-C. Wait two minutes. Do not fit the Pi to the car yet.
2. On the laptop: `ssh pi@robo1.local`. If that name does not resolve, find the Pi's IP in your router's device list and use `ssh pi@<ip>`.
3. Once in:
   ```
   sudo apt update && sudo apt full-upgrade -y
   sudo apt install -y i2c-tools python3-smbus
   sudo raspi-config
   ```
   In raspi-config: Interface Options, enable I2C. Also enable VNC if you ever want to see the desktop from the laptop. There is no Camera option on current Pi OS; Freenove's installer handles the camera in the next section. Finish, and say yes to reboot.

Paste me the last 10 lines of the `apt` output if anything says "error".

## 3. Freenove's library installer (15 minutes, needs internet)

```
cd ~
git clone --depth 1 https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi.git
cd Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/Code
sudo python3 setup.py
```

The installer downloads packages, then asks two questions:

| Question | Answer |
|---|---|
| Camera model, `ov5647` or `imx219` | `ov5647`. That is the camera in the kit. |
| Camera port, `cam0` or `cam1` | Whichever port on the Pi 5 you plugged the ribbon cable into. The labels CAM/DISP 0 and CAM/DISP 1 are printed on the board next to the two connectors. Answer the one you used. |

It edits `/boot/firmware/config.txt` (turns SPI on, sets `camera_auto_detect=0`, adds `dtoverlay=ov5647,cam0` or `cam1`) and keeps a `.bak` copy. Then:

```
sudo reboot
```

If it prints "Some libraries have not been installed yet", run `sudo python3 setup.py` again; that is almost always the network. If it fails twice, paste me the output.

## 4. Assemble the car (Freenove PDF chapter 2, 2 to 3 hours)

Follow the PDF's chapter 2 step by step, or the video linked in it. Three things to get right:

- **Batteries last.** Fit the two 18650 cells only after everything else is built and charged. Freenove's `About_Battery.pdf` says assembling without charged cells can damage the servos during the first power-up.
- **Camera ribbon.** The Pi 5 end uses the narrow 22-pin cable from the order list, not the wide 15-pin one. Contacts face the board on both ends. Note which port you used; it must match your answer in section 3.
- **Two switches.** S1 is the main power switch. S2 powers motors and servos. Both must be on for the tests.

Send me four photos before switching on: top of the car, the Pi and its ribbon cable, the battery holder with cells in, and the connection board. I check the wiring against the PDF before you press S1.

## 5. Test every module (Freenove PDF chapter 3, 30 minutes)

Car on a box so the wheels are off the floor. S1 and S2 on. The 5 V, 3.3 V and battery lights on the board should be lit. SSH in, then:

```
i2cdetect -y 1
```

You should see `40` and `48` in the grid. Those are the two chips on the connection board. If the grid is empty, S1 is off or the Pi is not seated on the board. Then:

```
cd ~/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/Code/Server
sudo python3 test.py Motor
```

The first time any Freenove program runs it asks for a **Connect Version** and a **PCB Version**, each 1 or 2. Both refer to the connection board. Read the version printed on the board: `PCB_V1.0` means answer `1` to both, `PCB_V2.0` means `2`. If you are unsure, send me a photo of the board before answering. Wrong answers only mean the LEDs do not light; the file `params.json` can be deleted and the questions come back.

Run each test in turn. Ctrl+C stops the ones that loop.

| Command | What should happen |
|---|---|
| `sudo python3 test.py Motor` | Wheels go forward, back, left turn, right turn, stop. One second each. |
| `sudo python3 test.py Servo` | Camera head pans, then tilts, back and forth. |
| `sudo python3 test.py Ultrasonic` | Prints a distance in cm. Put your hand at 20 cm; the number should follow it. |
| `sudo python3 test.py Infrared` | Prints Left, Middle or Right as you slide a strip of black tape under the three sensors. Nothing prints on a plain floor; that is normal. |
| `sudo python3 test.py Led` | The board's LEDs cycle through colours. |
| `sudo python3 test.py Buzzer` | Beeps for three seconds. |
| `sudo python3 test.py ADC` | Prints the battery voltage. Two fresh cells read about 8 V. |

Camera, without a screen:

```
rpicam-still -o ~/cam.jpg
```

Then on the laptop, `scp pi@robo1.local:cam.jpg .` and open it. If the command says no camera found, the port answer in section 3 does not match the cable, or the cable is in backwards. Also check the lens film is peeled off.

Paste me any test's full output if it does not match the table.

## 6. Stage 0 pass test: drive it from the laptop (PDF chapter 7)

Freenove's demo is a server on the Pi and a client program on your Mac. There is no phone app; our own phone page is stage 2.

On the Pi:
```
cd ~/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/Code/Server
sudo python3 main.py -t
```

On the Mac, once:
```
cd ~
git clone --depth 1 https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi.git
cd Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/Code
python3 setup_macos.py
```
Then each time:
```
cd ~/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/Code/Client
python3 Main.py
```

Type the Pi's IP into the client, connect, and drive with the arrow buttons. Video should show in the window. Car drives and video shows: stage 0 passed. Take a 20-second video for the record.

## 7. Our code

```
cd ~
git clone https://github.com/shivekkapoor/home-robo.git
cd home-robo/robot
python3 stage1_line.py --dry-run
```

Prints what it would do without touching the motors. Ctrl+C to stop. Then go to `docs/stage1-guide.md`.

## If something is wrong

| Symptom | Fix |
|---|---|
| `ssh` says connection refused or host not found | Wait another minute; first boot resizes the card. Then check the router's device list for `robo1`. If absent, the Wi-Fi name or password in Imager was wrong: re-flash. |
| `i2cdetect` shows nothing | S1 off, or I2C not enabled in raspi-config, or the Pi is not fully pushed onto the board's header. |
| Motors do not move but the test prints normally | S2 off, or batteries flat. Run `test.py ADC` and read the voltage. |
| Servo jitters or the board resets during tests | Batteries low. Charge them. The USB-C supply does not charge the cells. |
| LEDs do not light, everything else works | Wrong PCB version answer. Delete `params.json` in `Code/Server` and rerun. |
| Camera not found | Port answer does not match the cable, or the cable is backwards. Re-run `sudo python3 setup.py` and answer the other port. |
| Client on the Mac will not connect | Both devices on the same Wi-Fi; server running on the Pi first; IP typed correctly (`hostname -I` on the Pi). |
