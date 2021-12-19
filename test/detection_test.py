# -*- coding: utf-8 -*-
# Created at 17/12/2021
__author__ = "MrKelpy / Alexandre Silva"
__github__ = "github.com/MrKelpy"
__copyright__ = "© Alexandre Silva 2021"
__license__ = "GNU GENERAL PUBLIC LICENSE v3"

# Built-in Imports
# Third Party Imports
import pyautogui
import keyboard

# Local Application Imports

keyboard.wait("º")

try:
    x, y = pyautogui.locateCenterOnScreen("../src/assets/afknotice.png", grayscale=False, confidence=0.75)
    print(f"found {x, y}")
except pyautogui.ImageNotFoundException:
    print("not found")