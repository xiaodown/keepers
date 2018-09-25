#!/usr/bin/env python

# script that prints out info about your AWS instances

import sys
import json
import argparse

parser = argparse.ArgumentParser(description='Outputs a list of ALCs with associated rules')
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

for acl in awsdata['NetworkAcls']:
    common_name = ""
    for tag in acl['Tags']:
        if tag['Key'] == "Name":
            common_name = tag['Value']
    inbound = False
    print "\n\nACL: ", acl['NetworkAclId'], " ", common_name
    print "\nOutbound rules:\n"
    for entry in acl['Entries']:
        if entry['Egress'] == False:
            if inbound == False:
                print "Inbound rules:\n"
                inbound = True
        proto = entry['Protocol']
        ports = False
        if proto == "-1":
            proto_common = "All"
        elif proto == "1":
            proto_common = "ICMP"
        elif proto == "6":
            proto_common = "TCP"
            ports = True
            port_low = entry['PortRange']['From']
            port_high = entry['PortRange']['To']
        elif proto == "17":
            proto_common = "UDP"
            ports = True
            port_low = entry['PortRange']['From']
            port_high = entry['PortRange']['To']
        action = entry['RuleAction']
        cidr = entry['CidrBlock']

        print "Rule #", entry['RuleNumber']
        print "Protocol: ", proto_common
        if ports == True:
            print "Port(s): ", port_low, "-", port_high
        if inbound == False:
            print "Destination: ", cidr
        elif inbound == True:
            print "Source: ", cidr
        print "Action: ", action
        print "Justification: "
        print "\n"




