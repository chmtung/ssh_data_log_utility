# This file contains the template text for output file content. In the template
# test you see %s sprinkled all over the place. Those are the location where
# we replace those with auto generation code.


#///////////////////////////////////////////////////////////////////////////////
# For output file
#///////////////////////////////////////////////////////////////////////////////
FILENAME_TROUBLESHOOT_MSG = "troubleshooting_msg.py"

TROUBLESHOOT_DICTIONARY_DEF = \
'''   %(errorCode)-35s:[ %(number)-4s, %(level)-13s, %(message)-70s],
'''

TROUBLESHOOT_MSG_TEMPLATE = \
'''
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
%s}
'''
