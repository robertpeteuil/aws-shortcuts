#!/usr/bin/env python

# awss - Control AWS instances from command line: list, start, stop or ssh
#
#       https://github.com/robertpeteuil/aws-shortcuts
#
#   Build: 0.9.3.5    Date 2017-04-21
#
#  Author: Robert Peteuil   @RobertPeteuil

from __future__ import print_function
from builtins import range
from builtins import object
import argparse
import boto3
import sys
import subprocess
import os


class _Getch(object):
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()


class _GetchUnix(object):
    def __init__(self):
        import tty, sys     # noqa: F401, E401

    def __call__(self):
        import sys, tty, termios    # noqa: E401
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows(object):    # pragma: no cover
    def __init__(self):
        import msvcrt       # noqa: F401

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


def setupColor():
    global CLRnormal
    global CLRheading
    global CLRheading2
    global CLRtitle
    global CLRtitle2
    global CLRsuccess
    global CLRwarning
    global CLRerror
    global statCLR
    CLRnormal = ""
    CLRheading = ""
    CLRheading2 = ""
    CLRtitle = ""
    CLRtitle2 = ""
    CLRsuccess = ""
    CLRwarning = ""
    CLRerror = ""
    if sys.stdout.isatty():
        ncolors = int(runBash("tput colors 2> /dev/null"))
        if ncolors != "" and ncolors >= 8:
            blue = "\033[1;34m"
            white = "\033[1;37m"
            green = "\033[1;32m"
            red = "\033[1;31m"
            yellow = "\033[1;33m"
            cyan = "\033[1;36m"
            CLRnormal = white
            CLRheading = green
            CLRheading2 = blue
            CLRtitle = cyan
            CLRtitle2 = yellow
            CLRsuccess = green
            CLRwarning = yellow
            CLRerror = red
    statCLR = {"running": CLRsuccess, "start": CLRsuccess, "ssh": CLRsuccess,
               "stopped": CLRerror, "stop": CLRerror, "stopping": CLRwarning,
               "pending": CLRwarning, "starting": CLRwarning}


def runBash(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    if err:     # pragma: no cover
        p_status = p.wait()
        print("Command exit status / return code : ", p_status)
    return (output.rstrip())


def printNoCR(value):
    sys.stdout.write(value)


def getArguments():
    parser = argparse.ArgumentParser(description="Control AWS instances from"
                                     " the command line with: list, start,"
                                     " stop or ssh.", prog='awss',
                                     usage="\tawss {command} ( 'NAME' or"
                                     " '-i ID' ) [ OPTIONS ]\n\t{command} ="
                                     " list | start | stop | ssh")
    parser.add_argument('-v', '--version', action="version",
                        version='awss 0.9.3.4')

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
    parser_list.add_argument('-r', '--running', action="store_true",
                             help='list running instances')
    parser_list.add_argument('-s', '--stopped', action="store_true",
                             help='list stopped instances')
    parser_list.add_argument('-d', '--debug', action="store_true",
                             help=argparse.SUPPRESS)

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
                              help=argparse.SUPPRESS)

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
                             help=argparse.SUPPRESS)

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
    parser_ssh.add_argument('-p', '--nopem', action="store_true",
                            help='connect without PEM key')
    parser_ssh.add_argument('-d', '--debug', action="store_true",
                            help=argparse.SUPPRESS)

    options = parser.parse_args()
    return(options)


def decodeArguments(options):
    loginuser = ""
    filterType = ""
    filters = ""
    OutputText = ""
    nopem = False
    if options.instname:
        filterType = "name"
        filters = options.instname
    elif options.id:
        filterType = "id"
        filters = options.id
    if options.command == "list":
        filterType2 = ""
        (filterType, filters, OutputText) = decodeLIST(options, filterType,
                                                       filters)
    elif options.command == "ssh":
        filterType2 = "running"
        (nopem, loginuser) = decodeSSH(options)
    else:       # must be stop or start left
        (filterType2) = decodeToggle(options)
    return (options.command, filterType, filterType2, filters, OutputText,
            nopem, loginuser, options.debug)


def decodeLIST(options, filterType, filters):
    if filterType == "":        # only call if NAME or ID not specified
        if options.running:
            filterType = "running"
            filters = "running"
            OutputText = "Running EC2 Instances"
        elif options.stopped:
            filterType = "stopped"
            filters = "stopped"
            OutputText = "Stopped EC2 Instances"
        else:
            filterType = "all"
            filters = ""
            OutputText = "All Instances"
    else:
        OutputText = "Instances '{}'".format(filters)
    return (filterType, filters, OutputText)


def decodeSSH(options):
    if options.nopem:
        nopem = True
    else:
        nopem = False
    if options.user:
        loginuser = options.user
    else:
        loginuser = ""
    return (nopem, loginuser)


def decodeToggle(options):
    if options.command == "start":
        filterType2 = "stopped"
    elif options.command == "stop":
        filterType2 = "running"
    return (filterType2)


