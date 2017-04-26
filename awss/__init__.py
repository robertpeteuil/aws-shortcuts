#!/usr/bin/env python

"""
    awss - Control AWS instances from command line: list, start, stop or ssh
        https://github.com/robertpeteuil/aws-shortcuts

    Author: Robert Peteuil   @RobertPeteuil

"""

from __future__ import print_function
from builtins import range
import argparse
import sys
from awss.colors import CLRnormal, CLRheading, CLRtitle, CLRwarning, \
    CLRerror, statCLR
from awss.getchar import _Getch
import awss.awsc as awsc
import awss.debg as debg

__version__ = '0.9.5.5'


def main():
    """
    Main sets up the parser, retreives user options, sets debug modes,
    initializes external debug and awsc modules, then calls the module
    for the specified comamnd.
    """

    parser = parser_setup()
    options = parser.parse_args()

    debug = bool(options.debug > 0)
    debugall = bool(options.debug > 1)

    awsc.init()
    debg.init(debug, debugall)

    options.func(options)

    sys.exit()


def parser_setup():
    """
    Sets up the command line parser and four subparsers, one for each command:
    list, start, stop and ssh.
    """

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
    parser_list.set_defaults(func=cmd_list)

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
    parser_start.set_defaults(func=cmd_startstop)

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
    parser_stop.set_defaults(func=cmd_startstop)

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
    parser_ssh.set_defaults(func=cmd_ssh)
    return parser


def cmd_list(options):
    """
    'list' executer: input: object - created by the parser

    Finds instances that match the user specified args and displays them.
    """

    (qry_string, title_out) = qry_create(options)
    i_info = awsc.getids(qry_string)
    items = len(i_info)
    if items > 0:
        i_info = awsc.getdetails(i_info)
        title_out = "Instance List - " + title_out
        list_instances(title_out, i_info)
    else:
        print("No instances found with parameters: %s" % (title_out))


def cmd_startstop(options):
    """
    'start' and 'stop' executer: input: object - created by the parser

    Finds instances that match the user specified args plus the command
    specific args.  The target instance is determined and the specified
    action is applied to the instance. The action return information is
    retreived and displayed.
    """

    statelu = {"start": "stopped", "stop": "running"}
    options.inState = statelu[options.command]
    debg.dprint("toggle set state: ", options.inState)
    (qry_string, title_out) = qry_create(options)
    qry_check(qry_string)
    i_info = awsc.getids(qry_string)
    (tar_inst, tar_idx) = det_instance(options.command, i_info, title_out)
    response = awsc.startstop(tar_inst, options.command)
    responselu = {"start": "StartingInstances", "stop": "StoppingInstances"}
    filt = responselu[options.command]
    resp = {}
    state_term = ('CurrentState', 'PreviousState')
    for i, j in enumerate(state_term):
        resp[i] = response["{0}".format(filt)][0]["{0}".format(j)]['Name']
    print("\tCurrent State: %s%s%s  -  Previous State: %s%s%s\n" %
          (statCLR[resp[0]], resp[0], CLRnormal,
           statCLR[resp[1]], resp[1], CLRnormal))


def cmd_ssh(options):
    """
    'ssh' executer: input: object - created by the parser

    Finds instances that match the user specified args that are also
    in the 'running' state.  The target instance is determined, the
    required connection information is retreived (IP, key used, ssh
    user-name), and an 'ssh' connection is made to the instance.
    """

    import os
    import subprocess
    options.inState = "running"
    (qry_string, title_out) = qry_create(options)
    qry_check(qry_string)
    i_info = awsc.getids(qry_string)
    (tar_inst, tar_idx) = det_instance(options.command, i_info, title_out)
    (inst_ip, inst_key, inst_img_id) = awsc.getsshinfo(tar_inst)
    home_dir = os.environ['HOME']
    if options.user is None:
        i_info[tar_idx]['aminame'] = awsc.getaminame(inst_img_id)
        # only first 5 chars of AMI-name used to avoid version numbers
        userlu = {"ubunt": "ubuntu", "debia": "admin", "fedor": "fedora",
                  "cento": "centos", "openB": "root"}
        options.user = userlu.get(i_info[tar_idx]['aminame'][:5], "ec2-user")
        debg.dprint("loginuser Calculated: ", options.user)
    else:
        debg.dprint("LoginUser set by user: ", options.user)
    if options.nopem:
        debg.dprint("Connect string: ", "ssh %s@%s" %
                    (options.user, inst_ip))
        print("%sNo PEM mode%s - connecting without PEM key\n" % (CLRheading,
                                                                  CLRnormal))
        subprocess.call(["ssh {0}@{1}".format(options.user, inst_ip)],
                        shell=True)
    else:
        debg.dprint("Connect string: ", "ssh -i %s/.aws/%s.pem %s@%s" %
                    (home_dir, inst_key, options.user, inst_ip))
        print("")
        subprocess.call(["ssh -i {0}/.aws/{1}.pem {2}@{3}".
                         format(home_dir, inst_key, options.user,
                                inst_ip)], shell=True)


