# -*- coding: utf-8 -*-
# Created at 15/12/2021
__author__ = "MrKelpy / Alexandre Silva"
__github__ = "github.com/MrKelpy"
__copyright__ = "© Alexandre Silva 2021"
__license__ = "MIT LICENSE"

# Local Application Imports
import LaminariaCore

def log(logs_path: str, msg: str, src: str):
    """
    Logs a message to both the console and the logs file via a very simple
    logging system.
    :param: src -> Where the log is coming from
    :return:
    """

    with open(logs_path, "a") as logsfile:
        logsfile.write(f"[{LaminariaCore.get_formatted_date_now(include_seconds=True)}][IFXG][{src}] {msg}\n")

    print(f"[IFXG][{src}] {msg}")