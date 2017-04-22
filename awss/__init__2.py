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
# import subprocess
# import os
from awss.colors import CLRnormal, CLRheading, CLRheading2, CLRtitle,\
    CLRwarning, CLRerror, statCLR
# from awss.getchar import _Getch
from pprint import pprint

__version__ = '0.9.4.5'


def main():

    getArguments()

    sys.exit()

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
                             dest="inState", const="stopped",
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
    parser_start.set_defaults(func=commandToggle)

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
    parser_stop.set_defaults(func=commandToggle)

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
    parser_ssh.set_defaults(func=commandSSH)

    options = parser.parse_args()
    options.func(options)


def commandList(options):
    (QueryString, outputTitle) = calculateQuery(options)
    iInfo = getInstList(QueryString)
    # get full details
    if numInstances > 0:
        iInfo = getInstDetails(iInfo)
        outputTitle = "Instance List - " + outputTitle
        displayInstanceList(outputTitle, iInfo)
    else:
        print("No instances found with parameters: %s" % (outputTitle))
    # print(outputTitle)
    # debugPrint(iInfo)


def commandToggle(options):
    iscalc = {"start": "stopped", "stop": "running"}
    options.inState = iscalc[options.command]
    print("toggle set state = %s" % (options.inState))
    (QueryString, outputTitle) = calculateQuery(options)
    if QueryString == "ec2C.describe_instances(":
        print("%sError%s - instance identifier not specified" %
              (CLRerror, CLRnormal))
        sys.exit()
    iInfo = getInstList(QueryString)
    print("\nFull Report:\n")
    debugPrint(iInfo)


def commandSSH(options):
    options.inState = "running"
    (QueryString, outputTitle) = calculateQuery(options)
    if QueryString == "ec2C.describe_instances(":
        print("%sError%s - instance identifier not specified" %
              (CLRerror, CLRnormal))
        sys.exit()
    iInfo = getInstList(QueryString)
    print("\nFull Report:\n")
    debugPrint(iInfo)


def calculateQuery(options):
    qryStr = "ec2C.describe_instances("
    FiltStart = "Filters=["
    FiltEnd = ""
    outputTitle = ""
    outputEnd = "All"
    i = False
    n = False
    if options.id:
        qryStr = qryStr + "InstanceIds=['%s']" % (options.id)
        outputTitle = outputTitle + "id: '%s'" % (options.id)
        i = True
        outputEnd = ""
    if options.instname:
        # if i:
        #     qryStr = qryStr + ", "
        #     outputTitle = outputTitle + ", "
        (qryStr, outputTitle) = appendQuery(i, qryStr, outputTitle)
        n = True
        FiltEnd = "]"
        outputEnd = ""
        qryStr = qryStr + FiltStart + ("{'Name': 'tag:Name', 'Values': ['%s']}"
                                       % (options.instname))

        outputTitle = outputTitle + "name: '%s'" % (options.instname)
    if options.inState:
        # if n:
        #     qryStr = qryStr + ", "
        #     outputTitle = outputTitle + ", "
        # else:
        #     qryStr = qryStr + FiltStart
        (qryStr, outputTitle) = appendQuery(n, qryStr, outputTitle, i,
                                            FiltStart)
        qryStr = qryStr + "{'Name': 'instance-state-name','Values': ['%s']}" % (options.inState)
        outputTitle = outputTitle + "state: '%s'" % (options.inState)
        FiltEnd = "]"
        outputEnd = ""
    qryStr = qryStr + FiltEnd + ")"
    outputTitle = outputTitle + outputEnd
    return(qryStr, outputTitle)


def appendQuery(n, qryStr, outputTitle, i=False, FiltStart=""):
    if i or n:
        qryStr = qryStr + ", "
        outputTitle = outputTitle + ", "
    if not n:
            qryStr = qryStr + FiltStart
    return (qryStr, outputTitle)


def getInstList(QueryString):
    global numInstances
    global ec2C
    ec2C = boto3.client('ec2')
    instanceSummaryData = eval(QueryString)
    iInfo = {}
    for i, v in enumerate(instanceSummaryData['Reservations']):
        inID = v['Instances'][0]['InstanceId']
        iInfo[i] = {'id': inID}
    numInstances = len(iInfo)
    # print("numInstances:", numInstances)
    # debugPrint(iInfo)
    return (iInfo)


def getInstDetails(iInfo):
    global ec2R
    ec2R = boto3.resource('ec2')
    for i in range(numInstances):
        instanceData = ec2R.Instance(iInfo[i]['id'])
        iInfo[i]['state'] = instanceData.state['Name']
        iInfo[i]['ami'] = instanceData.image_id
        instanceTag = instanceData.tags
        for j in range(len(instanceTag)):
            if instanceTag[j]['Key'] == 'Name':
                iInfo[i]['name'] = instanceTag[j]['Value']
                break
    return (iInfo)


def displayInstanceList(outputTitle, iInfo, numbered="no"):
    global instanceAMIName
    if numbered == "no":
        print("\n%s%s%s\n" % (CLRheading2, outputTitle, CLRnormal))
    for i in range(numInstances):
        if numbered == "yes":
            print("Instance %s#%s%s" % (CLRwarning, i + 1, CLRnormal))
        iInfo[i]['aminame'] = ec2R.Image(iInfo[i]['ami']).name
        print("\tName: %s%s%s\t\tID: %s%s%s\t\tStatus: %s%s%s" %
              (CLRtitle, iInfo[i]['name'], CLRnormal, CLRtitle, iInfo[i]['id'],
               CLRnormal, statCLR[iInfo[i]['state']], iInfo[i]['state'],
               CLRnormal))
        print("\tAMI: %s%s%s\tAMI Name: %s%s%s\n" %
              (CLRtitle, iInfo[i]['ami'], CLRnormal, CLRtitle,
               iInfo[i]['aminame'], CLRnormal))


def debugPrint(passeditem):
    pprint(passeditem)


if __name__ == '__main__':
    main()