def qry_check(qry_string):
    """
    Query String Validator:  input: query string - in aws ec2 format

    Check if the generated query string is empty, and if so exits.
    This is executed by the 'start', 'stop', and 'ssh' command as they must
    target a specific instance.
    """

    if qry_string == "ec2C.describe_instances()":
        print("%sError%s - instance identifier not specified" %
              (CLRerror, CLRnormal))
        sys.exit(1)
    else:
        return


def qry_create(options):
    """
    Query Creator: input: object - created by the parser
                   returns: Query_String, Report_Title

    Creates aws ec2 formatted query string that incorporates the args in the
    options object.  Generation of this query on the fly allows for queries
    that search and/or filter on multiple properties in the same query.

    This function also generates the report output title for the 'list'
    function as the creation of it uses the exact same algoruthm as creating
    the query.
    """

    qry_string = "ec2C.describe_instances("
    filt_start = "Filters=["
    filt_end = ""
    title_out = ""
    out_end = "All"
    i = False
    n = False
    if options.id:
        qry_string = qry_string + "InstanceIds=['%s']" % (options.id)
        title_out = title_out + "id: '%s'" % (options.id)
        i = True
        out_end = ""
    if options.instname:
        (qry_string, title_out) = qry_helper(i, qry_string, title_out)
        n = True
        filt_end = "]"
        out_end = ""
        qry_string = qry_string + filt_start + ("{'Name': 'tag:Name',"
                                                " 'Values': ['%s']}"
                                                % (options.instname))
        title_out = title_out + "name: '%s'" % (options.instname)
    if options.inState:
        (qry_string, title_out) = qry_helper(n, qry_string, title_out, i,
                                             filt_start)
        qry_string = (qry_string + "{'Name': 'instance-state-name',"
                      "'Values': ['%s']}" % (options.inState))
        title_out = title_out + "state: '%s'" % (options.inState)
        filt_end = "]"
        out_end = ""
    qry_string = qry_string + filt_end + ")"
    title_out = title_out + out_end
    debg.dprintx("\nQuery String")
    debg.dprintx(qry_string, True)
    debg.dprint("title_out: ", title_out)
    return(qry_string, title_out)


def qry_helper(n, qry_string, title_out, i=False, filt_start=""):
    """
    Query helper: input: filter_set_flag, query_string, report_title,
                         id_set_flag (optional), string_flag (option)
                  returns: query_string, report_title

    This functions adds syntactical elements to the query string, and
    report title, based on the types and number of items added thus far.
    It is broken-out into a seperate function to eliminate duplication.
    """

    if i or n:
        qry_string = qry_string + ", "
        title_out = title_out + ", "
    if not n:
        qry_string = qry_string + filt_start
    return (qry_string, title_out)


