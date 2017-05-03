"""Test module for cmd_functions in awss."""

from __future__ import print_function
import mock
import pytest
from os.path import expanduser

import awss.debg as debg

# import ami numbers to names lookup table
from awstidydata import ami_lookup
# import response received when stopping and starting instances
from awstidydata import stop_resp, start_resp
# import expected info extracted from raw data
from awstidydata import expected_info
# import raw query data returned from AWS
from awsrawdata import rawdata

debg.init(False, False)
home_dir = expanduser("~")


class holdOptions():
    """Hold options used by cmd_function function."""

    def __init__(self, inCommand, idin, instname=None, inState=None,
                 inUser=None, inPem=False):
        """Initialize options to specified values."""
        self.command = inCommand
        self.id = idin
        self.instname = instname
        self.inState = inState
        self.user = inUser
        self.nopem = inPem


def l_gami(ami_num):
    amiName = ami_lookup[ami_num]
    return amiName


def l_allami(ami):
    for i in ami:
        ami[i]['aminame'] = ami_lookup[ami[i]['ami']]
    return ami


@pytest.mark.parametrize(("cmd", "qrystr", "exp_resp", "sshcmd"), [
    ("list", "InstanceIds=['i-04a10a9a89f05523d']", "", ""),
    ("stop", "InstanceIds=['i-04a10a9a89f05523d'], Filters=[{'Name':"
     " 'instance-state-name','Values': ['running']}]", stop_resp, ""),
    ("start", "InstanceIds=['i-04a10a9a89f05523d'], Filters=[{'Name':"
     " 'instance-state-name','Values': ['stopped']}]", start_resp, ""),
    ("ssh", "InstanceIds=['i-04a10a9a89f05523d'], Filters=[{'Name':"
     " 'instance-state-name','Values': ['running']}]", "",
     "ssh -i {0}/.aws/james.pem root@{1}".
     format(home_dir, expected_info[0]['pub_dns_name']))])
@mock.patch('awss.awsc.get_all_aminames', l_allami, create=True)
@mock.patch('awss.awsc.get_one_aminame', l_gami, create=True)
def test_determine_inst(capsys, cmd, qrystr, exp_resp, sshcmd):
    """Test commands with a specific instance # to match our raw data."""

    idnum = "i-04a10a9a89f05523d"

    qryoptions = holdOptions(cmd, idnum)

    def l_getinfo(qryrec):
        assert qryrec == qrystr
        return rawdata

    def l_toggle(instif, command):
        return exp_resp

    def l_scall(datain, shell):
        global rec_response
        rec_response = datain[0]
        return

    with mock.patch('awss.awsc.get_inst_info', l_getinfo, create=True):
        with mock.patch('awss.awsc.startstop', l_toggle, create=True):
            with mock.patch('subprocess.call', l_scall, create=True):
                debg.init(True, True)
                if cmd == "list":
                    from awss.core import cmd_list
                    cmd_list(qryoptions)
                elif cmd == "stop" or cmd == "start":
                    from awss.core import cmd_startstop
                    cmd_startstop(qryoptions)
                elif cmd == "ssh":
                    from awss.core import cmd_ssh
                    cmd_ssh(qryoptions)
                    assert rec_response == sshcmd
