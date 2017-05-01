"""Control and connect to AWS EC2 instances from command line.

The AWS Shortcuts (awss) library is a CLI utility allowing listing,
starting, stopping and connecting to AWS EC2 instances by Name or ID.

Modules in this library:

__init__ - Main module providing entry point and core code.
awsc     - Communicates with AWS services.
colors   - Determine color capability, define color vars and theme.
debg     - Debug print functions that execute if debug mode initialized.

URL:       https://github.com/robertpeteuil/aws-shortcuts
Author:    Robert Peteuil   @RobertPeteuil
"""
from __future__ import print_function
from builtins import input
from builtins import range
import argparse
import sys
import operator

import awss.awsc as awsc
import awss.debg as debg
from awss.colors import C_NORM, C_HEAD, C_HEAD2, C_TI, C_WARN, C_ERR, C_STAT

__version__ = '0.9.7'


def main():  # pragma: no cover
    """Collect user args and call command funct.

    Collect command line args and setup environment then call
    function for command specified in args.

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
    """Create ArgumentParser object to parse command line arguments.

    Returns:
        parser (object): containing ArgumentParser data and methods.
    Raises:
        SystemExit: if the user enters invalid args.

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
    """Gather data for instances matching args and call display func.

    Args:
        options (object): contains args and data from parser.

    """
    (i_info, title_out) = gather_data(options)
    if i_info:
        awsc.get_all_aminames(i_info)
        title_out = "Instance List - " + title_out
        list_instances(title_out, i_info)
    else:
        print("No instances found with parameters: {}".format(title_out))


def cmd_startstop(options):
    """Start or Stop the specified instance.

    Finds instances that match args and instance-state expected by the
    command.  Then, the target instance is determined, the action is
    performed on the instance, and the eturn information is displayed.

    Args:
        options (object): contains args and data from parser.

    """
    statelu = {"start": "stopped", "stop": "running"}
    options.inState = statelu[options.command]
    debg.dprint("toggle set state: ", options.inState)
    (i_info, title_out) = gather_data(options)
    (tar_inst, tar_idx) = determine_inst(options.command, i_info, title_out)
    response = awsc.startstop(tar_inst, options.command)
    responselu = {"start": "StartingInstances", "stop": "StoppingInstances"}
    filt = responselu[options.command]
    resp = {}
    state_term = ('CurrentState', 'PreviousState')
    for i, j in enumerate(state_term):
        resp[i] = response["{0}".format(filt)][0]["{0}".format(j)]['Name']
    print("Current State: {}{}{}  -  Previous State: {}{}{}\n".
          format(C_STAT[resp[0]], resp[0], C_NORM,
                 C_STAT[resp[1]], resp[1], C_NORM))


def cmd_ssh(options):
    """Connect to the specified instance via ssh.

    Finds instances that match the user specified args that are also
    in the 'running' state.  The target instance is determined, the
    required connection information is retreived (IP, key and ssh
    user-name), then an 'ssh' connection is made to the instance.

    Args:
        options (object): contains args and data from parser

    """
    import os
    import subprocess
    options.inState = "running"
    (i_info, title_out) = gather_data(options)
    (tar_inst, tar_idx) = determine_inst(options.command, i_info, title_out)
    home_dir = os.environ['HOME']
    if options.user is None:
        tar_aminame = awsc.get_one_aminame(i_info[tar_idx]['ami'])
        options.user = cmd_ssh_user(tar_aminame)
    else:
        debg.dprint("LoginUser set by user: ", options.user)
    if options.nopem:
        debg.dprint("Connect string: ", "ssh {}@{}".
                    format(options.user, i_info[tar_idx]['pub_dns_name']))
        print("{0}No PEM mode{1} - connecting without PEM key\n".
              format(C_HEAD, C_NORM))
        subprocess.call(["ssh {0}@{1}".format(options.user,
                         i_info[tar_idx]['pub_dns_name'])], shell=True)
    else:
        debg.dprint("Connect string: ", "ssh -i {}/.aws/{}.pem {}@{}".
                    format(home_dir, i_info[tar_idx]['ssh_key'], options.user,
                           i_info[tar_idx]['pub_dns_name']))
        print("")
        subprocess.call(["ssh -i {0}/.aws/{1}.pem {2}@{3}".
                        format(home_dir, i_info[tar_idx]['ssh_key'],
                               options.user, i_info[tar_idx]['pub_dns_name'])],
                        shell=True)


def cmd_ssh_user(tar_aminame):
    """Calculate instance login-username based on image-name.

    Args:
        tar_aminame (str): name of the image.
    Returns:
        username (str): name for ssh based on AMI-name.

    """
    # first 5 chars of AMI-name can be anywhere in AMI-Name
    userlu = {"ubunt": "ubuntu", "debia": "admin", "fedor": "root",
              "cento": "centos", "openB": "root"}
    usertmp = [value for key, value in list(userlu.items()) if key in
               tar_aminame.lower()]
    if usertmp:
        username = usertmp[0]
    else:
        username = "ec2-user"
    debg.dprint("loginuser Calculated: ", username)

    return username


