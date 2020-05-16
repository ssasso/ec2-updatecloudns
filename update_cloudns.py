#!/usr/bin/python

API_ID='1111'
API_PASSWORD='xxxxxxx'
D='rfc2821.it'
H='moose'

import sys
import requests
import json
import cloudnsapi

# Login to ClouDNS
a = cloudnsapi.api(API_ID, API_PASSWORD)
print "Test Login:"
print a.test_login()

# Get Current EC2 Hostname
response = requests.get('http://169.254.169.254/latest/meta-data/public-hostname')
hostname = response.text

print "Public Hostname: %s" % hostname
print "DNS H.D: %s.%s" % (H, D)

# Work on ClouDNS
# search for record id
records = a.records(D)

record_id = ''

for rid in records.keys():
        host = records[rid]['host']
        rtype = records[rid]['type']
        if (rtype == 'CNAME' and host == H):
                print "Fount CNAME record '%s' with ID %s" % (host, rid)
                record_id = str(rid)

if record_id == '':
        print "Record not found."
        sys.exit(1)

print "Doing update for ID %s" % record_id

print "Operation Result:"
print a.mod_record(D, record_id, H, hostname, 300)
