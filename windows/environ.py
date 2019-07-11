# Copyright (c) 2011 by American Power Conversion. All Rights Reserved.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appear in all copies and that
# both that copyright notice and this permission notice appear in
# supporting documentation, and that the name of Vinay Sajip
# not be used in advertising or publicity pertaining to distribution
# of the software without specific, written prior permission.

"""environ  - Environment information of PC operating system

This module exports:
-OsEnviron : Detect operating system is valid or not
"""

import re
import platform

WINDOWS_XP  = "Windows XP"
WINDOWS_7   = "Windows 7"
WINDOWS_8   = "Windows 8"
WINDOWS_8_1 = "Windows 8.1"
WINDOWS_10  = "Windows 10"

# Support Windows 7, 8, 10
_TARGET_WINDOWS_RELEASE = {
#    "XP"     : WINDOWS_XP,
    "7"      : WINDOWS_7,
    "8"      : WINDOWS_8,
    "8.1"    : WINDOWS_8_1,
    "post8.1": WINDOWS_8_1,
    "10"     : WINDOWS_10,
    "post10" : WINDOWS_10
}


def isMicrosoftWindows():
    if re.search("Windows", platform.system()):
        return True
    else:
        return False

def isTargetWindowsRelease():
    target_release_list = list(_TARGET_WINDOWS_RELEASE.keys())
    if isMicrosoftWindows():
        # Get system release info
        windows = platform.release()
        # Compare with target list
        for target_release in target_release_list:
            if windows == target_release:
                return True
    return False

def getWindowsRelease():
    windows = None
    if isTargetWindowsRelease():
        windows = _TARGET_WINDOWS_RELEASE[platform.release()]
    return windows

def is64bit():
    if platform.machine().endswith('64'):
        return True
    else:
        return False

def isApplicableOs():
    if (isMicrosoftWindows()) and (isTargetWindowsRelease()):
        return True
    else:
        return False

def getOsInformation():
    if is64bit():
        sys_type = "64bit"
    else:
        sys_type = "32bit"
    ret_val = str(platform.system()+" "+platform.release()+"\n"+sys_type)
    return ret_val

if __name__ == '__main__':
    print(getOsInformation())