def gather_data(options):
    """Get Data specific for command selected.

    Create ec2 specific query and output title based on
    options specified, retrieves the raw response data
    from aws, then processes it into the i_info dict,
    which is used throughout this module.

    Args:
        options (object): contains args and data from parser,
                          that has been adjusted by the command
                          specific functions as appropriate.
    Returns:
        i_info (dict): information on instances and details.
        title_out (str): the title to display before the list.

    """
    (qry_string, title_out) = qry_create(options)
    qry_results = awsc.get_inst_info(qry_string)
    i_info = process_results(qry_results)
    return (i_info, title_out)


def process_results(qry_results):
    """Generate dictionary of results from query.

    Decodes the large dict recturned from the AWS query.

    Args:
        qry_results (dict): results from awsc.get_inst_info
    Returns:
        i_info (dict): information on instances and details.

    """
    i_info = {}
    for i, j in enumerate(qry_results['Reservations']):
        i_info[i] = {'id': j['Instances'][0]['InstanceId']}
        i_info[i]['state'] = j['Instances'][0]['State']['Name']
        i_info[i]['ami'] = j['Instances'][0]['ImageId']
        i_info[i]['ssh_key'] = j['Instances'][0]['KeyName']
        i_info[i]['pub_dns_name'] = j['Instances'][0]['PublicDnsName']
        inst_tags = j['Instances'][0]['Tags']
        tag_dict = {}
        for k in range(len(inst_tags)):
            tag_dict[inst_tags[k]['Key']] = inst_tags[k]['Value']
        i_info[i]['tag'] = tag_dict
    debg.dprint("numInstances: ", len(i_info))
    debg.dprintx("Details except AMI-name")
    debg.dprintx(i_info, True)
    return i_info


def qry_create(options):
    """Create query from the args specified and command chosen.

    Creates a query string that incorporates the args in the options
    object, and creates the title for the 'list' function.

    Args:
        options (object): contains args and data from parser
    Returns:
        qry_string (str): the query to be used against the aws ec2 client.
        title_out (str): the title to display before the list.

    """
    qry_string = filt_end = title_out = ""
    filt_st = "Filters=["
    out_end = "All"
    flag_id = False
    flag_filt = False

    if options.id:
        qry_string += "InstanceIds=['%s']" % (options.id)
        title_out += "id: '%s'" % (options.id)
        flag_id = True
        out_end = ""

    if options.instname:
        (qry_string, title_out) = qry_helper(flag_id, qry_string, title_out)
        flag_filt = True
        filt_end = "]"
        out_end = ""
        qry_string += filt_st + ("{'Name': 'tag:Name', 'Values': ['%s']}"
                                 % (options.instname))
        title_out += "name: '%s'" % (options.instname)

    if options.inState:
        (qry_string, title_out) = qry_helper(flag_filt, qry_string,
                                             title_out, flag_id, filt_st)
        qry_string = (qry_string + "{'Name': 'instance-state-name',"
                      "'Values': ['%s']}" % (options.inState))
        title_out += "state: '%s'" % (options.inState)
        filt_end = "]"
        out_end = ""

    qry_string += filt_end
    title_out += out_end
    debg.dprintx("\nQuery String")
    debg.dprintx(qry_string, True)
    debg.dprint("title_out: ", title_out)
    return(qry_string, title_out)


def qry_helper(flag_filt, qry_string, title_out, flag_id=False, filt_st=""):
    """Dynamically add syntaxtical elements to query.

    This functions adds syntactical elements to the query string, and
    report title, based on the types and number of items added thus far.

    Args:
        flag_filt (bool): at least one filter item specified.
        qry_string (str): portion of the query constructed thus far.
        title_out (str): the title to display before the list.
        flag_id (bool): optional - instance-id was specified.
        filt_st (str): optional - syntax to add on end if filter specified.
    Returns:
        qry_string (str): the portion of the query that was passed in with
                          the appropriate syntactical elements added.
        title_out (str): the title to display before the list.

    """
    if flag_id or flag_filt:
        qry_string += ", "
        title_out += ", "

    if not flag_filt:
        qry_string += filt_st
    return (qry_string, title_out)


