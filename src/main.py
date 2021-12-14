# -*- coding: utf-8 -*-
# Created at 13/12/2021
__author__ = "MrKelpy / Alexandre Silva"
__github__ = "github.com/MrKelpy"
__copyright__ = "© Alexandre Silva 2021"
__license__ = "MIT LICENSE"

# Built-in Imports
import threading
import time


# Third Party Imports
import screeninfo
import keyboard
import pyautogui

# Local Application Import
from threads.antiafk import anti_afk_thread, focus_fortnite


def get_play_button():
    """
    Returns the relative monitor position for the Play button.
    The values below have been acquired through testing.
    :return:
    """

    screen_info = screeninfo.get_monitors()[0]
    return (0.01*88.3)*screen_info.width, (0.01*68)*screen_info.height


def fix_screen():
    """
    Fixes the screen. This is extremely needed, since the
    level up screen comes up quite some times, and new shop updates
    can also appear, they'll often break the bot.
    This function exists to prevent that from happening, by occasionally esc'ing twice.
    :return:
    """
    keyboard.press_and_release("esc")
    time.sleep(0.1)
    keyboard.press_and_release("esc")


def skip_vote():
    """
    Skips the imposter vote. This function will be called before the finish_imposters
    due the way the latter works, which causes the side effect of voting on the person at the front
    of the bot.
    :return:
    """
    focus_fortnite()
    keyboard.press("f")
    time.sleep(5)
    keyboard.release("f")
    print("[IFXG][GAME] Tried-for skipping the vote.")


def hit_ready():
    """
    Hits the "Ready" button in the initializer screen.
    This assumes that the Imposters gamemode is already setup.
    :return:
    """
    fix_screen()
    focus_fortnite()
    x, y = get_play_button()
    pyautogui.moveTo(x, y)
    time.sleep(0.5)
    pyautogui.click()


def finish_imposters():
    """
    Long-presses the E key to finish a game of Imposters.
    This will take the bot out of the XP Screen and send it back to the initializer screen.
    :return:
    """
    skip_vote()
    focus_fortnite()
    keyboard.press("e")
    time.sleep(5)
    keyboard.release("e")


def start_bot():
    """
    Starts the bot and all of its threads.
    :return:
    """

    # Starts the anti-afk system
    action_lock = threading.Lock()  # Prevent two actions from happening at the same time.
    print("[IFXG][init] Initialized threading lock.")

    antiafk_thread = threading.Thread(target=anti_afk_thread, args=(action_lock,), daemon=True)
    antiafk_thread.start()
    print("[IFXG][init] Started the ANTI-AFK System.")

    print("[IFXG][init] Started main joining loop.")
    while True:
        """
        Main joining loop. This loop is responsible for keeping the bot alive and
        for joining Imposter games.
        
        This loop works on a trying-for basis. This means that the functions were written in a way that
        calling them won't break the game, and most likely will result in nothing if the conditions
        are not met. Calling any won't raise errors and the anti-afk system will function correctly.
        """

        with action_lock:
            hit_ready()
            print("[IFXG][GAME] Tried-for starting a new imposters game.")
        time.sleep(20)  # Generic cooldown, games take quite a while to happen, so there's no need to check for game finishes all the time.

        with action_lock:
            finish_imposters()
            print("[IFXG][GAME] Tried-for finishing the imposters game.")
        time.sleep(10)  # Around the time it should take for the bot to be sent to the initializer screen again.


if __name__ == "__main__":
    start_bot()
