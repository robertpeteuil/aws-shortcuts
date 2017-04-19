#!/usr/bin/env python

# awss - Control AWS instances from the command line with: list, start, stop or ssh.
#
#       https://github.com/robertpeteuil/aws-shortcuts
#
#   Build: 0.9.2    Date 2017-04-18
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

################################################################################
#  Classes

class _Getch(object):
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix(object):
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows(object):
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

################################################################################
#  Functions

def setupColor():
    global CLRnormal
    global CLRheading
    global CLRheading2
    global CLRtitle
    global CLRtitle2
    global CLRsuccess
    global CLRwarning
    global CLRerror
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
            blue="\033[1;34m"
            white="\033[1;37m"
            green="\033[1;32m"
            red="\033[1;31m"
            yellow="\033[1;33m"
            cyan="\033[1;36m"
            CLRnormal = white
            CLRheading = green
            CLRheading2 = blue
            CLRtitle = cyan
            CLRtitle2 = yellow
            CLRsuccess = green
            CLRwarning = yellow
            CLRerror = red

def colorInstanceStatus(state):
    if state == "running":
        CLRstatus = CLRsuccess
    elif state == "stopped":
        CLRstatus = CLRerror
    elif state == "stopping":
        CLRstatus = CLRwarning
    elif state == "pending":
        CLRstatus = CLRwarning
    elif state == "starting":
        CLRstatus = CLRwarning
    elif state == "start":
        CLRstatus = CLRsuccess
    elif state == "stop":
        CLRstatus = CLRerror
    else:
        CLRstatus = CLRnormal
    return CLRstatus

