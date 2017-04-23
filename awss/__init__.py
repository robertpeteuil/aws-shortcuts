#!/usr/bin/env python

# awss - Control AWS instances from command line: list, start, stop or ssh
#
#       https://github.com/robertpeteuil/aws-shortcuts
#
#  Author: Robert Peteuil   @RobertPeteuil

from __future__ import print_function
from builtins import range
import argparse
import sys
from awss.colors import CLRnormal, CLRheading, CLRtitle, CLRwarning, \
    CLRerror, statCLR
from awss.getchar import _Getch
from pprint import pprint

__version__ = '0.9.5.1'


def main():
    global debug
    global debugall

    parser = setupParser()
    options = parser.parse_args()

    if options.debug > 0:
        debug = True
    else:
        debug = False
    if options.debug > 1:
        debugall = True
    else:
        debugall = False

    options.func(options)

    sys.exit()


def setupParser():
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
                                        " 'awss list' will list all instances,"
                                        " or instances can be specified with "
                                        "combinations of NAME, instance-id and"
                                        " current-state.  ex: 'awss list TEST "
                                        "-r' will list instances named 'TEST'"
                                        " that are currently running",
                                        usage="\tawss list [none] [NAME] [-i "
                                        "ID] [-r] [-s] [OPTIONS]")
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
    parser_list.add_argument('-d', '--debug', action="count",
                             default=0, help=argparse.SUPPRESS)
    parser_list.set_defaults(func=cmdList)

    # Parser for START command
    parser_start = subparsers.add_parser('start', usage="\tawss start ( [NAME]"
                                         " [-i ID] ) [-h]",
                                         description="Start an AWS instance"
                                         " from the command line. Either NAME"
                                         " or instance-id must be specified.")
    parser_start.add_argument('instname', nargs='?', metavar='NAME',
                              help='specify instance by name')
    parser_start.add_argument('-i', '--id', action="store",
                              help='specify instance-id')
    parser_start.add_argument('-d', '--debug', action="count",
                              default=0, help=argparse.SUPPRESS)
    parser_start.set_defaults(func=cmdToggle)

    # Parser for STOP command
    parser_stop = subparsers.add_parser('stop', usage="\tawss stop ( [NAME]"
                                        " [-i ID] ) [-h]",
                                        description="Stop an AWS instance"
                                        " from the command line. Either NAME"
                                        " or instance-id must be specified.")
    parser_stop.add_argument('instname', nargs='?', metavar='NAME',
                             help='specify instance by name')
    parser_stop.add_argument('-i', '--id', action="store",
                             help='specify instance-id')
    parser_stop.add_argument('-d', '--debug', action="count",
                             default=0, help=argparse.SUPPRESS)
    parser_stop.set_defaults(func=cmdToggle)

    # Parser for SSH command
    parser_ssh = subparsers.add_parser('ssh', usage="\tawss ssh ( [NAME]"
                                       " [-i ID] ) [-u USER] [-p] [-h]",
                                       description="Connect to an AWS i"
                                       "nstance via ssh. Either NAME "
                                       "or instance-id must be specified.")
    parser_ssh.add_argument('instname', nargs='?', metavar='NAME',
                            help='specify instance by name')
    parser_ssh.add_argument('-i', '--id', action="store",
                            help='specify instance-id')
    parser_ssh.add_argument('-u', '--user', action="store",
                            help='override default username for ssh')
    parser_ssh.add_argument('-p', '--nopem', action="store_true",
                            default=False, help='connect without PEM key')
    parser_ssh.add_argument('-d', '--debug', action="count",
                            default=0, help=argparse.SUPPRESS)
    parser_ssh.set_defaults(func=cmdSsh)
    return parser


def cmdList(options):
    (QueryString, outputTitle) = queryCreate(options)
    iInfo = awsGetList(QueryString)
    if numInstances > 0:
        iInfo = awsGetDetails(iInfo)
        outputTitle = "Instance List - " + outputTitle
        displayList(outputTitle, iInfo)
    else:
        print("No instances found with parameters: %s" % (outputTitle))


