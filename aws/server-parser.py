#!/usr/bin/env python

# script that prints out info about your AWS instances

import sys
import json
import argparse

parser = argparse.ArgumentParser(description='Outputs a list of AWS instances with type/region/status')
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

class server:
    def __init__(self,InstanceId,InstanceType,Subnet,IPAddress,AvailabilityZone,CommonName,Status,VpcId):
        self.InstanceId = InstanceId
        self.InstanceType = InstanceType
        self.Subnet = Subnet
        self.IP = IPAddress
        self.AvailabilityZone = AvailabilityZone
        self.CommonName = CommonName
        self.Status = Status
        self.VpcId = VpcId

    def displayCSV(self):
        print self.CommonName + "," + self.InstanceId + "," + self.InstanceType + "," + self.Subnet + "," + self.IP + "," + self.AvailabilityZone + "," + self.VpcId + "," + self.Status

    def display(self):
        print self.CommonName, "    ", self.InstanceId, "   ", self.InstanceType, " ", self.AvailabilityZone, " ", self.Status

servers = []
for reservation in awsdata['Reservations']:
    for instance in reservation['Instances']:
        status = instance['State']['Name']
        if status == "terminated":
            continue
        instance_id = instance['InstanceId']
        common_name = ""
        try:
            for tag in instance['Tags']:
                if tag['Key'] == "Name":
                    common_name = tag['Value']
        except:
            common_name = instance_id
        if not common_name:
            common_name = instance_id
        instance_type = instance['InstanceType']
        subnet = instance['SubnetId']
        vpc = instance['VpcId']
        ip = instance['PrivateIpAddress']
        availability_zone = instance['Placement']['AvailabilityZone']
        status = instance['State']['Name']

        servers.append(server(instance_id,instance_type,subnet,ip,availability_zone,common_name,status,vpc))

for server in servers:
    server.displayCSV()