def list_instances(title_out, i_info, numbered=False):
    """Display a list of all instances and their details.

    Iterates through all the instances in the dict, and displays
    information for each instance.

    Args:
        title_out (str): the title to display before the list.
        i_info (dict): information on instances and details.
        numbered (bool): optional - indicates wheter the list should be
                         displayed with numbers before each instance.
                         This is used when called from user_picklist.

    """
    if not numbered:
        print("\n{}\n".format(title_out))

    for i in i_info:
        if numbered:
            print("Instance {}#{}{}".format(C_WARN, i + 1, C_NORM))

        print("  {6}Name: {1}{3:<22}{1}ID: {0}{4:<20}{1:<18}Status: {2}{5}{1}".
              format(C_TI, C_NORM, C_STAT[i_info[i]['state']],
                     i_info[i]['tag']['Name'], i_info[i]['id'],
                     i_info[i]['state'], C_HEAD2))
        print("  AMI: {0}{2:<23}{1}AMI Name: {0}{3:.41}{1}".
              format(C_TI, C_NORM, i_info[i]['ami'], i_info[i]['aminame']))
        list_tags(i_info[i]['tag'])
    debg.dprintx("All Data")
    debg.dprintx(i_info, True)


def list_tags(tags):
    """Print tags in dict so they allign with listing above."""
    tags_sorted = sorted(list(tags.items()), key=operator.itemgetter(0))
    c = 1
    padlu = {1: 38, 2: 49}
    for k, v in tags_sorted:
        if k != "Name":
            if c < 3:
                pada = padlu[c]
                sys.stdout.write("  {2}{0}:{3} {1}".
                                 format(k, v, C_HEAD2, C_NORM).ljust(pada))
                c += 1
            else:
                sys.stdout.write("{2}{0}:{3} {1}\n".format(k, v, C_HEAD2,
                                                           C_NORM))
                c = 1
    print("\n")


def determine_inst(command, i_info, title_out):
    """Determine the instance-id of the target instance.

    Inspect the number of instance-ids collected and take the
    appropriate action: exit if no ids, return if single id,
    and call user_picklist function if multiple ids exist.

    Args:
        command (str): command specified on the command line.
        i_info (dict): information and details for instances.
        title_out (str): the title to display in the listing.
    Returns:
        tar_inst (str): the AWS instance-id of the target.
    Raises:
        SystemExit: if no instances are match parameters specified.

    """
    qty_instances = len(i_info)
    if qty_instances == 0:
        print("No instances found with parameters: {}".format(title_out))
        sys.exit(1)

    if qty_instances > 1:
        print("\n{} instances match these parameters:\n".format(qty_instances))
        tar_idx = user_picklist(title_out, i_info, command)

    else:
        tar_idx = 0
    tar_inst = i_info[tar_idx]['id']
    print("\n{0}{3}ing{1} instance id {2}{4}{1}".
          format(C_STAT[command], C_NORM, C_TI, command, tar_inst))
    return (tar_inst, tar_idx)


def user_picklist(title_out, i_info, command):
    """Display list of instances matching args and ask user to select target.

    Instance list displayed and user asked to enter the number corresponding
    to the desired target instance, or '0' to abort.

    Args:
        title_out (str): the title to display before the list.
        i_info (dict): information on instances and details.
        command (str): command specified on the command line.
    Returns:
        tar_idx (int): the dictionary index number of the targeted instance.

    """
    entry_valid = False
    awsc.get_all_aminames(i_info)
    list_instances(title_out, i_info, True)
    msg_txt = ("Enter {0}#{1} of instance to {3} ({0}1{1}-{0}{4}{1})"
               " [{2}0 aborts{1}]: ".format(C_WARN, C_NORM, C_TI,
                                            command, len(i_info)))
    while not entry_valid:
        entry_base = obtain_input(msg_txt)
        try:
            entry_raw = int(entry_base)
        except ValueError:
            entry_raw = 999
        (tar_idx, entry_valid) = user_entry(entry_raw, command, len(i_info))
    print()
    return tar_idx


def obtain_input(message_text):  # pragma: no cover
    """Perform input command as a function so it can be mocked."""
    return (input(message_text))


def user_entry(entry_raw, command, maxqty):
    """Validate user entry and returns index and validity flag.

    Processes the user entry and take the appropriate action: abort
    if '0' entered, set validity flag and index is valid entry, else
    return invalid index and the still unset validity flag.

    Args:
        entry_raw (int): a number entered or 999 if a non-int was entered.
        command (str): program command to display in prompt.
        maxqty (int): the largest valid number that can be entered.
    Returns:
        entry_idx(int): the dictionary index number of the targeted instance
        entry_valid (bool): specifies if entry_idx is valid.
    Raises:
        SystemExit: if the user enters 0 when they are choosing from the
                    list it triggers the "abort" option offered to the user.

    """
    entry_valid = False
    if not entry_raw:
        print("{}aborting{} - {} instance\n".
              format(C_ERR, C_NORM, command))
        sys.exit()
    elif entry_raw >= 1 and entry_raw <= maxqty:
        entry_idx = entry_raw - 1
        entry_valid = True
    else:
        print("{}Invalid entry:{} enter a number between 1"
              " and {}.".format(C_ERR, C_NORM, maxqty))
        entry_idx = entry_raw
    return (entry_idx, entry_valid)


if __name__ == '__main__':
    main()
