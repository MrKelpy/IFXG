# -*- coding: utf-8 -*-
# Created at 13/12/2021
__author__ = "MrKelpy / Alexandre Silva"
__github__ = "github.com/MrKelpy"
__copyright__ = "© Alexandre Silva 2021"
__license__ = "MIT LICENSE"

# Built-in Imports
import time
import random
import threading

# Third Party Imports
import keyboard

# Local Application Imports
from utils.focus import focus_fortnite
from utils.logging import log


def perform_emote():
    """
    Performs an emote in the game.
    :return:
    """
    keyboard.press("b")
    time.sleep(0.5)
    keyboard.release("b")


def anti_afk_thread(action_lock: threading.Lock, logs_path: str):
    """
    Keeps the bot from being detected as an AFK player.
    This is achieved by performing a random emote, since that a simple action
    that takes a buttonpress to perform, and cancels the AFK timer.
    This is not 100% accurate, so there will be another thread handling the actions when this fails.
    :return:
    """

    log(logs_path, "Started the main ANTI-AFK system thread.", "INIT")
    # We're using the keyboard module to simulate keypresses, this
    # means that we have to pass in the actual key names, i.a "a", "b", "RETURN".
    while True:
        time.sleep(15)  # Action cooldown

        with action_lock:
            focus_fortnite()
            perform_emote()
            log(logs_path, "Cancelled AFK Timer.", "ANTI-AFK")