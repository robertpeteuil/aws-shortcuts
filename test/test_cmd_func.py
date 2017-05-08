"""Test module for cmd_functions in awss."""

from __future__ import print_function
import mock
import pytest
from os.path import expanduser
import os

import awss.debg as debg

# ami numbers to names lookup table
from awsstestdata import ami_lookup
# expected info extracted from raw data
from awsstestdata import expected_info
# response received when stopping and starting instances
from awsresponse import stop_resp, start_resp
# raw query data returned from AWS
from awsresponse import rawdata, rawnodata

# home_dir is used by ssh function to look for the PEM key.
home_dir = expanduser("~")


class holdOptions():
    """Hold options used by cmd_function function."""

    def __init__(self, inCommand, idin, instname=None, inst_state=None,
                 inUser=None, inPem=False):
        """Initialize options to specified values."""
        self.command = inCommand
        self.id = idin
        self.instname = instname
        self.inst_state = inst_state
        self.user = inUser
        self.nopem = inPem


def l_allami(ami):
    for i in ami:
        ami[i]['aminame'] = ami_lookup[ami[i]['ami']]
    return ami


@pytest.mark.parametrize(("cmd", "qrystr", "idnum", "idname", "val"), [
    ("list", "InstanceIds=['i-04a10a9a89f05523d']",
     "i-04a10a9a89f05523d", "", 1),
    ("list", "Filters=[{'Name': 'tag:Name', 'Values': ['server']}]",
     "", "server", 0)])
@mock.patch('awss.awsc.get_all_aminames', l_allami, create=True)
def test_list_inst(capsys, cmd, qrystr, idnum, idname, val):
    """Test list command with a specific queries to match raw data.

    Tests for both normal listing, and listing when no instances
    have been found.
    """

    qryoptions = holdOptions(cmd, idnum, idname)

    def l_getinfo(qryrec):
        assert qryrec == qrystr
        if val:
            retinfo = rawdata
        else:
            retinfo = rawnodata
        return retinfo

    with mock.patch('awss.awsc.get_inst_info', l_getinfo, create=True):
        debg.init(True, True)
        from awss.core import cmd_list
        cmd_list(qryoptions)


@pytest.mark.parametrize(("cmd", "qrystr", "exp_resp"), [
    ("stop", "InstanceIds=['i-04a10a9a89f05523d'], Filters=[{'Name':"
     " 'instance-state-name','Values': ['running']}]", stop_resp),
    ("start", "InstanceIds=['i-04a10a9a89f05523d'], Filters=[{'Name':"
     " 'instance-state-name','Values': ['stopped']}]", start_resp)])
@mock.patch('awss.awsc.get_all_aminames', l_allami, create=True)
def test_startstop(capsys, cmd, qrystr, exp_resp):
    """Test startstop with a specific instance # to match raw data."""

    idnum = "i-04a10a9a89f05523d"

    qryoptions = holdOptions(cmd, idnum)

    def l_getinfo(qryrec):
        assert qryrec == qrystr
        return rawdata

    def l_toggle(instif, command):
        return exp_resp

    with mock.patch('awss.awsc.get_inst_info', l_getinfo, create=True):
        with mock.patch('awss.awsc.startstop', l_toggle, create=True):
            debg.init(True, True)
            from awss.core import cmd_startstop
            cmd_startstop(qryoptions)


def l_gami(ami_num):
    amiName = ami_lookup[ami_num]
    return amiName


@pytest.mark.parametrize(("cmd", "qrystr", "cmd_lin", "cmd_win",
                          "iuser", "ipem"), [
    ("ssh", "InstanceIds=['i-04a10a9a89f05523d'], Filters=[{'Name':"
     " 'instance-state-name','Values': ['running']}]",
     "ssh -i {0}/.aws/james.pem root@{1}".
     format(home_dir, expected_info[0]['pub_dns_name']),
     "powershell plink -i {0}\.aws\james.ppk root@{1}".
     format(home_dir, expected_info[0]['pub_dns_name']),
     None, ""),
    ("ssh", "InstanceIds=['i-04a10a9a89f05523d'], Filters=[{'Name':"
     " 'instance-state-name','Values': ['running']}]",
     "ssh root@{0}".format(expected_info[0]['pub_dns_name']),
     "powershell plink root@{0}".format(expected_info[0]['pub_dns_name']),
     None, "-p"),
    ("ssh", "InstanceIds=['i-04a10a9a89f05523d'], Filters=[{'Name':"
     " 'instance-state-name','Values': ['running']}]",
     "ssh -i {0}/.aws/james.pem adminuser@{1}".
     format(home_dir, expected_info[0]['pub_dns_name']),
     "powershell plink -i {0}\.aws\james.ppk adminuser@{1}".
     format(home_dir, expected_info[0]['pub_dns_name']),
     "adminuser", "")])
@mock.patch('awss.awsc.get_one_aminame', l_gami, create=True)
def test_ssh(capsys, cmd, qrystr, cmd_lin, cmd_win, iuser, ipem):
    """Test ssh in modes: normal, specified username, and no pem-key."""

    idnum = "i-04a10a9a89f05523d"

    qryoptssh = holdOptions(cmd, idnum, None, None, iuser, ipem)

    def l_getinfo(qryrec):
        assert qryrec == qrystr
        return rawdata

    def l_scall(datain, shell):
        global rec_response
        rec_response = datain
        return

    if os.name == 'nt':
        sshcmd = cmd_win
    else:
        sshcmd = cmd_lin

    with mock.patch('awss.awsc.get_inst_info', l_getinfo, create=True):
        with mock.patch('subprocess.call', l_scall, create=True):
            debg.init(True, True)
            from awss.core import cmd_ssh
            cmd_ssh(qryoptssh)
            assert rec_response == sshcmd  # noqa
