import board
import time
import usb_hid
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn
from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# --- INIT USB HID DEVICES ---
mouse = Mouse(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)

# --- PIN CONFIGURATION ---
btn_forward = DigitalInOut(board.GP26)
btn_forward.direction = Direction.INPUT
btn_forward.pull = Pull.UP

btn_back = DigitalInOut(board.GP22)
btn_back.direction = Direction.INPUT
btn_back.pull = Pull.UP

btn_fire = DigitalInOut(board.GP27)
btn_fire.direction = Direction.INPUT
btn_fire.pull = Pull.UP

pot = AnalogIn(board.GP28)

# --- STATS & TIMERS ---
shots_fired = 0
deaths = 0
session_start = time.monotonic()
last_send = time.monotonic()

fire_was_pressed = False
combo_start = None

# --- MAIN LOOP ---
while True:
    now = time.monotonic()

    # Movement Control (Keyboard W/S)
    if not btn_forward.value:
        keyboard.press(Keycode.W)
    else:
        keyboard.release(Keycode.W)

    if not btn_back.value:
        keyboard.press(Keycode.S)
    else:
        keyboard.release(Keycode.S)

    # Fire Control (Mouse Left Click with Edge Detection)
    fire_pressed = not btn_fire.value
    if fire_pressed and not fire_was_pressed:
        shots_fired += 1
        mouse.press(Mouse.LEFT_BUTTON)
    elif not fire_pressed:
        mouse.release(Mouse.LEFT_BUTTON)
    fire_was_pressed = fire_pressed

    # Aim Control (Potentiometer -> Mouse X Axis)
    pot_val = (pot.value / 65535) * 100
    if pot_val < 45:
        move = -int((45 - pot_val) / 2)
    elif pot_val > 55:
        move = int((pot_val - 55) / 2)
    else:
        move = 0
    mouse.move(x=move)

    # Death/Respawn Reset Combo (Hold Forward + Back for 1s)
    both = not btn_forward.value and not btn_back.value
    if both:
        if combo_start is None:
            combo_start = now
        elif now - combo_start >= 1.0:
            deaths += 1
            shots_fired = 0
            session_start = now
            combo_start = None
    else:
        combo_start = None

    # Serial Telemetry Output (1Hz)
    if now - last_send >= 1.0:
        elapsed = int(now - session_start)
        print("{},{},{}".format(shots_fired, elapsed, deaths))
        last_send = now

    time.sleep(0.01)