#!/usr/bin/python

# An NRPE script (i.e. prints out OK/WARN/CRIT)
# Checks the number of messages in a queue
#
# requires: rabbitmq_management plugin
# note: python 2.x not 3.x currently
#
# Will Dunn / CC BY
#
# example usage for NRPE (maybe for checking dead letter queues):
# check_queue_count.py -n -w 2 -c 4 -v vhost1 -q queue1 -u user -p pass
# example for just checking messages in a queue
# (assumes localhost, 15672, and guest/guest
# check_queue_count.py -v vhost1 -q queue1


import argparse
import requests
import sys
sys.excepthook = sys.__excepthook__


parser = argparse.ArgumentParser(description='Check and alert based on number of messages in a queue')

parser.add_argument('--host',
                    metavar='HOST',
                    dest='host',
                    required=False,
                    default='localhost',
                    help='Hostname of the RabbitMQ server, defaults to localhost')

parser.add_argument('--port',
                    metavar='PORT',
                    dest='port',
                    required=False,
                    default='15672',
                    help='Port for the rabbitmqadmin HTTP interface, defaults to 15672')

parser.add_argument('-u', '--user',
                    metavar='USER',
                    dest='username',
                    required=False,
                    default='guest',
                    help='Username for the admin interface, defaults to guest')

parser.add_argument('-p', '--pass',
                    metavar='PASS',
                    dest='password',
                    required=False,
                    default='guest',
                    help='Password for the admin interface, defaults to guest')

parser.add_argument('-n', '--nrpe',
                    dest='nrpe',
                    required=False,
                    default=False,
                    action='store_true',
                    help='Use this flag to behave like NRPE expects, default false')

parser.add_argument('-w', '--warning',
                    metavar='WARN',
                    dest='warning',
                    required=False,
                    default=1,
                    type=int,
                    help='Number of messages for warning')

parser.add_argument('-c', '--critical',
                    metavar='CRIT',
                    dest='critical',
                    required=False,
                    default=10,
                    type=int,
                    help='Number of messages for critical')

requiredargs = parser.add_argument_group('required arguments')

requiredargs.add_argument('-v', '--vhost',
                          metavar='VHOST',
                          dest='vhost',
                          required=True,
                          help='RabbitMQ Vhost')

requiredargs.add_argument('-q', '--queue',
                          metavar='QUEUE',
                          dest='queue',
                          required=True,
                          help='RabbitMQ Queue in the specified vhost')

args = parser.parse_args()

if len(sys.argv) == 1:
    print
    parser.print_help()
    exit(0)


querystring = "http://" + args.host + ":" + args.port + "/api/queues/" + args.vhost + "/" + args.queue

r = requests.get(querystring, auth=(args.username, args.password))
try:
    r.raise_for_status()
except requests.exceptions.HTTPError as e:
    print "UNKNOWN: HTTP error " + str(e.response.status_code)
    exit(3)

num_messages = r.json()['messages']

if args.nrpe:
    status = 0
    if num_messages >= args.warning:
        if num_messages >= args.critical:
            status = 2
            print "CRITICAL: " + str(num_messages) + " in " + args.vhost + "/" + args.queue
        else:
            status = 1
            print "WARNING: " + str(num_messages) + " in " + args.vhost + "/" + args.queue
    else:
        print "OK: " + str(num_messages) + " in " + args.vhost + "/" + args.queue
    exit(status)
else:
    print num_messages


