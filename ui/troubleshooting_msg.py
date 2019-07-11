
# Copyright (c) 2011 by American Power Conversion. All Rights Reserved.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appear in all copies and that
# both that copyright notice and this permission notice appear in
# supporting documentation, and that the name of Vinay Sajip
# not be used in advertising or publicity pertaining to distribution
# of the software without specific, written prior permission.

"""troubleshooting_msg.py - Manage all troubleshooting information for upgrade tool

PLEASE only create new troubleshooting item through troubleshooting_msg.xlsx and
use build_troubleshooting_msg.py to generate this file automatically.
"""

#list sequence
_NUMBER = 0
_LEVEL = 1
_MESSAGE = 2

 #  errorCode                    list :[number,  level,      , message]
TROUBLESHOOT_INFO_TABLE = {
   "Bad AC power"                     :[ 0   , "INVALID"    , """Bad AC power is detected. 
Please make sure that the input power is available."""],
   "Not STANDBY mode"                 :[ 1   , "INVALID"    , """Your UPS is in operation.
Please turn off the UPS and any connected equipment."""],
   "UPS is not found"                 :[ 2   , "FAIL"       , """Cannot find any compatible APC UPS.
Please connect UPS to the computer via USB cable.
If USB cable is connected, RESTART your UPS and then try again."""],
   "More than one APC UPS"            :[ 3   , "FAIL"       , """More than one UPSs are found.
Please connect only 1 UPS to upgrade firmware."""],
   "Enter DFU fail"                   :[ 4   , "FAIL"       , """Battery may be low capacity.
For chargeing UPS battery capacity,
Please connect UPS to avaliable AC power at least 24 hours.
Then, try again."""],
   "Found at least one DFU device"    :[ 5   , "INVALID"    , """Find at least one or more unknown device.
It might influence upgrade process,
please remove it from USB on PC and connect only 1 UPS to upgrade firmware."""],
   "Found more than one DFU device"   :[ 6   , "INVALID"    , """Find more than one unknown device.
It might influence upgrade process,
please remove it from USB on PC and connect only 1 UPS to upgrade firmware."""],
   "Driver setup fail"                :[ 7   , "FAIL"       , """Driver setup fail.
Try again, please.

When the driver install window showed up,
please select

--[ Install this driver software anyway ]--"""],
   "GREEN_STANDBY or weak aux-charger":[ 8   , "INVALID"    , """First, make sure battery is connected.
Second, the UPS might be in sleep mode, please turn on the UPS by button and then turn off it. 
Next, try again."""],
   "Up to date firmware"              :[ 9   , "INVALID"    , """Your firmware is already up to date."""                            ],
   "Wrong sku"                        :[ 10  , "INVALID"    , """Sku is wrong, please use applicable UPS.
If sku is literally applicable to this utility, please replug usb data port or 
restart your PC, then try again."""],
   "Old fw version"                   :[ 11  , "FAIL"       , """Firmware is still old version."""                                  ],
   "Unknown error"                    :[ 12  , "FAIL"       , """An unexpected error occurred.
Please read welcome message carefully, ensure the UPS status and environment
setup are valid to upgrade.

After that, you could try again."""],
   "RESTART procedure"                :[ 13  , "NONE"       , """----------------------------------------------------------------------
|   RESTART procedure :                                                |
|   -Step1. Unplug the UPS power cord from AC outlet at least 5 sec.   |
|   -Step2. Replug it back.                                            |
|   -Done.                                                             |
 ----------------------------------------------------------------------"""],
   "PC OS is not applicable"          :[ 14  , "INVALID"    , """Your PC oprating system is not applicable."""                      ],
   "Pywinusb open device fail"        :[ 15  , "FAIL"       , """USB message is incomplete. 
Please confirm that connect UPS data port directly to USB on PC; not a USB hub.

Next, try again."""],
   "Visual C++ environment bad"       :[ 16  , "FAIL"       , """"Entry Point Not Found error"
A corruptive Visual C++ run-time environment is detected.
This PC might be shutdown abnormally or effected by malware once.
Technically, it is not an issue coming from the firmware upgrade utility.
However, you could install run-time components by the Visual C++ Redistributable
Packages released by Microsoft to solve this problem.

Detail please view troubleshooting of attached documentation."""],
}
