"""Test module for det_instance function in awss."""

from __future__ import print_function
import pytest
import mock

from awss.core import determine_inst
import awss.debg as debg

# import ami numbers to names lookup table
from awsstestdata import ami_lookup

debg.init(False, False)


@pytest.mark.parametrize(("ids", "kys", "expct_inst", "expct_idx"), [
    ({0: {'ami': 'ami-16efb076',
          'id': 'i-0c875fafa1e71327b',
          'pub_dns_name': '',
          'ssh_key': 'robert',
          'state': 'stopped',
          'tag': {'Name': 'Ubuntu', 'Role': 'Test'}},
      1: {'ami': 'ami-3e21725e',
          'id': 'i-0c459a77e113c6c9c',
          'pub_dns_name': '',
          'ssh_key': 'robert',
          'state': 'stopped',
          'tag': {'Name': 'Ubuntu'}},
      2: {'ami': 'ami-e09acc80',
          'id': 'i-0014d16e7f68ce746',
          'pub_dns_name': '',
          'ssh_key': 'robert',
          'state': 'stopped',
          'tag': {'Name': 'Suse', 'Role': 'Test'}},
      3: {'ami': 'ami-165a0876',
          'id': 'i-03120c2544fdf5b6f',
          'pub_dns_name': '',
          'ssh_key': 'robert',
          'state': 'stopped',
          'tag': {'Name': 'Amazon', 'Role': 'Test'}},
      4: {'ami': 'ami-2cade64c',
          'id': 'i-0341963e139617c75',
          'pub_dns_name': '',
          'ssh_key': 'robert',
          'state': 'stopped',
          'tag': {'Name': 'RHEL', 'Role': 'Test'}}},
     ['a', 'P', '.', '9', '3'],
     'i-0014d16e7f68ce746', 2),
    ({0: {'ami': 'ami-2cade64c',
          'id': 'i-0341963e139617c75',
          'pub_dns_name': '',
          'ssh_key': 'robert',
          'state': 'stopped',
          'tag': {'Name': 'RHEL', 'Role': 'Test'}}},
     ['1'],
     'i-0341963e139617c75', 0),
    ({0: {'ami': 'ami-16efb076',
          'id': 'i-0c875fafa1e71327b',
          'pub_dns_name': '',
          'ssh_key': 'robert',
          'state': 'stopped',
          'tag': {'Name': 'Ubuntu', 'Role': 'Test'}},
      1: {'ami': 'ami-165a0876',
          'id': 'i-03120c2544fdf5b6f',
          'pub_dns_name': '',
          'ssh_key': 'robert',
          'state': 'stopped',
          'tag': {'Name': 'Amazon', 'Role': 'Test'}}},
     ['a', '7', '0'],
     0, 0),
    ({}, ['1'],
     0, 0)])
def test_determine_inst(ids, kys, expct_inst, expct_idx):
    """Test valid and invalid params with det_instance function in awss."""
    global counter
    counter = 0

    def local_aminames(ami):
        for i in ami:
            ami[i]['aminame'] = ami_lookup[ami[i]['ami']]
        return ami

    def local_input(item1):
        global counter
        keye = kys[counter]
        counter += 1
        return keye

    with mock.patch('awss.awsc.get_all_aminames', local_aminames, create=True):
        with mock.patch('awss.core.obtain_input', local_input, create=True):
            if expct_inst:
                debg.init(True, True)
                (tar_inst, tar_idx) = determine_inst(ids, "TEST", "ssh")
                assert tar_inst == expct_inst
                assert tar_idx == expct_idx
            else:
                with pytest.raises(SystemExit):
                    debg.init(True, True)
                    tar_inst = determine_inst(ids, "TEST", "ssh")
                    pass