def list_instances(title_out, i_info, numbered="no"):
    """
    Displays Instance Information:
        input: report_title, dict of inst_info, and
            special_case_flag(optional)

    This function iterates through all the instances contained in the
    i_info dict, displayed the information contained, and also obtained
    the name of the EC2 image that was used to create the instance.  The
    image name is not retreived until it is certain it is needed because
    retrieving it is relatively slow.

    If the special_case flag is set, it means this function is being called
    to display a list for a user to select from.  In this case, a colored
    number is displayed before each instances data.
    """

    if numbered == "no":
        print("\n%s\n" % (title_out))
    for i in range(len(i_info)):
        if numbered == "yes":
            print("Instance %s#%s%s" % (CLRwarning, i + 1, CLRnormal))
        i_info[i]['aminame'] = awsc.getaminame(i_info[i]['ami'])
        print("\tName: %s%s%s\t\tID: %s%s%s\t\tStatus: %s%s%s" %
              (CLRtitle, i_info[i]['name'], CLRnormal, CLRtitle,
               i_info[i]['id'], CLRnormal, statCLR[i_info[i]['state']],
               i_info[i]['state'], CLRnormal))
        print("\tAMI: %s%s%s\tAMI Name: %s%s%s\n" %
              (CLRtitle, i_info[i]['ami'], CLRnormal, CLRtitle,
               i_info[i]['aminame'], CLRnormal))
    debg.dprintx("All Data")
    debg.dprintx(i_info, True)


def det_instance(command, i_info, title_out):
    """
    Determine Target Instance ID:
            input: command, dict of instance info, report_title
            returns: instance-id-of-target-instance, dict-index-of-target

    This functions inspects the dict of instance-ids:
    if it is empty, it displays a message that no instances were found that
    matched the query conditions specified, then exits.
    If it contains one item, then the instance-id of that item is returned.
    If it contains more than one item, then the picklist function is called.
    note: command, and report_title are only used for user display purposes.
    """

    if len(i_info) == 0:
        print("No instances found with parameters: %s" % (title_out))
        sys.exit()
    if len(i_info) > 1:
        print("\n%s instances match these parameters:\n" % (len(i_info)))
        tar_idx = user_picklist(title_out, i_info, command)
    else:
        tar_idx = 0
    tar_inst = i_info[tar_idx]['id']
    print("\n%s%sing%s instance id %s%s%s" % (statCLR[command],
                                              command, CLRnormal,
                                              CLRtitle, tar_inst, CLRnormal))
    return (tar_inst, tar_idx)


def user_picklist(title_out, i_info, command):
    """
    Picklist Function:
            input: report_title, dict of instance info, command
            returns: dictionary-index-of-target

    Display Matching Instances and askd user t0 select target.  The list is
    displayed by calling the list_instances func with the special_flag set.
    Once the list is displayed, the user will be requires to enter a number
    between 1 and the number of matchign instances (or a '0' to abort).
    Entering a number outside of this range generates an invalid selection
    error message, and the user is asked again.
    """

    getch = _Getch()
    entry_valid = "False"
    i_info = awsc.getdetails(i_info)
    list_instances(title_out, i_info, "yes")
    while entry_valid != "True":
        sys.stdout.write("Enter %s#%s of instance to %s (%s1%s-%s%i%s) [%s0"
                         " aborts%s]: " % (CLRwarning, CLRnormal, command,
                                           CLRwarning, CLRnormal, CLRwarning,
                                           len(i_info), CLRnormal, CLRtitle,
                                           CLRnormal))
        entry_raw = getch.int()
        keyconvert = {"999": "invalid entry"}
        entry_display = keyconvert.get(str(entry_raw), entry_raw)
        sys.stdout.write(str(entry_display))
        (tar_idx, entry_valid) = user_entry(entry_raw, command, len(i_info))
    print()
    return tar_idx


def user_entry(entry_raw, command, maxqty):
    """
    User Entry Validation: input: user_entry, command, max_valid_entry

    This function validates the user entry:
    If it is 0, an abort message is diaplyed and the program exits.
    If the entry is between 1 and max_valid_entry, then one is subtracted
    (because its a zero based index) and it is set as the dict-index-of-
    target and the entry_valid flag is set.
    Otherwise the entry is invlid, and the functions returns the invalid_
    value and the entry_valid flag remains False.
    """

    entry_valid = "False"
    entry_int = int(entry_raw)
    if entry_int == 0:
        print("\n\n%saborting%s - %s instance\n" %
              (CLRerror, CLRnormal, command))
        sys.exit()
    elif entry_int >= 1 and entry_int <= maxqty:
        entry_idx = entry_int - 1
        entry_valid = "True"
    else:
        sys.stdout.write("\n%sInvalid entry:%s enter a number between 1"
                         " and %s.\n" % (CLRerror, CLRnormal, maxqty))
        entry_idx = entry_int
    return (entry_idx, entry_valid)


if __name__ == '__main__':
    main()
