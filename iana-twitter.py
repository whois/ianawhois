#!/usr/bin/python

import os
import sys
import string
import encodings.idna

# http://github.com/joshthecoder/tweepy
import tweepy
# http://code.google.com/p/python-bitly/
import bitly

authfile = "/home/bortzmeyer/.twitter/auth-ianawhois"
iana_base_url = "http://www.iana.org/domains/root/db"
vcs_url = "https://viewvc.generic-nic.net/viewvc.cgi/NIC-generique/iana/whois/%s?root=R%%26D&r1=%i&r2=%i"
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
bitly_login = authdata.readline()[:-1]
bitly_key = authdata.readline()[:-1]
if not bitly_key: 
    raise Exception("Cannot read all the auth. material in %s: not enough lines" % authfile)
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
    revision2 = int(log[0]['revision'].number)
    revision1 = int(log[1]['revision'].number)
    actual_vcs_url = (vcs_url % (btld, revision1, revision2))
    actual_iana_url = ("%s/%s.html" % (iana_base_url, ltld))
    bitly_api = bitly.Api(login=bitly_login, apikey=bitly_key) 
    actual_vcs_url_short = bitly_api.shorten(actual_vcs_url)
    actual_iana_url_short = bitly_api.shorten(actual_iana_url)
    urls = "Changes: %s New states: %s" % \
        (actual_vcs_url_short, actual_iana_url_short)
else:
    urls = "%s/%s.html" % (iana_base_url, ltld)
    # No need to shorten it
if ltld[0:4] == "xn--":
    utld = encodings.idna.ToUnicode(ltld)
    tld = "%s (%s)" % (utld, tld)
tmpl = string.Template(msg)
expanded_msg = tmpl.substitute(tld=tld)
if not debug:
    status = api.update_status("IANA whois: %s %s" % (expanded_msg, urls))
else:
    print "IANA whois: %s %s" % (expanded_msg, urls)