def getInstanceIDs(filtype, filter):
    global instanceID
    global numInstances
    instanceID = {}
    if filtype == "id":
        instanceSummaryData = ec2C.describe_instances(
            InstanceIds=["{0}".format(filter)])
    elif filtype == "running" or filtype == "stopped":
        instanceSummaryData = ec2C.describe_instances(
            Filters=[{'Name': 'instance-state-name',
                      'Values': ["{0}".format(filter)]}])
    elif filtype == "name":
        instanceSummaryData = ec2C.describe_instances(
            Filters=[{'Name': 'tag:Name', 'Values': ["{0}".format(filter)]}])
    else:
        instanceSummaryData = ec2C.describe_instances()
    for i, v in enumerate(instanceSummaryData['Reservations']):
        ID = v['Instances'][0]['InstanceId']
        instanceID[i] = ID
    numInstances = len(instanceID)
    return


def getAMIname(ID):
    instanceImage = ec2R.Image(ID).name
    return (instanceImage)


def getInstanceDetails():
    global numInstances
    global instanceID
    global instanceState
    global instanceAMI
    global instanceName
    global instanceAMIName
    instanceState = {}
    instanceAMI = {}
    instanceName = {}
    instanceAMIName = {}
    for i in range(numInstances):
        instanceData = ec2R.Instance(instanceID[i])
        instanceState[i] = instanceData.state['Name']
        instanceAMI[i] = instanceData.image_id
        instanceTag = instanceData.tags
        for j in range(len(instanceTag)):
            if instanceTag[j]['Key'] == 'Name':
                instanceName[i] = instanceTag[j]['Value']
                break
        instanceAMIName[i] = getAMIname(instanceAMI[i])
    return


def refineInstanceList(filterType2):
    global numInstances
    newQty = numInstances
    for i in range(numInstances):
        if instanceState[i] != filterType2:
            del instanceName[i]
            del instanceID[i]
            del instanceState[i]
            del instanceAMI[i]
            del instanceAMIName[i]
            newQty -= 1
    numInstances = newQty
    return


def displayInstanceList(title, numbered="no"):
    if numbered == "no":
        print("\n%s%s%s\n" % (CLRheading, title, CLRnormal))
    for i in range(numInstances):
        if numbered == "yes":
            print("Instance %s#%s%s" % (CLRwarning, i + 1, CLRnormal))
        print("\tName: %s%s%s\t\tID: %s%s%s\t\tStatus: %s%s%s" %
              (CLRtitle, instanceName[i], CLRnormal, CLRtitle, instanceID[i],
               CLRnormal, statCLR[instanceState[i]], instanceState[i],
               CLRnormal))
        print("\tAMI: %s%s%s\tAMI Name: %s%s%s\n" %
              (CLRtitle, instanceAMI[i], CLRnormal, CLRtitle,
               instanceAMIName[i], CLRnormal))


def selectFromList(OutputText, actionType):
    getch = _Getch()
    selectionValid = "False"
    displayInstanceList(OutputText, "yes")
    while selectionValid != "True":
        printNoCR("Enter %s#%s of instance to %s (%s1%s-%s%i%s) [%s0 aborts%s"
                  "]: " % (CLRwarning, CLRnormal, actionType, CLRwarning,
                           CLRnormal, CLRwarning, numInstances, CLRnormal,
                           CLRtitle, CLRnormal))
        RawkeyEntered = getch()
        printNoCR(RawkeyEntered)
        (instanceForAction, selectionValid) = validateKeyEntry(RawkeyEntered,
                                                               actionType)
    print()
    return (instanceForAction)


def validateKeyEntry(RawkeyEntered, actionType):
    selectionValid = "False"
    try:
        KeyEntered = int(RawkeyEntered)
    except ValueError:
        KeyEntered = RawkeyEntered
    if KeyEntered == 0:
        print("\n\n%saborting%s - %s instance\n" %
              (CLRerror, CLRnormal, actionType))
        sys.exit()
    elif KeyEntered >= 1 and KeyEntered <= numInstances:
        instanceForAction = KeyEntered - 1
        selectionValid = "True"
    else:
        printNoCR("\n%sInvalid entry:%s enter a number between 1 and %s.\n"
                  % (CLRerror, CLRnormal, numInstances))
        instanceForAction = KeyEntered
    return (instanceForAction, selectionValid)


def debugPrint(item1, item2=""):  # pragma: no cover
    global debug
    if (debug):
        print(item1, "%s%s%s" % (CLRtitle, item2, CLRnormal))


def debugPrintList(listname, displayname):  # pragma: no cover
    print("%sListing %s %s" % (CLRheading, displayname, CLRnormal))
    for x, y in list(listname.items()):
        print("\ti = %s%s%s, %s = %s%s%s" % (CLRtitle, x, CLRnormal,
                                             displayname, CLRtitle, y,
                                             CLRnormal))


