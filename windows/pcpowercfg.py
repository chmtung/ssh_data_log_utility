#!/usr/bin/env python
#!python

# Copyright (c) 2011 by American Power Conversion. All Rights Reserved.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appear in all copies and that
# both that copyright notice and this permission notice appear in
# supporting documentation, and that the name of Vinay Sajip
# not be used in advertising or publicity pertaining to distribution
# of the software without specific, written prior permission.

"""
Module: PC power plan config - Change PC power setting level by command line
                               for preventing unforeseen low battery shutdown via HID interface.
Class:  PowerPlan - Config or revert PC specific power plan
"""

import re
import subprocess
from windows import environ

_DO_NOTHING, _SLEEP, _HIBERNATE, _SHUTDOWN = [0, 1, 2, 3]

def _isEnvironmentValidToSetPowerPlan():
    valid_system = [environ.WINDOWS_7, environ.WINDOWS_8, environ.WINDOWS_8_1, environ.WINDOWS_10]
    if environ.getWindowsRelease() in valid_system:
        return True
    else:
        return False

def _readCommand(command):
    return str(subprocess.Popen(command,shell = True, stdout= subprocess.PIPE).communicate())

def _sendCommand(command):
    subprocess.Popen(command,shell = True)

def _searchPattern(pattern,text):
    p = re.compile(pattern)
    out = p.findall(text)
    return out[0]

class PowerPlan:
    def __init__(self):
        # About how to use "powercfg" command, please refer Microsoft website.
        self.prev_dc_value = None
        self.prev_ac_value = None

    def readBatteryPowerSetting(self):
        """ Query all battery setting of active power plan scheme ."""
        return _readCommand("powercfg -q"+" "+"SCHEME_CURRENT"+" "+"SUB_BATTERY")

    def getCritBattDCAct(self, qInfo):
        """ Get critical battery setting when PC is On-battery."""
        return int(_searchPattern("\(Critical battery action\).*?Current DC Power Setting Index: 0x(\d+)", qInfo))

    def getCritBattACAct(self, qInfo):
        """ Get critical battery setting when PC is Plugged-in."""
        return int(_searchPattern("\(Critical battery action\).*?Current AC Power Setting Index: 0x(\d+)", qInfo))

    def setCritBattDCAct(self, value):
        """ Set critical battery setting when PC is On-battery."""
        _sendCommand('powercfg -setdcvalueindex SCHEME_CURRENT SUB_BATTERY BATACTIONCRIT ' + str(value))

    def setCritBattACAct(self, value):
        """ Set critical battery setting when PC is Plugged-in."""
        _sendCommand('powercfg -setacvalueindex SCHEME_CURRENT SUB_BATTERY BATACTIONCRIT ' + str(value))

    def config(self):
        if _isEnvironmentValidToSetPowerPlan():
            qInfo = self.readBatteryPowerSetting()
            self.prev_dc_value = self.getCritBattDCAct(qInfo)
            self.prev_ac_value = self.getCritBattACAct(qInfo)
            self.setCritBattDCAct(_DO_NOTHING)
            self.setCritBattACAct(_DO_NOTHING)

    def revert(self):
        if _isEnvironmentValidToSetPowerPlan():
            self.setCritBattDCAct(self.prev_dc_value)
            self.setCritBattACAct(self.prev_ac_value)

def _test():
    # 1 search current active power mode
    pp = PowerPlan()
    pp.config()
    answer = input("Are you ready to continue? y/[n]:")
    if (answer is "Y") or (answer is "y"):
        pp.revert()

if __name__ == '__main__':
    _test()
