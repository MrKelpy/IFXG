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


def anti_afk_thread(action_lock: threading.Lock, logs_path: str):
    """
    Keeps the bot from being detected as an AFK player.
    This is achieved by first selecting a random action to be performed, and after
    a certain period of time, performing it.
    The available actions are the following:
        > Emoting
        > Moving
        > Jumping

    :return:
    """

    # We're using the keyboard module to simulate keypresses, this
    # means that we have to pass in the actual key names, i.a "a", "b", "RETURN".
    while True:
        time.sleep(15)  # Action cooldown

        with action_lock:

            actions = ["emoting", "moving", "jumping"]
            action_choice = random.choice(actions)
            focus_fortnite()

            log(logs_path, f"Performing '{action_choice}' action.", "ANTIAFK")
            if action_choice == "emoting":

                # Handles emoting
                keyboard.press("b")
                time.sleep(0.5)
                keyboard.release("b")

            elif action_choice == "moving":

                # Handles movement
                direction = random.choice(['w', 'a', 's', 'd'])
                keyboard.press(direction)
                time.sleep(1)
                keyboard.release(direction)

            else:

                # Handles jumps
                keyboard.press_and_release("SPACE")
