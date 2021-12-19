# -*- coding: utf-8 -*-
# Created at 19/12/2021
__author__ = "MrKelpy / Alexandre Silva"
__github__ = "github.com/MrKelpy"
__copyright__ = "© Alexandre Silva 2021"
__license__ = "GNU GENERAL PUBLIC LICENSE v3"

# Built-in Imports
import threading
import time

# Third Party Imports
import pyautogui

# Local Application Imports
from utils.logging import log
from utils.focus import focus_fortnite


def checkfor_continue(action_lock: threading.Lock, error_continue: str):
    """
    Checks for a continue button in the screen.
    This function returns a flag and the coords, the flag being a Bool, of the
    success on finding the continue button, and the coords being a list
    with the x and y coordinates of the button.
    :return: Bool, List
    """

    try:
        with action_lock:
            focus_fortnite()
            time.sleep(0.1)
            x, y = pyautogui.locateCenterOnScreen(error_continue, grayscale=True, confidence=0.75)
        return True, [x, y]

    except Exception:
        return False, None


def fix_screen(action_lock: threading.Lock, coords: list):
    """
    Fixes the screen by moving the mouse to the continue button
    and pressing it.
    :return:
    """
    with action_lock:
        focus_fortnite()
        pyautogui.moveTo(coords[0], coords[1])
        pyautogui.click()


def error_screen_fix_thread(action_lock: threading.Lock, logs_path: str):
    """
    Searches in the screen for the "continue" button every minute.
    This continue button appears only when there was an error, and there's no
    keybind to skip it, only the button. This is somewhat of a rare occurence,
    but it can really screw an afk session up.
    :return:
    """

    error_continue = "./assets/continue.png"

    while True:

        # Checks if an error has happened
        flag, coords = checkfor_continue(action_lock, error_continue)

        # If so, fix the screen and regardless, sleep for a minute.
        if flag:
            log(logs_path, "Game error found! Fixing it and continuing the bot.", "ERRFIX")
            fix_screen(action_lock, coords)

        time.sleep(60)


