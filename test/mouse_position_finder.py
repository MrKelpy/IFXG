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
import LaminariaCore

while True:
    keyboard.wait("º")
    x = mouse.get_position()[0]
    y = mouse.get_position()[1]
    relx, rely = LaminariaCore.get_relative_screen_coords(x, y)
    xx, yy = LaminariaCore.get_absolute_screen_coords(relx, rely)
    print(f"Relative X: {relx, x}")
    print(f"Relative Y: {rely, y}")
    print(f"Abs. X: {xx}")
    print(f"Abs. Y: {yy}")