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
import pyautogui
import pygetwindow

# Local Application Imports

def focus_fortnite():
    """
    Hands over the window focus to the fornite screen.
    :return:
    """
    ft_window = [x for x in pygetwindow.getAllWindows() if x.title.strip() == "Fortnite"][0]
    ft_window.activate()


def anti_afk_thread(action_lock: threading.Lock):
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

            print(f"[IFXG][ANTIAFK] Performing '{action_choice}' action.")
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
