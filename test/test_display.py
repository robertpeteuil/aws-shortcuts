"""Test module for list_instances function in awss."""

from __future__ import print_function

from awss import list_instances
import awss.debg as debg


infoAll = {
    0: {'ami': 'ami-16efb076',
        'aminame': 'ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64',
        'id': 'i-0c875fafa1e71327b',
        'pub_dns_name': '',
        'ssh_key': 'robert',
        'state': 'stopped',
        'tag': {'Name': 'Ubuntu', 'Role': 'Test'}},
    1: {'ami': 'ami-3e21725e',
        'aminame': 'ubuntu/images/hvm-ssd/ubuntu-trusty-14.04-amd64',
        'id': 'i-0c459a77e113c6c9c',
        'pub_dns_name': '',
        'ssh_key': 'robert',
        'state': 'stopped',
        'tag': {'Name': 'Ubuntu'}},
    2: {'ami': 'ami-e09acc80',
        'aminame': 'suse-sles-12-sp2-v20161214-hvm-ssd-x86_64',
        'id': 'i-0014d16e7f68ce746',
        'pub_dns_name': '',
        'ssh_key': 'robert',
        'state': 'stopped',
        'tag': {'Name': 'Suse', 'Role': 'Test'}},
    3: {'ami': 'ami-165a0876',
        'aminame': 'amzn-ami-hvm-2016.09.1.20170119-x86_64-gp2',
        'id': 'i-03120c2544fdf5b6f',
        'pub_dns_name': '',
        'ssh_key': 'robert',
        'state': 'stopped',
        'tag': {'Name': 'Amazon', 'Role': 'Test'}},
    4: {'ami': 'ami-2cade64c',
        'aminame': 'RHEL-7.3_HVM_GA-20161026-x86_64-1-Hourly2-GP2',
        'id': 'i-0341963e139617c75',
        'pub_dns_name': '',
        'ssh_key': 'robert',
        'state': 'stopped',
        'tag': {'Name': 'RHEL', 'Role': 'Test'}}}


def test_display_list(capsys):
    """Test list_instances function in awss."""
    debg.init(False, False)
    outputTitle = "Test Report"
    list_instances(outputTitle, infoAll)
    out, err = capsys.readouterr()
    assert err == ""
