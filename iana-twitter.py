#!/usr/bin/python

import os
import sys
import twitter

authfile = "/home/bortzmeyer/.twitter/auth"

if len(sys.argv) != 2:
    print >>sys.stderr, ("Usage: %s message" % sys.argv[0])
    sys.exit(1)

if not os.path.exists(authfile):
    print >>sys.stderr, ("Cannot find %s" % authfile)
    sys.exit(1)

msg = sys.argv[1]
auth = open(authfile)
login = auth.readline()[:-1]
passwd = auth.readline()[:-1]
api = twitter.Api(username=login, password=passwd) 
status = api.PostUpdate("IANA whois: %s" % msg)