def runBash(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    if err:
        p_status = p.wait()
        print("Command exit status / return code : ", p_status)
    return (output.rstrip())

def printWithoutCR(value):
    sys.stdout.write(value)

def printList(listname, displayname):
    print("%sListing %s %s" % (CLRheading, displayname, CLRnormal))
    for x,y in list(listname.items()):
        print("\ti = %s%s%s, %s = %s%s%s" % (CLRtitle, x, CLRnormal, displayname, CLRtitle, y, CLRnormal))

def getArguments():
    nopem = False
    loginuser = ""
    filterType = ""
    filters = ""
    OutputText = ""
    parser = argparse.ArgumentParser(description="Control AWS instances from the command line with: list, start, stop or ssh.", usage="\tawss {command} ( 'NAME' or '-i ID' ) [ OPTIONS ]\n\t{command} = list | start | stop | ssh",
        prog='awss')
    parser.add_argument('-v', '--version', action = "version", version='awss 0.9.2')
    subparsers = parser.add_subparsers(dest='command', title='For additional help on command parameters', description="type 'awss {command} -h', where {command} is: list, start, stop or ssh")
    parser_list = subparsers.add_parser('list', description="List AWS instances from the command line. List all by typing 'awss list', or specify instances by name, instance-id or state.", usage="\tawss list ( (none) | 'NAME' | '-i ID' | -r | -s ) [ OPTIONS ]")
    parser_list.add_argument('instname', nargs='?', metavar='NAME', help='specify instance by name')
    parser_list.add_argument('-i', '--id', action="store",
                help='specify instance by id')
    parser_list.add_argument('-r', '--running', action = "store_true",
                help = 'list running instances')
    parser_list.add_argument('-s', '--stopped', action = "store_true",
                help='list stopped instances')
    parser_list.add_argument('-d', '--debug', action="store_true",
                help=argparse.SUPPRESS)
    parser_start = subparsers.add_parser('start', description="Start an AWS instance from the command line.", usage="\tawss start ( 'NAME' | '-i ID' ) [ OPTIONS ]")
    parser_start.add_argument('instname', nargs='?', metavar='NAME', help='specify instance by name')
    parser_start.add_argument('-i', '--id', action="store",
                help='specify instance-id')
    parser_start.add_argument('-d', '--debug', action="store_true",
                help=argparse.SUPPRESS)
    parser_stop = subparsers.add_parser('stop', description="Stop an AWS instance from the command line.", usage="\tawss stop ( 'NAME' | '-i ID' ) [ OPTIONS ]")
    parser_stop.add_argument('instname', nargs='?', metavar='NAME', help='specify instance by name')
    parser_stop.add_argument('-i', '--id', action="store",
                help='specify instance-id')
    parser_stop.add_argument('-d', '--debug', action="store_true",
                help=argparse.SUPPRESS)
    parser_ssh = subparsers.add_parser('ssh', description="Connect to an AWS instance via ssh.", usage="\tawss ssh ( 'NAME' | '-i ID' ) [ -u USER -p -h ]")
    parser_ssh.add_argument('instname', nargs='?', metavar='NAME', help='specify instance by name')
    parser_ssh.add_argument('-i', '--id', action="store",
                help='specify instance-id')
    parser_ssh.add_argument('-u', '--user', action="store",
                help='specify username to use for ssh')
    parser_ssh.add_argument('-p', '--nopem', action = "store_true",
                help='connect without PEM key')
    parser_ssh.add_argument('-d', '--debug', action="store_true",
                help=argparse.SUPPRESS)
    options = parser.parse_args()
    if options.command == "list":
        actionType="list"
        filterType2 = ""
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
            OutputText = "All Instances"
    elif options.command == "start":
        actionType = "start"
        filterType2 = "stopped"
    elif options.command == "stop":
        actionType = "stop"
        filterType2 = "running"
    elif options.command == "ssh":
        actionType = "ssh"
        filterType2 = "running"
        if options.nopem:
            nopem = True
        if options.user:
            loginuser = options.user
    if options.instname:
        filterType = "name"
        filters = options.instname
        OutputText = "Instances '{}'".format(options.instname)
    elif options.id:
        filterType = "id"
        filters = options.id
        OutputText = "Instance '{}'".format(options.id)
    if options.debug:
        debug = True
    else:
        debug = False
    return (actionType, filterType, filterType2, filters, OutputText, debug, nopem, loginuser)

def getInstanceIDs(filtype, filter):
    instanceID = {}
    if filtype == "id":
        instanceSummaryData = ec2C.describe_instances( InstanceIds=["{0}".format(filter)])
    elif filtype == "running" or filtype == "stopped":
        instanceSummaryData = ec2C.describe_instances( Filters =[{'Name':'instance-state-name', 'Values':["{0}".format(filter)]}])
    elif filtype == "name":
        instanceSummaryData = ec2C.describe_instances( Filters =[{'Name':'tag:Name', 'Values':["{0}".format(filter)]}])
    else:
        instanceSummaryData = ec2C.describe_instances()
    for i,v in enumerate(instanceSummaryData['Reservations']):
        ID = v['Instances'][0]['InstanceId']
        instanceID[i] = ID
    numInstances=len(instanceID)
    return (instanceID, numInstances)

def getAMIname(ID):
    instanceImage = ec2R.Image(ID).name
    return (instanceImage)

def getInstanceDetails(qty,idlist):
    instanceState = {}
    instanceAMI = {}
    instanceName = {}
    instanceAMIName = {}
    for i in range(qty):
        instanceData = ec2R.Instance(idlist[i])
        instanceState[i] = instanceData.state['Name']
        instanceAMI[i] = instanceData.image_id
        instanceTag = instanceData.tags
        for j in range(len(instanceTag)):
            if instanceTag[j]['Key'] == 'Name':
                instanceName[i]=instanceTag[j]['Value']
                break
        instanceAMIName[i] = getAMIname(instanceAMI[i])
    return (instanceState, instanceAMI, instanceName, instanceAMIName)

def refineInstanceList(numInstances, filterType2):
    newQty = numInstances
    for i in range(numInstances):
        if instanceState[i] != filterType2:
            del instanceName[i]
            del instanceID[i]
            del instanceState[i]
            del instanceAMI[i]
            del instanceAMIName[i]
            newQty -= 1
    return (newQty, instanceName, instanceID, instanceState, instanceAMI, instanceAMIName)

def displayInstanceList(title, numbered="no"):
    if numbered == "no":
        print("\n%s%s%s\n" % (CLRheading, title, CLRnormal))
    for i in range(numInstances):
        if numbered == "yes":
            print("Instance %s#%s%s" % (CLRwarning, i+1, CLRnormal))
        CLRstatus = colorInstanceStatus(instanceState[i])
        print("\tName: %s%s%s\t\tID: %s%s%s\t\tStatus: %s%s%s" % (CLRtitle, instanceName[i], CLRnormal, CLRtitle, instanceID[i], CLRnormal, CLRstatus, instanceState[i], CLRnormal))
        print("\tAMI: %s%s%s\tAMI Name: %s%s%s\n" % (CLRtitle, instanceAMI[i], CLRnormal, CLRtitle, instanceAMIName[i], CLRnormal))

def selectFromList(OutputText, actionType):
    getch = _Getch()
    selectionValid = "False"
    displayInstanceList(OutputText, "yes")
    while selectionValid != "True":
        printWithoutCR("Enter %s#%s of instance to %s (%s1%s-%s%i%s) [%s0 aborts%s]: " % (CLRwarning, CLRnormal, actionType, CLRwarning, CLRnormal, CLRwarning, numInstances, CLRnormal, CLRtitle, CLRnormal))
        RawkeyEntered = getch()
        printWithoutCR(RawkeyEntered)
        try:
            KeyEntered = int(RawkeyEntered)
        except:
            KeyEntered = RawkeyEntered
        if KeyEntered == 0:
            print("\n\n%saborting%s - %s instance\n" % (CLRerror, CLRnormal, actionType))
            sys.exit()
        if KeyEntered >= 1 and KeyEntered <= numInstances:
            instanceForAction = KeyEntered - 1
            selectionValid = "True"
        else:
            printWithoutCR("\n%sInvalid entry:%s enter a number between 1 and %s.\n" % (CLRerror, CLRnormal, numInstances))
    print()
    return (instanceForAction)

def DetermineLoginUser(ID):
    selectedImageDescription = instanceAMIName[ID]
    if selectedImageDescription.startswith( 'ubuntu' ):
        loginuser="ubuntu"
    elif selectedImageDescription.startswith( 'suse' ):
        loginuser="ec2-user"
    elif selectedImageDescription.startswith( 'amzn' ):
        loginuser="ec2-user"
    elif selectedImageDescription.startswith( 'RHEL' ):
        loginuser="ec2-user"
    elif selectedImageDescription.startswith( 'debian' ):
        loginuser="admin"
    elif selectedImageDescription.startswith( 'fedora' ):
        loginuser="fedora"
    elif selectedImageDescription.startswith( 'centos' ):
        loginuser="centos"
    elif selectedImageDescription.startswith( 'openBSD' ):
        loginuser="root"
    else:
        loginuser="ec2-user"
    if (debug):
        print("loginuser calculated as: %s%s%s\n" % (CLRtitle, loginuser, CLRnormal))
    return (loginuser)

def debugPrintList():
    print("%sDebug Listing of Info by Type%s\n" % (CLRheading2, CLRnormal))
    printList(instanceID, "instanceID")
    printList(instanceState, "instanceState")
    printList(instanceAMI, "instanceAMI")
    printList(instanceName, "instanceName")
    printList(instanceAMIName, "instanceAMIName")

################################################################################
#  Execution Begins

def main():

    global debug
    global ec2C
    global ec2R
    global numInstances
    global instanceID
    global instanceState
    global instanceAMI
    global instanceName
    global instanceAMIName

    instanceID = {}
    instanceState = {}
    instanceAMI = {}
    instanceName = {}
    instanceAMIName = {}

    # Setup AWS EC2 connections
    ec2C = boto3.client('ec2')
    ec2R = boto3.resource('ec2')

    (actionType, filterType, filterType2, filters, OutputText, debug, nopem, loginuser) = getArguments()

    setupColor()

    if (debug):
        print("actionType = ", actionType)
        print("filterType = ", filterType)
        print("filterType2 = ", filterType2)
        print("filters = ", filters)
        print("OutputText = ", OutputText)
        print("nopem = ", nopem)
        print("loginuser = ", loginuser)

    if actionType != "list" and filterType == "":
        print("%sError%s - instance identifier not specified" % (CLRerror, CLRnormal))
        sys.exit()

    (instanceID, numInstances) = getInstanceIDs(filterType, filters)
    (instanceState, instanceAMI, instanceName, instanceAMIName) = getInstanceDetails(numInstances, instanceID)

    if actionType == "list":
        if numInstances > 0:
            displayInstanceList(OutputText)
        else:
            print("No instance '%s' found." % (filters))
    else:
        # narrow it down to one instance
        (numInstances, instanceName, instanceID, instanceState, instanceAMI, instanceAMIName) = refineInstanceList(numInstances, filterType2)
        if numInstances == 0:
            print("No instance '%s' found %s." % (filters, filterType2))
            sys.exit()
        if numInstances > 1:
            print("\n%s instances match these parameters:\n" % (numInstances))
            instanceForAction = selectFromList(OutputText, actionType)
        else:
            instanceForAction = 0
        if (debug):
            debugPrintList()
        # get index# and instance-id of target instance
        index, instanceIDForAction = instanceID.items()[instanceForAction]
        print("\n%s%sing%s instance: %s%s%s with id: %s%s%s" % (colorInstanceStatus(actionType), actionType, CLRnormal, CLRtitle, filters, CLRnormal, CLRtitle, instanceIDForAction, CLRnormal))
        specifiedInstance = ec2R.Instance(instanceIDForAction)
        # perform instance specific actions
        if actionType == "start":
            response = specifiedInstance.start()
            currentState = response['StartingInstances'][0]['CurrentState']['Name']
            prevState = response['StartingInstances'][0]['PreviousState']['Name']
            print("\tCurrent State: %s%s%s  -  Previous State: %s%s%s" % (colorInstanceStatus(currentState), currentState, CLRnormal, colorInstanceStatus(prevState), prevState, CLRnormal))
        elif actionType == "stop":
            response = specifiedInstance.stop()
            currentState = response['StoppingInstances'][0]['CurrentState']['Name']
            prevState = response['StoppingInstances'][0]['PreviousState']['Name']
            print("\tCurrent State: %s%s%s  -  Previous State: %s%s%s" % (colorInstanceStatus(currentState), currentState, CLRnormal, colorInstanceStatus(prevState), prevState, CLRnormal))
        elif actionType == "ssh":
            instanceIP = specifiedInstance.public_ip_address
            instanceKey = specifiedInstance.key_name
            homeDir = os.environ['HOME']
            if (debug):
                print("target IP= ", instanceIP)
                print("target key = ", instanceKey)
            if loginuser == "":
                loginuser = DetermineLoginUser(index)
            else:
                pass
                if (debug):
                    print("LoginUser set by user: %s%s%s\n" % (CLRtitle, loginuser, CLRnormal))
            if (nopem):
                if (debug):
                    print("%sNo PEM mode%s  Connect string: %sssh %s@%s%s\n" % (CLRheading, CLRnormal, CLRtitle, loginuser, instanceIP, CLRnormal))
                else:
                    print("%sNo PEM mode%s - connecting without PEM key\n" % (CLRheading, CLRnormal))
                subprocess.call(["ssh {0}@{1}".format(loginuser,instanceIP)], shell=True)
            else:
                if (debug):
                    print("Connect string: %sssh -i %s/.aws/%s.pem %s@%s%s\n" % (CLRtitle, homeDir, instanceKey, loginuser, instanceIP, CLRnormal))
                subprocess.call(["ssh -i {0}/.aws/{1}.pem {2}@{3}".format(homeDir,instanceKey,loginuser, instanceIP)], shell=True)

    sys.exit()

if __name__ == '__main__':
    main()
