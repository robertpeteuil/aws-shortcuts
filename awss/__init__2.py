#!/usr/bin/env python

# awss - Control AWS instances from command line: list, start, stop or ssh
#
#       https://github.com/robertpeteuil/aws-shortcuts
#
#  Author: Robert Peteuil   @RobertPeteuil

from __future__ import print_function
from builtins import range
import argparse
import boto3
import sys
import subprocess
import os
from awss.colors import CLRnormal, CLRheading, CLRheading2, CLRtitle,\
    CLRwarning, CLRerror, statCLR
from awss.getchar import _Getch

__version__ = '0.9.4.2'


def main():

    getArguments()

# OLD MAIN BELOW HERE

    global debug
    global ec2C
    global ec2R
    global instanceAMIName
    instanceAMIName = {}

    # Setup AWS EC2 connections
    ec2C = boto3.client('ec2')
    ec2R = boto3.resource('ec2')

    (options) = getArguments()
    (actionType, filterType, filterType2, filters, OutputText, nopem,
     loginuser, debug) = decodeArguments(options)

    debugPrintOptions(actionType, filterType, filterType2, filters,
                      OutputText, nopem, loginuser)

    if actionType != "list" and filterType == "":
        print("%sError%s - instance identifier not specified" %
              (CLRerror, CLRnormal))
        sys.exit()

    instanceSummaryData = getSummaryData(filterType, filters)
    getInstanceIDs(instanceSummaryData)
    getInstanceDetails()

    performAction(actionType, filterType, filterType2, filters, OutputText,
                  nopem, loginuser)

    sys.exit()


def getArguments():
    parser = argparse.ArgumentParser(description="Control AWS instances from"
                                     " the command line with: list, start,"
                                     " stop or ssh.", prog='awss',
                                     usage="\tawss {command} ( 'NAME' or"
                                     " '-i ID' ) [ OPTIONS ]\n\t{command} ="
                                     " list | start | stop | ssh")
    parser.add_argument('-v', '--version', action="version",
                        version="awss {0}".format(__version__))

    subparsers = parser.add_subparsers(title="For additional help on"
                                       " command parameters", dest='command',
                                       description="type 'awss {command} -h',"
                                       " where {command} is: list, start,"
                                       " stop or ssh")

    # Parser for LIST command
    parser_list = subparsers.add_parser('list', description="List AWS "
                                        "instances from the command line. "
                                        "List all by typing 'awss list', or"
                                        " specify instances by name, instance"
                                        "-id or state.", usage="\tawss list"
                                        " ( (none) | 'NAME' | '-i ID' | -r |"
                                        " -s ) [ OPTIONS ]")
    parser_list.add_argument('instname', nargs='?', metavar='NAME',
                             help='specify instance by name')
    parser_list.add_argument('-i', '--id', action="store",
                             help='specify instance by id')
    parser_list.add_argument('-s', '--stopped', action='store_const',
                             dest="inState", const="running",
                             help='list stopped instances')
    parser_list.add_argument('-r', '--running', action='store_const',
                             dest="inState", const="running",
                             help='list running instances')
    parser_list.add_argument('-d', '--debug', action="store_true",
                             default=False, help=argparse.SUPPRESS)
    parser_list.set_defaults(func=commandList)

    # Parser for START command
    parser_start = subparsers.add_parser('start', usage="\tawss start ( 'NAME'"
                                         " | '-i ID' ) [ OPTIONS ]",
                                         description="Start an AWS instance"
                                         " from the command line.")
    parser_start.add_argument('instname', nargs='?', metavar='NAME',
                              help='specify instance by name')
    parser_start.add_argument('-i', '--id', action="store",
                              help='specify instance-id')
    parser_start.add_argument('-d', '--debug', action="store_true",
                              default=False, help=argparse.SUPPRESS)
    parser_start.set_defaults(func=commandStart)

    # Parser for STOP command
    parser_stop = subparsers.add_parser('stop', usage="\tawss stop ( 'NAME' |"
                                        " '-i ID' ) [ OPTIONS ]",
                                        description="Stop an AWS instance from"
                                        " the command line.")
    parser_stop.add_argument('instname', nargs='?', metavar='NAME',
                             help='specify instance by name')
    parser_stop.add_argument('-i', '--id', action="store",
                             help='specify instance-id')
    parser_stop.add_argument('-d', '--debug', action="store_true",
                             default=False, help=argparse.SUPPRESS)
    parser_start.set_defaults(func=commandStop)

    # Parser for SSH command
    parser_ssh = subparsers.add_parser('ssh', description="Connect to an AWS i"
                                       "nstance via ssh.", usage="\tawss ssh ("
                                       " 'NAME' | '-i ID' ) [ -u USER -p -h ]")
    parser_ssh.add_argument('instname', nargs='?', metavar='NAME',
                            help='specify instance by name')
    parser_ssh.add_argument('-i', '--id', action="store",
                            help='specify instance-id')
    parser_ssh.add_argument('-u', '--user', action="store",
                            help='specify username to use for ssh')
    parser_ssh.add_argument('-p', '--nopem', action="store_true", default=False,
                            help='connect without PEM key')
    parser_ssh.add_argument('-d', '--debug', action="store_true",
                            default=False, help=argparse.SUPPRESS)
    parser_start.set_defaults(func=commandSSH)

    options = parser.parse_args()
    options.func(options)


if __name__ == '__main__':
    main()
