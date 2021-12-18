# -*- coding: utf-8 -*-
# Created at 17/12/2021
__author__ = "MrKelpy / Alexandre Silva"
__github__ = "github.com/MrKelpy"
__copyright__ = "© Alexandre Silva 2021"
__license__ = "GNU GENERAL PUBLIC LICENSE v3"

# Built-in Imports
import threading
import time

# Third Party Imports
import pyautogui
import keyboard

# Local Application Imports
import LaminariaCore
from utils.logging import log
from utils.focus import focus_fortnite


def check_for_afk_notice(action_lock: threading.Lock, afk_notice: str):
    """
    Checks if an afk notice is present on the screen
    :return:
    """
    try:
        with action_lock:
            focus_fortnite()
            _, _ = pyautogui.locateCenterOnScreen(afk_notice, grayscale=True, confidence=0.7)

        return True

    except ValueError:
        return False

    except TypeError:
        return False


def leave_game(action_lock: threading.Lock):
    """
    Leaves the current imposters game. This is achieved by performing a series of
    actions that lead up to leaving the game.
    :return:
    """

    leave_x, leave_y = LaminariaCore.get_absolute_screen_coords(2.7, 93.6)
    leave_match_x, leave_match_y = LaminariaCore.get_absolute_screen_coords(15.4, 16)
    confirm_x, confirm_y = LaminariaCore.get_absolute_screen_coords(60, 72)

    with action_lock:
        focus_fortnite()

        # Hit ESC to bring up the menu
        keyboard.send("ESC")
        time.sleep(0.1)

        # Hit the first leave button
        pyautogui.moveTo(leave_x, leave_y)
        pyautogui.click()
        time.sleep(0.1)

        # Hit the leave match button
        pyautogui.moveTo(leave_match_x, leave_match_y)
        pyautogui.click()
        time.sleep(0.1)

        # Hit the confirmation button
        pyautogui.moveTo(confirm_x, confirm_y)
        pyautogui.click()
        time.sleep(0.1)


def afk_detection_thread(action_lock: threading.Lock, logs_path: str):
    """
    Because the AntiAFK system is not 100% accurate, this thread handles
    any cases where the former should fail, by leaving the match and entering a new
    one. This makes it so the bot only gets the most experience it can without wasting
    time on low-xp matches.
    :return:
    """

    afk_notice = "./assets/afknotice.png"
    log(logs_path, "Started the complementary AFK Detection system thread.", "INIT")

    while True:

        time.sleep(1) # Generic checking cooldown

        # Performs the game-leaving
        if not check_for_afk_notice(action_lock, afk_notice):
            continue

        log(logs_path, "AFK notice detected. Leaving the game.", "AFKDETECT")
        leave_game(action_lock)
