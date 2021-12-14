# -*- coding: utf-8 -*-
# Created at 13/12/2021
__author__ = "MrKelpy / Alexandre Silva"
__github__ = "github.com/MrKelpy"
__copyright__ = "© Alexandre Silva 2021"
__license__ = "MIT LICENSE"

# Built-in Importsºººº
# Third Party Imports
import time

import screeninfo
import keyboard
import mouse
import pyautogui

# Local Application Imports

while True:
    keyboard.wait("º")
    x = mouse.get_position()[0]
    y = mouse.get_position()[1]
    monitor = screeninfo.get_monitors()[0]

    print(f"Relative X: {(x*100)/monitor.width}")
    print(f"Relative Y: {(y*100)/monitor.height}")
    print(f"Calculated: {0.01*((x*100)/monitor.width) * monitor.width}")
    print(f"Calculated: {0.01*((y*100)/monitor.height) * monitor.height}")
    print(f"TrueX: {x}")
    print(f"TrueY: {y}")
    xx = 0.01*((x*100)/monitor.width) * monitor.width
    yy = 0.01*((y*100)/monitor.height) * monitor.height

    time.sleep(2)
    pyautogui.moveTo(xx, yy)