def debugPrintAllLists():  # pragma: no cover
    print("%sDebug Listing of Info by Type%s\n" % (CLRheading2, CLRnormal))
    debugPrintList(instanceID, "instanceID")
    debugPrintList(instanceState, "instanceState")
    debugPrintList(instanceAMI, "instanceAMI")
    debugPrintList(instanceName, "instanceName")
    debugPrintList(instanceAMIName, "instanceAMIName")


def performSSHAction(specifiedInstance, loginuser, index, nopem):
    # only first 5 chars of AMI-name used to avoid version numbers
    lu = {"ubunt": "ubuntu", "debia": "admin", "fedor": "fedora",
          "cento": "centos", "openB": "root"}
    instanceIP = specifiedInstance.public_ip_address
    instanceKey = specifiedInstance.key_name
    homeDir = os.environ['HOME']
    debugPrint("target IP =", instanceIP)
    debugPrint("target key =", instanceKey)
    if loginuser == "":
        loginuser = lu.get(instanceAMIName[index][:5], "ec2-user")
        debugPrint("loginuser Calculated =", loginuser)
    else:
        debugPrint("LoginUser set by user:", loginuser)
    if (nopem):
        debugPrint("Connect string:", "ssh %s@%s" % (loginuser, instanceIP))
        print("%sNo PEM mode%s - connecting without PEM key\n" % (CLRheading,
                                                                  CLRnormal))
        subprocess.call(["ssh {0}@{1}".format(loginuser, instanceIP)],
                        shell=True)
    else:
        debugPrint("Connect string:", "ssh -i %s/.aws/%s.pem %s@%s\n" %
                   (homeDir, instanceKey, loginuser, instanceIP))
        subprocess.call(["ssh -i {0}/.aws/{1}.pem {2}@{3}".
                         format(homeDir, instanceKey, loginuser, instanceIP)],
                        shell=True)


def performToggleAction(specifiedInstance, actionType):
    if actionType == "start":
        filterS = "StartingInstances"
    else:
        filterS = "StoppingInstances"
    thecmd = getattr(specifiedInstance, actionType)
    response = thecmd()
    currentState = response["{0}".format(filterS)][0]['CurrentState']['Name']
    prevState = response["{0}".format(filterS)][0]['PreviousState']['Name']
    print("\tCurrent State: %s%s%s  -  Previous State: %s%s%s" %
          (statCLR[currentState], currentState, CLRnormal,
           statCLR[prevState], prevState, CLRnormal))


def detTargetInstance(filterType2, filters, OutputText, actionType):
    global numInstances
    global debug
    refineInstanceList(filterType2)
    if numInstances == 0:
        print("No instance '%s' found %s." % (filters, filterType2))
        sys.exit()
    elif numInstances > 1:
        print("\n%s instances match these parameters:\n" % (numInstances))
        instanceForAction = selectFromList(OutputText, actionType)
    else:
        instanceForAction = 0
    if (debug):             # pragma: no cover
        debugPrintAllLists()
    (index, instanceIDForAction) = instanceID.items()[instanceForAction]
    print("\n%s%sing%s instance: %s%s%s with id: %s%s%s" %
          (statCLR[actionType], actionType, CLRnormal, CLRtitle,
           filters, CLRnormal, CLRtitle, instanceIDForAction, CLRnormal))
    specifiedInstance = ec2R.Instance(instanceIDForAction)
    return (index, specifiedInstance)


def performAction(actionType, filterType, filterType2, filters, OutputText,
                  nopem, loginuser):
    global numInstances
    if actionType == "list":
        if numInstances > 0:
            displayInstanceList(OutputText)
        else:
            print("No instance '%s' found." % (filters))
    else:
        (index, specifiedInstance) = detTargetInstance(filterType2,
                                                       filters, OutputText,
                                                       actionType)
        if actionType == "start" or actionType == "stop":
            performToggleAction(specifiedInstance, actionType)
        else:
            performSSHAction(specifiedInstance, loginuser, index, nopem)


def main():

    global debug
    global ec2C
    global ec2R

    # Setup AWS EC2 connections
    ec2C = boto3.client('ec2')
    ec2R = boto3.resource('ec2')

    (options) = getArguments()
    (actionType, filterType, filterType2, filters, OutputText, nopem,
     loginuser, debug) = decodeArguments(options)

    setupColor()

    debugPrint("actionType =", actionType)
    debugPrint("filterType =", filterType)
    debugPrint("filterType2 =", filterType2)
    debugPrint("filters =", filters)
    debugPrint("OutputText =", OutputText)
    debugPrint("nopem =", nopem)
    debugPrint("loginuser =", loginuser)

    if actionType != "list" and filterType == "":
        print("%sError%s - instance identifier not specified" %
              (CLRerror, CLRnormal))
        sys.exit()

    getInstanceIDs(filterType, filters)
    getInstanceDetails()

    performAction(actionType, filterType, filterType2, filters, OutputText,
                  nopem, loginuser)

    sys.exit()


if __name__ == '__main__':
    main()
