# Copyright (c) 2011 by American Power Conversion. All Rights Reserved.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appear in all copies and that
# both that copyright notice and this permission notice appear in
# supporting documentation, and that the name of Vinay Sajip
# not be used in advertising or publicity pertaining to distribution
# of the software without specific, written prior permission.

"""ui - Display features.

This module exports:

Display - a class deal how to print massage to screen.
"""
import sys
import time
import textwrap
import ui.troubleshooting_msg as trbl

_INDENT_LEVEL_0 = 0  #white space left indent, = 0 tab
_INDENT_LEVEL_1 = 4  #white space left indent, = 1 tab
_INDENT_LEVEL_2 = 8  #white space left indent, = 2 tab
_INDENT_LEVEL_3 = 12 #white space left indent, = 3 tab

_INDENT_LEVEL = {
    "Lv0": _INDENT_LEVEL_0,
    "Lv1": _INDENT_LEVEL_1,
    "Lv2": _INDENT_LEVEL_2,
    "Lv3": _INDENT_LEVEL_3}


#---------------------------------------------------------------------------
#   Display with indent
#---------------------------------------------------------------------------
class DisplayIndent(object):

    _present_level = _INDENT_LEVEL_1
    _old_level = _INDENT_LEVEL_1

    def __init__(self):
        pass

    def printI(self, text, end='\n'):
        """ Print str with indent """
        print(textwrap.indent(text, (" " * DisplayIndent._present_level)), end=end)

    def returnI(self, text):
        """ Return str with indent """
        return textwrap.indent(text,(" " * DisplayIndent._present_level))

    def setIndent(self, level):
        """ Set with indent """
        if DisplayIndent._present_level != _INDENT_LEVEL[level]:
            DisplayIndent._old_level = DisplayIndent._present_level
            DisplayIndent._present_level = _INDENT_LEVEL[level]

    def revertIndentLevel(self):
        DisplayIndent._present_level = DisplayIndent._old_level

#---------------------------------------------------------------------------
#   Display for user interface
#---------------------------------------------------------------------------
class DisplayBoard(DisplayIndent):

    _registered = False
    _subject = None
    _pass_message = []
    _fail_message = []
    _troubleshoot_info = []
    _stopFlashingText = False

    def __init__(self):
        pass

    def cleanBuffer(self):
        DisplayBoard._subject = None
        DisplayBoard._pass_message = []
        DisplayBoard._fail_message = []
        DisplayBoard._troubleshoot_info = []

    def registerDisplayBoard(self, subject):
        DisplayBoard._registered = True
        self.cleanBuffer()
        DisplayBoard._subject = subject

    def removeDisplayBoard(self):
        DisplayBoard._registered = False
        self.cleanBuffer()

    def printI(self, text, end='\n'):
        """ If DisplayBoard register, do not print str with indent """
        if not DisplayBoard._registered:
            print(textwrap.indent(text, (" " * DisplayIndent._present_level)), end=end)

    def printIAnyway(self, text, end='\n'):
        """ No matter what DisplayBoard register or not, print str with indent anyway """
        print(textwrap.indent(text, (" " * DisplayIndent._present_level)), end=end)

    def logPassMsg(self, text):
        if DisplayBoard._registered:
            DisplayBoard._pass_message.append(text)

    def logFailMsg(self, text):
        if DisplayBoard._registered:
            DisplayBoard._fail_message.append(text)

    def logTroubleshooting(self, error_code):
        if DisplayBoard._registered:
            # 1. Get troubleshooting information by error_code.
            DisplayBoard._troubleshoot_info = trbl.TROUBLESHOOT_INFO_TABLE[error_code.strip()]
            # 2. Log corresponding fail message from troubleshooting info.
            self.logFailMsg(DisplayBoard._troubleshoot_info[trbl._MESSAGE])

    def printDisplayBoard(self, execute_status = False):
        issue_level = "FAIL"
        if DisplayBoard._troubleshoot_info and DisplayBoard._troubleshoot_info[trbl._LEVEL] != "NONE":
            issue_level = DisplayBoard._troubleshoot_info[trbl._LEVEL]

        sentence_end_point = 45
        if not DisplayBoard._registered:
            return
        DisplayBoard._registered = False
        dot_num = sentence_end_point - len(DisplayBoard._subject)
        subject_and_status = DisplayBoard._subject + (dot_num * ".")

        self.setIndent("Lv2")
        if execute_status:
            self.printI(subject_and_status + "PASS!")
            self.setIndent("Lv3")
            for i in DisplayBoard._pass_message:
                self.printI(i)
        else:
            self.printI(subject_and_status + issue_level + "!")
            self.setIndent("Lv3")
            for i in DisplayBoard._fail_message:
                self.printI(i)
        self.revertIndentLevel()
        print("")
        self.cleanBuffer()
        return execute_status

    def flashingOneLineText(self, msg, timeout=10):
        if len(msg.split()) > 1:
            raise ValueError('Invalid test, you should type only one line.')
        toggle = 0
        timeStart = time.time()
        while (1):
            time.sleep(1)
            if toggle % 2:
                sys.stdout.write("\r{}".format(msg))
            else:
                sys.stdout.write("\r{}".format(""))
            toggle += 1
            if time.time() > (timeStart + timeout) or self._stopFlashingText:
                break

    def stopflashingOneLineText(self):
        _stopFlashingText = True

def _test():
    tmp = DisplayBoard()
    tmp.flashingOneLineText("ABCDFG")
    time.sleep(3)
    tmp.stopflashingOneLineText()

if __name__ == '__main__':
    sys.exit(_test())