def cmdToggle(options):
    iscalc = {"start": "stopped", "stop": "running"}
    recalc = {"start": "StartingInstances", "stop": "StoppingInstances"}
    qryStates = ('CurrentState', 'PreviousState')
    options.inState = iscalc[options.command]
    debugPrint("toggle set state: ", options.inState)
    (QueryString, outputTitle) = queryCreate(options)
    if QueryString == "ec2C.describe_instances(":
        print("%sError%s - instance identifier not specified" %
              (CLRerror, CLRnormal))
        sys.exit(1)
    iInfo = awsGetList(QueryString)
    (tarID, tarIndex) = determineTarget(options.command, iInfo, outputTitle)
    response = awsDoToggle(tarID, options.command)
    filterS = recalc[options.command]
    resp = {}
    for i, j in enumerate(qryStates):
        resp[i] = response["{0}".format(filterS)][0]["{0}".format(j)]['Name']
    print("\tCurrent State: %s%s%s  -  Previous State: %s%s%s\n" %
          (statCLR[resp[0]], resp[0], CLRnormal,
           statCLR[resp[1]], resp[1], CLRnormal))


def cmdSsh(options):
    import os
    import subprocess
    options.inState = "running"
    (QueryString, outputTitle) = queryCreate(options)
    if QueryString == "ec2C.describe_instances(":
        print("%sError%s - instance identifier not specified" %
              (CLRerror, CLRnormal))
        sys.exit(1)
    iInfo = awsGetList(QueryString)
    (tarID, tarIndex) = determineTarget(options.command, iInfo, outputTitle)
    (instanceIP, instanceKey, instanceImgID) = awsGetSsh(tarID)
    homeDir = os.environ['HOME']
    if options.user is None:
        iInfo[tarIndex]['aminame'] = awsGetAmiName(instanceImgID)
        # use dict as lookup table to calculate ssh user based on AMI-name
        # only first 5 chars of AMI-name used to avoid version numbers
        lu = {"ubunt": "ubuntu", "debia": "admin", "fedor": "fedora",
              "cento": "centos", "openB": "root"}
        options.user = lu.get(iInfo[tarIndex]['aminame'][:5], "ec2-user")
        debugPrint("loginuser Calculated: ", options.user)
    else:
        debugPrint("LoginUser set by user: ", options.user)
    if options.nopem:
        debugPrint("Connect string: ", "ssh %s@%s" %
                   (options.user, instanceIP))
        print("%sNo PEM mode%s - connecting without PEM key\n" % (CLRheading,
                                                                  CLRnormal))
        subprocess.call(["ssh {0}@{1}".format(options.user, instanceIP)],
                        shell=True)
    else:
        debugPrint("Connect string: ", "ssh -i %s/.aws/%s.pem %s@%s" %
                   (homeDir, instanceKey, options.user, instanceIP))
        print("")
        subprocess.call(["ssh -i {0}/.aws/{1}.pem {2}@{3}".
                         format(homeDir, instanceKey, options.user,
                                instanceIP)], shell=True)


def queryCreate(options):
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
        (qryStr, outputTitle) = queryAdd(i, qryStr, outputTitle)
        n = True
        FiltEnd = "]"
        outputEnd = ""
        qryStr = qryStr + FiltStart + ("{'Name': 'tag:Name', 'Values': ['%s']}"
                                       % (options.instname))
        outputTitle = outputTitle + "name: '%s'" % (options.instname)
    if options.inState:
        (qryStr, outputTitle) = queryAdd(n, qryStr, outputTitle, i,
                                         FiltStart)
        qryStr = (qryStr + "{'Name': 'instance-state-name','Values': ['%s']}"
                  % (options.inState))
        outputTitle = outputTitle + "state: '%s'" % (options.inState)
        FiltEnd = "]"
        outputEnd = ""
    qryStr = qryStr + FiltEnd + ")"
    outputTitle = outputTitle + outputEnd
    debugPrintAll(qryStr, True)
    debugPrint("outputTitle: ", outputTitle)
    return(qryStr, outputTitle)


def queryAdd(n, qryStr, outputTitle, i=False, FiltStart=""):
    if i or n:
        qryStr = qryStr + ", "
        outputTitle = outputTitle + ", "
    if not n:
            qryStr = qryStr + FiltStart
    return (qryStr, outputTitle)


def awsInit():
    global boto3
    import boto3
    global ec2C
    global ec2R
    ec2C = boto3.client('ec2')
    ec2R = boto3.resource('ec2')


def awsGetList(QueryString):
    global numInstances
    awsInit()
    instanceSummaryData = eval(QueryString)
    iInfo = {}
    for i, v in enumerate(instanceSummaryData['Reservations']):
        inID = v['Instances'][0]['InstanceId']
        iInfo[i] = {'id': inID}
    numInstances = len(iInfo)
    debugPrint("numInstances: ", numInstances)
    debugPrintAll("InstanceIds Only")
    debugPrintAll(iInfo, True)
    return (iInfo)


