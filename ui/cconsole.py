# Copyright (c) 2011 by American Power Conversion. All Rights Reserved.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appear in all copies and that
# both that copyright notice and this permission notice appear in
# supporting documentation, and that the name of Vinay Sajip
# not be used in advertising or publicity pertaining to distribution
# of the software without specific, written prior permission.
"""cconsole - Config console window.

This module exports:

windowConfig()
"""
import os
import win32console
import ctypes.wintypes
from ctypes import windll

ENABLE_QUICK_EDIT_MODE = 0x40
ENABLE_EXTENDED_FLAGS = 0x80


def quick_edit_mode(turn_on=None):
    """ Enable/Disable windows console Quick Edit Mode """
    screen_buffer = win32console.GetStdHandle(-10)
    orig_mode = screen_buffer.GetConsoleMode()
    is_on = (orig_mode & ENABLE_QUICK_EDIT_MODE)
    if is_on != turn_on and turn_on is not None:
        if turn_on:
            new_mode = orig_mode | ENABLE_QUICK_EDIT_MODE
        else:
            new_mode = orig_mode & ~ENABLE_QUICK_EDIT_MODE
        screen_buffer.SetConsoleMode(new_mode | ENABLE_EXTENDED_FLAGS)

    return is_on if turn_on is None else turn_on


def windowConfig(width, height, line_buffer):
    """a function to config console window size and buffer"""
    window_size = ("mode con cols="+str(width)+" lines="+str(height))
    os.system(window_size)
    STDOUT = -12
    hdl = windll.kernel32.GetStdHandle(STDOUT)
    bufsize = ctypes.wintypes._COORD(width, line_buffer) # rows, columns
    windll.kernel32.SetConsoleScreenBufferSize(hdl, bufsize)


if __name__ == '__main__':
    windowConfig(100, 40, 300) # width, height, line_buffer
    quick_edit_mode(False)
    print("Hello World")
    os.system('pause')