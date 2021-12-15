# -*- coding: utf-8 -*-
# Created at 15/12/2021
__author__ = "MrKelpy / Alexandre Silva"
__github__ = "github.com/MrKelpy"
__copyright__ = "© Alexandre Silva 2021"
__license__ = "MIT LICENSE"

# Third-Party imports
import pygetwindow


def focus_fortnite():
    """
    Hands over the window focus to the fornite screen.
    :return:
    """
    ft_window = [x for x in pygetwindow.getAllWindows() if x.title.strip() == "Fortnite"][0]
    ft_window.activate()
