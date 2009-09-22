#!/usr/bin/python

import os
import sys
import twitter

authfile = "/home/bortzmeyer/.twitter/auth"
base_url = "http://www.iana.org/domains/root/db"

if len(sys.argv) != 3:
    print >>sys.stderr, ("Usage: %s TLD message" % sys.argv[0])
    sys.exit(1)

if not os.path.exists(authfile):
    print >>sys.stderr, ("Cannot find %s" % authfile)
    sys.exit(1)

tld = sys.argv[1]
msg = sys.argv[1]
auth = open(authfile)
login = auth.readline()[:-1]
passwd = auth.readline()[:-1]
api = twitter.Api(username=login, password=passwd) 
url = "%s/%s.html" % (base_url, tld.lower())
status = api.PostUpdate("IANA whois: %s %s" % (msg, url))

