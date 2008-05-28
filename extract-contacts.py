#!/usr/bin/python

# $Id: extract-contacts.py,v 1.1 2003-10-21 08:51:14 bortzmeyer Exp $

import sys
import re
import os

files = os.listdir(".")
tlds = []
for file in files:
    if re.search ("^[A-Z]{2}$", file):
        tlds.append (file)
for tld in tlds:
    #sys.stderr.write ("Extracting info for %s...\n" % tld)
    file = open (tld)
    mode = 0
    line = file.readline()
    print tld ,
    while line:
        match = re.search ("^ *Name: *(.*)$", line)
        if match:
            name = match.group(1)
            if name: # Many empty records
                mode = 1
                name = re.sub (",", " ", name)
                name = re.sub (";", " ", name)
        match = re.search ("^ *Email: *(.*)$", line)
        if match:
            email = match.group (1)
            if email: # Many empty records
                if re.search ("/", email): # The IANA database does not allow
                    # multiple contacts but cheat by giving email addresses
                    # separated by a slash.
                    addresses = re.split ("/", email)
                    for address in addresses:
                        contact = name + ", " + address
                        print "; ", contact,
                else:
                    contact = name + ", " + email
                    print "; ", contact,
                mode = 0
        line = file.readline()
    file.close()
    print ""
