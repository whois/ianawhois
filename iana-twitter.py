#!/usr/bin/python

import os
import sys
import string
import encodings.idna

# http://github.com/joshthecoder/tweepy
import tweepy

authfile = "/home/bortzmeyer/.twitter/auth-ianawhois"
base_url = "http://www.iana.org/domains/root/db"
vcs_url = "Change: https://viewvc.generic-nic.net/viewvc.cgi/NIC-generique/iana/whois/%s?root=R%%26D&r1=%i&r2=%i"
debug = False

if len(sys.argv) != 3:
    print >>sys.stderr, ("Usage: %s TLD message" % sys.argv[0])
    sys.exit(1)

if not os.path.exists(authfile):
    print >>sys.stderr, ("Cannot find %s" % authfile)
    sys.exit(1)

tld = sys.argv[1]
msg = sys.argv[2]
authdata = open(authfile)
consumer_key = authdata.readline()[:-1]
consumer_secret = authdata.readline()[:-1]
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
access_key = authdata.readline()[:-1]
access_secret = authdata.readline()[:-1]
authdata.close()
auth.set_access_token(access_key, access_secret)
if not debug:
    api = tweepy.API(auth)
ltld = tld.lower()
btld = tld.upper()
if string.split(msg)[0] == "update":
    import pysvn
    client = pysvn.Client()
    log = client.log("./%s" % btld)
    revision1 = int(log[0]['revision'].number)
    revision2 = int(log[1]['revision'].number)
    url = (vcs_url % (btld, revision1, revision2)) + "\n" + \
          ("New state: %s/%s.html" % (base_url, ltld))
else:
    url = "%s/%s.html" % (base_url, ltld)
if ltld[0:4] == "xn--":
    utld = encodings.idna.ToUnicode(ltld)
    tld = "%s (%s)" % (utld, tld)
tmpl = string.Template(msg)
expanded_msg = tmpl.substitute(tld=tld)
if not debug:
    status = api.update_status("IANA whois: %s %s" % (expanded_msg, url))
else:
    print "IANA whois: %s %s" % (expanded_msg, url)
