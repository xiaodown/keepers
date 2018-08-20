#!/usr/bin/python

# Checks knife status using the command line output
# Will Dunn / CC BY

from __future__ import print_function
import argparse
import time
import sys
import json
import subprocess


parser = argparse.ArgumentParser(description='Check knife status, alert based on time since run')
parser.add_argument('--testfile', help='use json-formatted TESTFILE rather than actually querying knife status', required=False)
requiredargs = parser.add_argument_group('required arguments')
requiredargs.add_argument('-w', '--warning', metavar='WARN', dest='warning', type=int, help='Warning condition, in minutes', required=True)
requiredargs.add_argument('-c', '--critical', metavar='CRIT', dest='critical', type=int, help='Critical condition, in minutes', required=True)

if len(sys.argv) == 1:
    print()
    parser.print_help()
    exit(0)

args = parser.parse_args()

if args.testfile is None:
    generatedcmd = "knife status -F j"
else:
    generatedcmd = "cat "+args.testfile

kstatus = json.loads(subprocess.Popen(generatedcmd, stdout=subprocess.PIPE, shell=True).stdout.read().decode())

i = 0
status = 0
badservers = {}

while i <= len(kstatus) - 1:
    if kstatus[i]['ohai_time'] < time.time() - (args.warning * 60):
        badservers[kstatus[i]['name']] = str(int(int(time.time() - kstatus[i]['ohai_time']) / 60))+"m"
        status = max(1, status)
    if kstatus[i]['ohai_time'] < time.time() - (args.critical * 60):
        status = 2
    i += 1

sortedbad = list(badservers.items())
sortedbad.sort()
if status >= 1:
    if status == 1:
        print("WARNING: chef-client fail: ", end='')
    if status == 2:
        print("CRITICAL: chef-client fail: ", end='')
    for name, time in sortedbad:
        print(name, time, "|", end='')
    print()

exit(status)
