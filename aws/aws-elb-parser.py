#!/usr/bin/env python

# script that prints out info about your AWS load balancers

import sys
import json
import argparse

parser = argparse.ArgumentParser(description='Outputs a list of elbs with associated rules')
parser.add_argument('--datafile', help='use json-formatted file rather than stdin', required=False)

args = parser.parse_args()

if len(sys.argv) == 1:
    if not sys.stdin.isatty():
        awsdata=json.load(sys.stdin)
    else:
        print
        parser.print_help()
        exit(0)
else:
    awsdata=json.load(open(args.datafile))

print "VPC,Name,Scheme,Subnet,type,DNS"

for elb in awsdata['LoadBalancers']:
    vpc = elb['VpcId'].strip()
    commonname = elb['LoadBalancerName'].strip()
    scheme = elb['Scheme'].strip()
    for az in elb['AvailabilityZones']:
        subnet = az['SubnetId']
    lbtype = elb['Type']
    dns = elb['DNSName']
    dnsname = dns.split(".", 1)[0]

    print vpc + "," + commonname + "," + scheme + "," + subnet + "," + lbtype + "," + dnsname

