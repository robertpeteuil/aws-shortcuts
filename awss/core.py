"""Control and connect to AWS EC2 instances from command line.

The AWS Shortcuts (awss) library is a CLI utility allowing listing,
starting, stopping and connecting to AWS EC2 instances by Name or ID.

License:

    AWSS - Control and connect to AWS EC2 instances from command line
    Copyright (C) 2017  Robert Peteuil

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

URL:       https://github.com/robertpeteuil/aws-shortcuts
Author:    Robert Peteuil

"""
from __future__ import print_function
from builtins import input
from builtins import range
import argparse
import sys
import operator

import awss.awsc as awsc
import awss.debg as debg
from awss.colors import C_NORM, C_HEAD2, C_TI, C_WARN, C_ERR, C_STAT

__version__ = '0.9.13'


def main():
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
    print(C_NORM)

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
                                     usage="\tawss {command} [ 'NAME' ] "
                                     "[ '-i ID' ] [ OPTIONS ]\n\t{command} ="
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
                                        "'awss list' will list instances"
                                        " specified using combinations of "
                                        "NAME, instance-id and current-state."
                                        "  If no specifications are given, "
                                        " all instances will be listed."
                                        "  ex: 'awss list TEST "
                                        "-r' will list instances named 'TEST'"
                                        " that are currently running.",
                                        usage="\tawss list [none] [NAME] [-i "
                                        "ID] [-r] [-s] [OPTIONS]")
    parser_list.add_argument('instname', nargs='?', metavar='NAME',
                             help='specify instance by name')
    parser_list.add_argument('-i', '--id', action="store",
                             help='specify instance by id')
    parser_list.add_argument('-s', '--stopped', action='store_const',
                             dest="inst_state", const="stopped",
                             help='list stopped instances')
    parser_list.add_argument('-r', '--running', action='store_const',
                             dest="inst_state", const="running",
                             help='list running instances')
    parser_list.add_argument('-d', '--debug', action="count",
                             default=0, help=argparse.SUPPRESS)
    parser_list.set_defaults(func=cmd_list)

    # Parser for START command
    parser_start = subparsers.add_parser('start', usage="\tawss start [NAME]"
                                         " [-i ID] [-h]",
                                         description="Start an AWS instance"
                                         " from the command line.")
    parser_start.add_argument('instname', nargs='?', metavar='NAME',
                              help='specify instance by name')
    parser_start.add_argument('-i', '--id', action="store",
                              help='specify instance-id')
    parser_start.add_argument('-d', '--debug', action="count",
                              default=0, help=argparse.SUPPRESS)
    parser_start.set_defaults(func=cmd_startstop)

    # Parser for STOP command
    parser_stop = subparsers.add_parser('stop', usage="\tawss stop [NAME]"
                                        " [-i ID] [-h]",
                                        description="Stop an AWS instance"
                                        " from the command line.")
    parser_stop.add_argument('instname', nargs='?', metavar='NAME',
                             help='specify instance by name')
    parser_stop.add_argument('-i', '--id', action="store",
                             help='specify instance-id')
    parser_stop.add_argument('-d', '--debug', action="count",
                             default=0, help=argparse.SUPPRESS)
    parser_stop.set_defaults(func=cmd_startstop)

    # Parser for SSH command
    parser_ssh = subparsers.add_parser('ssh', usage="\tawss ssh [NAME]"
                                       " [-i ID] [-u USER] [-p] [-h]",
                                       description="Connect to an AWS i"
                                       "nstance via ssh.")
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
    (i_info, param_str) = gather_data(options)
    if i_info:
        awsc.get_all_aminames(i_info)
        param_str = "Instance List - " + param_str + "\n"
        list_instances(i_info, param_str)
    else:
        print("No instances found with parameters: {}".format(param_str))


def cmd_startstop(options):
    """Start or Stop the specified instance.

    Finds instances that match args and instance-state expected by the
    command.  Then, the target instance is determined, the action is
    performed on the instance, and the eturn information is displayed.

    Args:
        options (object): contains args and data from parser.

    """
    statelu = {"start": "stopped", "stop": "running"}
    options.inst_state = statelu[options.command]
    debg.dprint("toggle set state: ", options.inst_state)
    (i_info, param_str) = gather_data(options)
    (tar_inst, tar_idx) = determine_inst(i_info, param_str, options.command)
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
    from os.path import expanduser
    options.inst_state = "running"
    (i_info, param_str) = gather_data(options)
    (tar_inst, tar_idx) = determine_inst(i_info, param_str, options.command)
    home_dir = expanduser("~")
    if options.user is None:
        tar_aminame = awsc.get_one_aminame(i_info[tar_idx]['ami'])
        options.user = cmd_ssh_user(tar_aminame,
                                    i_info[tar_idx]['tag']['Name'])
    else:
        debg.dprint("LoginUser set by user: ", options.user)
    os_spec = {"nt": ["powershell plink", "\\", "ppk"]}
    c_itm = os_spec.get(os.name, ["ssh", "/", "pem"])
    cmd_ssh_run = c_itm[0]
    if not options.nopem:
        cmd_ssh_run += (" -i {0}{1}.aws{1}{2}.{3}".
                        format(home_dir, c_itm[1], i_info[tar_idx]['ssh_key'],
                               c_itm[2]))
    else:
        debg.dprint("Connect string: ", "ssh {}@{}".
                    format(options.user, i_info[tar_idx]['pub_dns_name']))
    cmd_ssh_run += " {0}@{1}".format(options.user,
                                     i_info[tar_idx]['pub_dns_name'])
    print(cmd_ssh_run)
    subprocess.call(cmd_ssh_run, shell=True)


