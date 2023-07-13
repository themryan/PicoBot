"""
@mainpage PicoBot Entry Poiht

@file code.py

@description This file provides the main entry point for CircuitPython code on the Raspberry Pi Pico

@author Michael Ryan
@date {6/18/23}
"""

import board
from display import Display
import time
from base import Base
from wifi_connection import WifiConnection
from robot_modes import RobotMode
from exploration import Exploration
from racing import Racing
from dance import Dance
from debug import Debug
from remote import Remote
from exploration import Exploration

# Define the screen board connections here
SCREEN_SCL = board.GP13
SCREEN_SDA = board.GP12
display = Display(SCREEN_SDA,SCREEN_SCL)

# Connect to the wifi
wifi_connection = WifiConnection(display)
connected = (wifi_connection.get_ip() is not None)
base = Base(display, connected)
base.output.startup_screen(base.troop_id_str)

# Wait a bit to allow the user to read the screen
time.sleep(5)

base.output.erase()
base.output.screen("Hi " + base.i_am, 0, 4, 0)

robot_mode = RobotMode()

mode_control = None

# What robot mode are we in?
if robot_mode.mode == RobotMode.MODE_EXPLORE:
    mode_control = Exploration(base)
elif robot_mode.mode == RobotMode.MODE_DANCE:
    mode_control = Dance(base)
elif robot_mode.mode == RobotMode.MODE_REMOTE:
    mode_control = Remote(base)
elif robot_mode.mode == RobotMode.MODE_RACING:
    mode_control = Racing(base)
elif robot_mode.mode == RobotMode.MODE_DEBUG:
    mode_control = Debug(base)
    mode_control.wifi_connection = wifi_connection
elif robot_mode.mode == RobotMode.MODE_SLEEP:
    touch_alarm = alarm.touch.TouchAlarm(pin=board.IO5)
    alarm.exit_and_deep_sleep_until_alarms(touch_alarm)

while True:
    base.loop()
    mode_control.loop()

    time.sleep(0.005)
