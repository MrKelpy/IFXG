# -*- coding: utf-8 -*-
# Created at 13/12/2021
__author__ = "MrKelpy / Alexandre Silva"
__github__ = "github.com/MrKelpy"
__copyright__ = "© Alexandre Silva 2021"
__license__ = "MIT LICENSE"

# Built-in Imports
import threading
import traceback
import time
import os


# Third Party Imports
import screeninfo
import keyboard
import pyautogui

# Local Application Import
import LaminariaCore
from threads.antiafk import anti_afk_thread
from utils.focus import focus_fortnite
from utils.logging import log


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


def skip_vote(lp: str):
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

    log(lp, "Tried-for skipping the vote.", "GAME")


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


def finish_imposters(lp: str):
    """
    Long-presses the E key to finish a game of Imposters.
    This will take the bot out of the XP Screen and send it back to the initializer screen.
    :return:
    """
    skip_vote(lp)
    focus_fortnite()
    keyboard.press("e")
    time.sleep(5)
    keyboard.release("e")


def start_bot(logs_path: str):
    """
    Starts the bot and all of its threads.
    :return:
    """

    # Starts the anti-afk system
    action_lock = threading.Lock()  # Prevent two actions from happening at the same time.
    log(logs_path, "Initialized threading lock.", "INIT")

    antiafk_thread = threading.Thread(target=anti_afk_thread, args=(action_lock, logs_path), daemon=True)
    antiafk_thread.start()
    log(logs_path, "Started the ANTI-AFK System.", "INIT")

    log(logs_path, "Started main joining loop.", "INIT")
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
            log(logs_path, "Tried-for starting a new imposters game.", "GAME")
        time.sleep(20)  # Generic cooldown, games take quite a while to happen, so there's no need to check for game finishes all the time.

        with action_lock:
            finish_imposters(logs_path)
            log(logs_path, "Tried-for finishing the imposters game.", "GAME")
        time.sleep(10)  # Around the time it should take for the bot to be sent to the initializer screen again.


if __name__ == "__main__":

    log_session = LaminariaCore.get_formatted_date_now(formatting=2)
    logs_path = os.path.join(os.getcwd(), "logs", log_session + ".log")

    # Check if path exists, if not, make all folders and subfolders of it, and make the file.
    if not os.path.isfile(logs_path):
        os.makedirs(os.path.dirname(logs_path), exist_ok=True)
        open(logs_path, "w").close()

    try:
        start_bot(logs_path)

    except KeyboardInterrupt:
        # A KeyboardInterrupt error will always come up when you willingly close the bot.
        # This is due to the time.sleeps in the code.
        log(logs_path, "Bot closed.", "STOP")

    except BaseException as err:
        # Any other exception is to be logged as an error in the logs.
        log(logs_path, traceback.format_exc(), "ERROR")