def cmd_ssh_user(tar_aminame, inst_name):
    """Calculate instance login-username based on image-name.

    Args:
        tar_aminame (str): name of the image instance created with.
        inst_name (str): name of the instance.
    Returns:
        username (str): name for ssh based on AMI-name.

    """
    if tar_aminame == "Unknown":
        tar_aminame = inst_name
    # first 5 chars of AMI-name can be anywhere in AMI-Name
    userlu = {"ubunt": "ubuntu", "debia": "admin", "fedor": "root",
              "cento": "centos", "openb": "root"}
    usertemp = ['name'] + [value for key, value in list(userlu.items())
                           if key in tar_aminame.lower()]
    usertemp = dict(zip(usertemp[::2], usertemp[1::2]))
    username = usertemp.get('name', 'ec2-user')
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
        param_str (str): the title to display before the list.

    """
    (qry_string, param_str) = qry_create(options)
    qry_results = awsc.get_inst_info(qry_string)
    i_info = process_results(qry_results)
    return (i_info, param_str)


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
        try:
            i_info[i]['tag'] = process_tags(j['Instances'][0]['Tags'])
        except KeyError:
            i_info[i]['tag'] = {"Name": ""}
    debg.dprint("numInstances: ", len(i_info))
    debg.dprintx("Details except AMI-name")
    debg.dprintx(i_info, True)
    return i_info


def process_tags(inst_tags):
    """Create dict of instance tags as only name:value pairs."""
    tag_dict = {}
    for k in range(len(inst_tags)):
        tag_dict[inst_tags[k]['Key']] = inst_tags[k]['Value']
    return tag_dict


def qry_create(options):
    """Create query from the args specified and command chosen.

    Creates a query string that incorporates the args in the options
    object, and creates the title for the 'list' function.

    Args:
        options (object): contains args and data from parser
    Returns:
        qry_string (str): the query to be used against the aws ec2 client.
        param_str (str): the title to display before the list.

    """
    qry_string = filt_end = param_str = ""
    filt_st = "Filters=["
    param_str_default = "All"

    if options.id:
        qry_string += "InstanceIds=['%s']" % (options.id)
        param_str += "id: '%s'" % (options.id)
        param_str_default = ""

    if options.instname:
        (qry_string, param_str) = qry_helper(bool(options.id),
                                             qry_string, param_str)
        filt_end = "]"
        param_str_default = ""
        qry_string += filt_st + ("{'Name': 'tag:Name', 'Values': ['%s']}"
                                 % (options.instname))
        param_str += "name: '%s'" % (options.instname)

    if options.inst_state:
        (qry_string, param_str) = qry_helper(bool(options.id),
                                             qry_string, param_str,
                                             bool(options.instname), filt_st)
        qry_string += ("{'Name': 'instance-state-name',"
                       "'Values': ['%s']}" % (options.inst_state))
        param_str += "state: '%s'" % (options.inst_state)
        filt_end = "]"
        param_str_default = ""

    qry_string += filt_end
    param_str += param_str_default
    debg.dprintx("\nQuery String")
    debg.dprintx(qry_string, True)
    debg.dprint("param_str: ", param_str)
    return(qry_string, param_str)


def qry_helper(flag_id, qry_string, param_str, flag_filt=False, filt_st=""):
    """Dynamically add syntaxtical elements to query.

    This functions adds syntactical elements to the query string, and
    report title, based on the types and number of items added thus far.

    Args:
        flag_filt (bool): at least one filter item specified.
        qry_string (str): portion of the query constructed thus far.
        param_str (str): the title to display before the list.
        flag_id (bool): optional - instance-id was specified.
        filt_st (str): optional - syntax to add on end if filter specified.
    Returns:
        qry_string (str): the portion of the query that was passed in with
                          the appropriate syntactical elements added.
        param_str (str): the title to display before the list.

    """
    if flag_id or flag_filt:
        qry_string += ", "
        param_str += ", "

    if not flag_filt:
        qry_string += filt_st
    return (qry_string, param_str)


def list_instances(i_info, param_str, numbered=False):
    """Display a list of all instances and their details.

    Iterates through all the instances in the dict, and displays
    information for each instance.

    Args:
        i_info (dict): information on instances and details.
        param_str (str): the title to display before the list.
        numbered (bool): optional - indicates wheter the list should be
                         displayed with numbers before each instance.
                         This is used when called from user_picklist.

    """
    print(param_str)

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
    tag_sec_spacer = ""
    c = 1
    ignored_keys = ["Name", "aws:ec2spot:fleet-request-id"]
    pad_col = {1: 38, 2: 49}
    for k, v in tags_sorted:
        # if k != "Name":
        if k not in ignored_keys:
            if c < 3:
                padamt = pad_col[c]
                sys.stdout.write("  {2}{0}:{3} {1}".
                                 format(k, v, C_HEAD2, C_NORM).ljust(padamt))
                c += 1
                tag_sec_spacer = "\n"
            else:
                sys.stdout.write("{2}{0}:{3} {1}\n".format(k, v, C_HEAD2,
                                                           C_NORM))
                c = 1
                tag_sec_spacer = ""
    print(tag_sec_spacer)


def determine_inst(i_info, param_str, command):
    """Determine the instance-id of the target instance.

    Inspect the number of instance-ids collected and take the
    appropriate action: exit if no ids, return if single id,
    and call user_picklist function if multiple ids exist.

    Args:
        i_info (dict): information and details for instances.
        param_str (str): the title to display in the listing.
        command (str): command specified on the command line.
    Returns:
        tar_inst (str): the AWS instance-id of the target.
    Raises:
        SystemExit: if no instances are match parameters specified.

    """
    qty_instances = len(i_info)
    if not qty_instances:
        print("No instances found with parameters: {}".format(param_str))
        sys.exit(1)

    if qty_instances > 1:
        print("{} instances match these parameters:".format(qty_instances))
        tar_idx = user_picklist(i_info, command)

    else:
        tar_idx = 0
    tar_inst = i_info[tar_idx]['id']
    print("{0}{3}ing{1} instance id {2}{4}{1}".
          format(C_STAT[command], C_NORM, C_TI, command, tar_inst))
    return (tar_inst, tar_idx)


def user_picklist(i_info, command):
    """Display list of instances matching args and ask user to select target.

    Instance list displayed and user asked to enter the number corresponding
    to the desired target instance, or '0' to abort.

    Args:
        i_info (dict): information on instances and details.
        command (str): command specified on the command line.
    Returns:
        tar_idx (int): the dictionary index number of the targeted instance.

    """
    valid_entry = False
    awsc.get_all_aminames(i_info)
    list_instances(i_info, "", True)
    msg_txt = ("Enter {0}#{1} of instance to {3} ({0}1{1}-{0}{4}{1})"
               " [{2}0 aborts{1}]: ".format(C_WARN, C_NORM, C_TI,
                                            command, len(i_info)))
    while not valid_entry:
        entry_raw = obtain_input(msg_txt)
        try:
            entry_int = int(entry_raw)
        except ValueError:
            entry_int = 999
        (tar_idx, valid_entry) = user_entry(entry_int, len(i_info), command)
    return tar_idx


def obtain_input(message_text):  # pragma: no cover
    """Perform input command as a function so it can be mocked."""
    return (input(message_text))


def user_entry(entry_int, num_inst, command):
    """Validate user entry and returns index and validity flag.

    Processes the user entry and take the appropriate action: abort
    if '0' entered, set validity flag and index is valid entry, else
    return invalid index and the still unset validity flag.

    Args:
        entry_int (int): a number entered or 999 if a non-int was entered.
        num_inst (int): the largest valid number that can be entered.
        command (str): program command to display in prompt.
    Returns:
        entry_idx(int): the dictionary index number of the targeted instance
        valid_entry (bool): specifies if entry_idx is valid.
    Raises:
        SystemExit: if the user enters 0 when they are choosing from the
                    list it triggers the "abort" option offered to the user.

    """
    valid_entry = False
    if not entry_int:
        print("{}aborting{} - {} instance\n".
              format(C_ERR, C_NORM, command))
        sys.exit()
    elif entry_int >= 1 and entry_int <= num_inst:
        entry_idx = entry_int - 1
        valid_entry = True
    else:
        print("{}Invalid entry:{} enter a number between 1"
              " and {}.".format(C_ERR, C_NORM, num_inst))
        entry_idx = entry_int
    return (entry_idx, valid_entry)


if __name__ == '__main__':
    main()
