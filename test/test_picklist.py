"""Test module for det_instance function in awss."""

from __future__ import print_function
import pytest
import mock

from awss import determine_inst
import awss.debg as debg

debg.init(False, False)


@pytest.mark.parametrize(("ids", "kys", "anames", "ide", "tidx"), [
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
     {'ami-16efb076': 'ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64',
      'ami-3e21725e': 'ubuntu/images/hvm-ssd/ubuntu-trusty-14.04-amd64',
      'ami-e09acc80': 'suse-sles-12-sp2-v20161214-hvm-ssd-x86_64',
      'ami-165a0876': 'amzn-ami-hvm-2016.09.1.20170119-x86_64-gp2',
      'ami-2cade64c': 'RHEL-7.3_HVM_GA-20161026-x86_64-1-Hourly2-GP2'},
     'i-0014d16e7f68ce746', 2),
    ({0: {'ami': 'ami-2cade64c',
          'id': 'i-0341963e139617c75',
          'pub_dns_name': '',
          'ssh_key': 'robert',
          'state': 'stopped',
          'tag': {'Name': 'RHEL', 'Role': 'Test'}}},
     ['1'],
     {'ami-2cade64c': 'RHEL-7.3_HVM_GA-20161026-x86_64-1-Hourly2-GP2'},
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
     {'ami-16efb076': 'ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64',
      'ami-165a0876': 'amzn-ami-hvm-2016.09.1.20170119-x86_64-gp2'},
     0, 0),
    ({}, ['1'], {},
     0, 0)])
def test_determine_inst(ids, kys, anames, ide, tidx):
    """Test valid and invalid params with det_instance function in awss."""
    global counter
    counter = 0

    def getlclaminame(ami):
        for i in ami:
            ami[i]['aminame'] = anames[ami[i]['ami']]
        return ami

    def RetKey(item1):
        global counter
        keye = kys[counter]
        counter += 1
        return keye

    with mock.patch('awss.awsc.get_all_aminames', getlclaminame, create=True):
        with mock.patch('awss.obtain_input', RetKey, create=True):
            if ide:
                debg.init(True, True)
                (tar_inst, tar_idx) = determine_inst("ssh", ids, "TEST")
                assert tar_inst == ide
                assert tar_idx == tidx
            else:
                with pytest.raises(SystemExit):
                    debg.init(True, True)
                    tar_inst = determine_inst("ssh", ids, "TEST")
                    pass
