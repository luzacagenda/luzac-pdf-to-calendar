#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Luzac Rooster PDF to Google Calendar
# Developed by Sander Laarhoven (c) 2016
# Licensed under the MIT License
# https://git.io/luzac

# Import required default modules.

import sys
import os.path
import subprocess
import json
import datetime

# Import our files.
import library
import googlelib

# Script Constants.
__version__         = "1.3.0"
__timezone__        = "Europe/Amsterdam"
__calendar__        = "primary"
__debugMode__       = True
__scopes__          = "https://www.googleapis.com/auth/calendar"
__client_secret__   = "client_secret.json"

# Schoolhour times. All classes last one hour (60mins).
schoolHours = [ ["8", "00"], ["9", "00"], ["10", "00"], ["11", "15"],
                ["12", "15"], ["13", "45"], ["14", "45"], ["16", "00"],
                ["17", "00"] ]

# Let's get this party started.
print "\n"
print "    Luzac Rooster PDF to Google Calendar"
print "    version "+__version__+" - https://git.io/luzac"
print "\n"

# ========================================== #
#          1. Convert the PDF to JSON.
# ========================================== #

# Is the pdf2txt module available?
try:
    import pdfminer
except ImportError, error:
    print "[!] Required module pdfminer is not installed."
    sys.exit()

# Did we get a PDF file and student number?
if len(sys.argv) < 3:
    print "[!] No PDF file or student number provided as parameter."
    sys.exit()

# Our pdf file is the first argument.
pdfFile = sys.argv[2]
studentNumber = sys.argv[1]

# Make sure the file exists.
if not os.path.isfile(pdfFile):
    print "[!] Could not find file "+pdfFile+"."
    sys.exit()

# We've got our file.
print "[*] PDF file: "+pdfFile+"."

# Run pdfminer.
print "[*] PDFMiner is starting HTML extraction.."
command = 'pdf2txt.py -t html -p '+studentNumber+' -o output-'+studentNumber+'.html '+pdfFile
p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

# Wait for output.
print "[*] Waiting for PDFMiner to finish.."
(output, err) = p.communicate()
status = p.wait()

# What was the result?
print "[*] PDFMiner exited with status/error: ", status, "/", err

# Set the data list.
data = {}
data['rooster'] = []
n = 0

# Parse all lines.
print "[*] Parsing output file."
with open("output-"+studentNumber+".html") as f:

    for line in f:

        n = n + 1

        if "Naam Leerling" in line:
            data['type'] = 'student'
            data['name'] = line.split(">:", 1)[1].strip()
            print "[*] Name of student is "+data['name']
            continue

        if "Naam docent" in line:
            data['type'] = 'teacher'
            data['name'] = line.split(">:", 1)[1].strip()
            print "[*] Name of teacher is "+data['name']
            # teachers do not have week numbers.
            data['week'] = '9001'
            continue

        if "WEEKROOSTER" in line:
            data['week'] = line.rpartition(">")[-1].strip()
            print "[*] Week number is "+data['week']
            continue

        if "Datum" in line:
            data['date'] = line.rpartition(">")[-1].strip()
            print "[*] Date is "+data['date']
            continue

        if "lokaal" in line:
            classroom = line.rpartition(":")[-1].strip()
            data['rooster'][len(data['rooster'])-1]['classroom'] = classroom
            continue

        if "dag" in line:
            # ignore.
            continue

        if "uur" in line:
            # ignore.
            continue

        if "Persoonlijk rooster" in line:
            # ignore.
            continue

        if "textbox" in line:
            subject = line.rpartition(">")[-1].strip()
            top = library.find_between(line, "top:", "px;")
            left = library.find_between(line, "left:", "px;")
            hour = library.determine_hour(data['type'], top)
            startTime = schoolHours[hour]
            day = library.determine_day(data['type'], left)
            data['rooster'].append({"subject": subject, "hour": hour,
                                    "startTime": startTime, "day": day})
            continue

# Did we actually parse anything?
print "[*] Parsed "+str(n)+" lines."
if n == 0:
    print "[!] Got 0 lines from PDFMiner, something went wrong."
    sys.exit()

# Dump to JSON.
jsonData = library.toJson(data)
library.writeFile("rooster-"+studentNumber+".json", jsonData, "w")
print "[*] Wrote JSON to disk."

# Did we determine the type of user?
if not data['type']:
    print "[!] Could not determine type of user."
    sys.exit()
else:
    print "[*] User is a "+data['type']

# =============================================== #
#    2. Convert JSON to Google Calendar events.
# =============================================== #

# Get the next monday from the date when the PDF was sent.
# The sent date is in d-m-yyyy format,
# the returned date is in yyyy-mm-dd format.
parts = data['date'].split("-")
date = datetime.date(int(parts[2]), int(parts[1]), int(parts[0]))
nextMonday = library.next_weekday(date, 0)
print "[*] The next monday is at", nextMonday

# Loop through all appointments and convert them
# into Google Calendar event objects.
events = []
for appointmentIndex, appointmentData in enumerate(data['rooster']):

    print "\r[*] Converting appointment " + str(appointmentIndex+1) + "/" + str(len(data['rooster'])),

    # Only parse valid days.
    day = appointmentData['day']
    if str(day) != "0" and day == False:
        print "[!] Could not determine date of appointment, day is False."
        continue

    # Determine the appointment date.
    if str(day) == "0":
        appointmentDate = nextMonday
    else:
        appointmentDate = library.next_weekday(nextMonday, day)
    #print "    Date: ("+str(day)+")", appointmentDate

    # Determine the start time of the appointment.
    hours = int(appointmentData['startTime'][0])
    minutes = int(appointmentData['startTime'][1])
    appointmentStart = datetime.datetime.combine( appointmentDate, datetime.time(hours, minutes) )

    # Determine the end time of the appointment.
    appointmentEnd = appointmentStart + datetime.timedelta(hours = 1)

    # Do we have a location?
    if not 'classroom' in appointmentData:
        appointmentData['classroom'] = "onbekend"

    # Construct the event object.
    events.append({
        "summary": "["+str(appointmentData['hour'])+"] "+appointmentData['subject'],
        "location": "Lokaal "+appointmentData['classroom'],
        "description": "",
        "start": {
            "dateTime": appointmentStart.isoformat(),
            "timeZone": __timezone__
        },
        "end": {
            "dateTime": appointmentEnd.isoformat(),
            "timeZone": __timezone__
        },
        "reminders": {
            "useDefault": False,
            "overrides": [
                { "method": "popup", "minutes": 5 }
            ]
        }
    })

    pass

# Save this to disk.
jsonEvents = library.toJson(events)
library.writeFile("events-"+studentNumber+".json", jsonEvents, "w")

# Obtain credentials with Google OAuth2.
#googlelib.test(__client_secret__, __scopes__, __calendar__)

print "\n[*] Ready to start adding events to calendar.";
raw_input("    Press ENTER to continue..\n");
for eventIndex, eventData in enumerate(events):
    googlelib.addEvent(eventIndex, eventData, __client_secret__, __scopes__, __calendar__)
    pass
