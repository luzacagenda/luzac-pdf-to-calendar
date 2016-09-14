#!/usr/bin/env python

# Find between.
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

# Find between last occurence.
def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""

def determine_day( top ):

    m = 10
    avg1 = 180
    avg2 = 290
    avg3 = 413
    avg4 = 552
    avg5 = 680

    pos = int(top)

    if pos <= avg1+m and pos >= avg1-m:
        return "ma"

    if pos <= avg2+m and pos >= avg2-m:
        return "di"

    if pos <= avg3+m and pos >= avg3-m:
        return "wo"

    if pos <= avg4+m and pos >= avg4-m:
        return "do"

    if pos <= avg5+m and pos >= avg5-m:
        return "vr"

    return False

def determine_hour( left ):


    #                                   turfgetallen            gemiddelde  verschil
    # uur 0 (8.00-9.00) begint rond     ?
    # uur 1 (9.00-10.00) zit tussen     188 en 190px            189         diff ?
    # uur 2 (10.15-11.15) zit tussen    223, 221, 224, 222px    222,5       diff 33,5
    # uur 3 (11.15-12.15) zit tussen    259, 261, 260, 258px    259,5       diff 37
    # uur 4 (12.15-13.15) zit tussen    306, 303, 304,          304,3
    # uur 5 (13.45-14.45) zit tussen    340, 341, 339,          340
    # uur 6 (14.45-15.45) zit tussen    377, 374, 376,          375,6
    # uur 7 (16.00-17.00) zit tussen    413, 412,               412,5
    # uur 8 (17.00-18.00) zit tussen    ?

    # we kunnen stellen dat een uur niet meer dan 10px afwijkt van zijn gemiddelde.
    # dus als top tussen 170 en 200 ligt, weten we zeker dat het een eerste lesuur is.
    # en als een top tussen 210 en 230, dat het een tweede lesuur is.
    # en als een top tussen 250 en 270, dat het een derde lesuur is.

    m      = 10  # margin
    avg1   = 189 # ~ 190
    avg2   = 223 # ~ 220
    avg3   = 260 # ~ 260
    avg4   = 304 # ~ 300
    avg5   = 340 # ~ 340
    avg6   = 376 # ~ 380
    avg7   = 413 # ~ 410

    pos = int(left)

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
