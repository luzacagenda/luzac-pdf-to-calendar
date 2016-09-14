#!/usr/bin/env python
import sys
import os.path
import subprocess
import json

import library

__version__ = "1.0.0"

print "    Luzac Rooster PDF to Calendar"
print "    version "+__version__
print "    https://git.io/luzac"

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
command = 'pdf2txt.py -t html -p '+studentNumber+' -o output-'+studentNumber+'.html '+pdfFile
p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

# Wait for output.
(output, err) = p.communicate()
status = p.wait()

# Save output.
print "[*] PDFMiner exited with status: ", status
f = open("output.html", "w")
f.write(output)
f.close()

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
            data['name'] = line.split(">:", 1)[1].strip()
            print "[*] Name of student is "+data['name']
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

        if "textbox" in line:
            title = line.rpartition(">")[-1].strip()
            top = library.find_between(line, "top:", "px;")
            left = library.find_between(line, "left:", "px;")
            hour = library.determine_hour(top)
            day = library.determine_day(left)
            data['rooster'].append({"title": title, "hour": hour, "day": day})
            continue

        #print line

print "[*] Parsed "+str(n)+" lines."

# Dump to JSON.
jsonData = json.dumps(data, ensure_ascii=False, sort_keys=False, indent=2, separators=(",", ": "))
f = open("rooster-"+studentNumber+".json", "w")
f.write(jsonData)
f.close()
print "[*] Wrote JSON to disk."
