#!/usr/bin/env python

import datetime
import json

# Find a string between to substrings.
# @param string s
# @param string first
# @param string last
# @returns string
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

# Find between last occurence.
# @param string s
# @param string first
# @param string last
# @returns string
def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""

# Find the date for the first Monday after a given a date.
# @param string d
# @param integer weekday
# @returns string
def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

# Write file to disk.
# @param string path
# @param string contents
# @param string mode
# @returns boolean
def writeFile( path, contents, mode ):
    f = open(path, mode)
    f.write(contents)
    f.close()
    return True

# Our customised JSON dumps configuration.
# @param list | dict
# @returns string
def toJson( obj ):
    return json.dumps(obj, ensure_ascii=False, sort_keys=False, indent=2, separators=(",", ": "))

# Determine the day of the appointment
# by comparing it's left offset.
# @param string left
# @returns string
def determine_day( left ):

    m = 10
    avg1 = 180
    avg2 = 290
    avg3 = 413
    avg4 = 552
    avg5 = 680

    pos = int(left)

    if pos <= avg1+m and pos >= avg1-m:
        return 0 # monday

    if pos <= avg2+m and pos >= avg2-m:
        return 1 # tuesday

    if pos <= avg3+m and pos >= avg3-m:
        return 2 # wednesday

    if pos <= avg4+m and pos >= avg4-m:
        return 3 # thursday

    if pos <= avg5+m and pos >= avg5-m:
        return 4 # friday

    return False

# Determine the schoolhour of the appointment
# by comparing it's top offset.
# @param string top
# @returns integer
def determine_hour( top ):

    ##############                                               ##############
    #                        turfgetallen            gemiddelde  verschil     #
    # uur 0 (8.00-9.00)      ?                                                #
    # uur 1 (9.00-10.00)     188 en 190px            189         ?            #
    # uur 2 (10.00-11.00)    223, 221, 224, 222px    222,5       33,5         #
    # uur 3 (11.15-12.15)    259, 261, 260, 258px    259,5       37           #
    # uur 4 (12.15-13.15)    306, 303, 304,          304,3                    #
    # uur 5 (13.45-14.45)    340, 341, 339,          340                      #
    # uur 6 (14.45-15.45)    377, 374, 376,          375,6                    #
    # uur 7 (16.00-17.00)    413, 412,               412,5                    #
    # uur 8 (17.00-18.00)    447                                              #
    ###########################################################################

    # We kunnen stellen dat de positie van een uur niet meer dan
    # 10px afwijkt van zijn soort's gemiddelde. Dus als een top tussen
    # 170px en 200px ligt, weten we zeker dat het een eerste lesuur is.
    # En als een top tussen 210 en 230, dat het een tweede lesuur is.
    # En als een top tussen 250 en 270, dat het een derde lesuur is, etc etc..

    m      = 10  # margin
    avg1   = 189 # ~ 190
    avg2   = 223 # ~ 220
    avg3   = 260 # ~ 260
    avg4   = 304 # ~ 300
    avg5   = 340 # ~ 340
    avg6   = 376 # ~ 380
    avg7   = 413 # ~ 410
    avg8   = 435 # not enough data points.

    pos = int(top)

    if pos <= avg1+m and pos >= avg1-m:
        return 1

    if pos <= avg2+m and pos >= avg2-m:
        return 2

    if pos <= avg3+m and pos >= avg3-m:
        return 3

    if pos <= avg4+m and pos >= avg4-m:
        return 4;

    if pos <= avg5+m and pos >= avg5-m:
        return 5;

    if pos <= avg6+m and pos >= avg6-m:
        return 6;

    if pos <= avg7+m and pos >= avg7-m:
        return 7;

    if pos <= avg8+m and pos >= avg8-m:
        return 8;

    if pos <= 0 and pos >= 0:
        return 0;

    return False
