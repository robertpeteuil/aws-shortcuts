"""Test module for det_instance function in awss."""

from __future__ import print_function
import mock

from awss.core import cmd_list
import awss.debg as debg

# import ami numbers to names lookup table
from awstidydata import ami_lookup
# import raw query data returned from AWS
from awsrawdata import rawdata

debg.init(False, False)


class holdOptions():
    """Hold options used by qry_create function."""

    def __init__(self, inCommand, idnum, instname=None, inState=None):
        """Initialize options to specified values."""
        self.command = inCommand
        self.id = idnum
        self.instname = instname
        self.inState = inState


def test_determine_inst(capsys):
    """Test list command from entry to exit in awss."""

    qryoptions = holdOptions("list", "i-04a10a9a89f05523d")

    def local_aminames(ami):
        for i in ami:
            ami[i]['aminame'] = ami_lookup[ami[i]['ami']]
        return ami

    def local_gi(qryrec):
        assert qryrec == "InstanceIds=['i-04a10a9a89f05523d']"
        return rawdata

    with mock.patch('awss.awsc.get_all_aminames', local_aminames, create=True):
        with mock.patch('awss.awsc.get_inst_info', local_gi, create=True):
            debg.init(True, True)
            cmd_list(qryoptions)
            out, err = capsys.readouterr()
            assert err == ""