def awsGetDetails(iInfo):
    for i in range(numInstances):
        instanceData = ec2R.Instance(iInfo[i]['id'])
        iInfo[i]['state'] = instanceData.state['Name']
        iInfo[i]['ami'] = instanceData.image_id
        instanceTag = instanceData.tags
        for j in range(len(instanceTag)):
            if instanceTag[j]['Key'] == 'Name':
                iInfo[i]['name'] = instanceTag[j]['Value']
                break
    debugPrintAll("Details except AMI-name")
    debugPrintAll(iInfo, True)
    return (iInfo)


def awsGetAmiName(instanceImgID):
    aminame = ec2R.Image(instanceImgID).name
    return (aminame)


def awsGetSsh(tarID):
    tarInstance = ec2R.Instance(tarID)
    instanceIP = tarInstance.public_ip_address
    instanceKey = tarInstance.key_name
    instanceImgID = tarInstance.image_id
    return (instanceIP, instanceKey, instanceImgID)


def awsDoToggle(tarID, cmdtodo):
    tarInstance = ec2R.Instance(tarID)
    thecmd = getattr(tarInstance, cmdtodo)
    response = thecmd()
    return (response)


def displayList(outputTitle, iInfo, numbered="no"):
    if numbered == "no":
        print("\n%s\n" % (outputTitle))
    for i in range(numInstances):
        if numbered == "yes":
            print("Instance %s#%s%s" % (CLRwarning, i + 1, CLRnormal))
        iInfo[i]['aminame'] = awsGetAmiName(iInfo[i]['ami'])
        print("\tName: %s%s%s\t\tID: %s%s%s\t\tStatus: %s%s%s" %
              (CLRtitle, iInfo[i]['name'], CLRnormal, CLRtitle, iInfo[i]['id'],
               CLRnormal, statCLR[iInfo[i]['state']], iInfo[i]['state'],
               CLRnormal))
        print("\tAMI: %s%s%s\tAMI Name: %s%s%s\n" %
              (CLRtitle, iInfo[i]['ami'], CLRnormal, CLRtitle,
               iInfo[i]['aminame'], CLRnormal))
    debugPrintAll("All Data")
    debugPrintAll(iInfo, True)


def determineTarget(command, iInfo, outputTitle):
    if numInstances == 0:
        print("No instances found with parameters: %s" % (outputTitle))
        sys.exit()
    if numInstances > 1:
        iInfo = awsGetDetails(iInfo)
        print("\n%s instances match these parameters:\n" % (numInstances))
        tarIndex = userPicklist(outputTitle, iInfo, command)
    else:
        tarIndex = 0
    tarID = iInfo[tarIndex]['id']
    print("\n%s%sing%s instance id %s%s%s" % (statCLR[command],
                                              command, CLRnormal,
                                              CLRtitle, tarID, CLRnormal))
    return (tarID, tarIndex)


def userPicklist(outputTitle, iInfo, command):
    getch = _Getch()
    selValid = "False"
    displayList(outputTitle, iInfo, "yes")
    while selValid != "True":
        sys.stdout.write("Enter %s#%s of instance to %s (%s1%s-%s%i%s) [%s0"
                         " aborts%s]: " % (CLRwarning, CLRnormal, command,
                                           CLRwarning, CLRnormal, CLRwarning,
                                           numInstances, CLRnormal, CLRtitle,
                                           CLRnormal))
        RawkeyEntered = getch()
        sys.stdout.write(RawkeyEntered)
        (tarIndex, selValid) = userKeyEntry(RawkeyEntered, command)
    print()
    return (tarIndex)


def userKeyEntry(RawkeyEntered, command):
    selValid = "False"
    try:
        KeyEntered = int(RawkeyEntered)
    except ValueError:
        KeyEntered = RawkeyEntered
    if KeyEntered == 0:
        print("\n\n%saborting%s - %s instance\n" %
              (CLRerror, CLRnormal, command))
        sys.exit()
    elif KeyEntered >= 1 and KeyEntered <= numInstances:
        instanceForAction = KeyEntered - 1
        selValid = "True"
    else:
        sys.stdout.write("\n%sInvalid entry:%s enter a number between 1"
                         " and %s.\n" % (CLRerror, CLRnormal, numInstances))
        instanceForAction = KeyEntered
    return (instanceForAction, selValid)


def debugPrint(item1, item2=""):  # pragma: no cover
    if debug:
        print(item1, "%s%s%s" % (CLRtitle, item2, CLRnormal))


def debugPrintAll(passeditem, special=False):  # pragma: no cover
    if debugall:
        if special:
            pprint(passeditem)
        else:
            print("%s%s%s" % (CLRtitle, passeditem, CLRnormal))


if __name__ == '__main__':
    main()
