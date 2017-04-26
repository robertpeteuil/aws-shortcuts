#!/usr/bin/env python

'''
This runs the display list function using sample data.
'''

from __future__ import print_function
import mock

from awss import list_instances
import awss.debg as debg

debg.init(True, True)


amiNameList = {
    'ami-16efb076': 'ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64',
    'ami-3e21725e': 'ubuntu/images/hvm-ssd/ubuntu-trusty-14.04-amd64',
    'ami-e09acc80': 'suse-sles-12-sp2-v20161214-hvm-ssd-x86_64',
    'ami-165a0876': 'amzn-ami-hvm-2016.09.1.20170119-x86_64-gp2',
    'ami-2cade64c': 'RHEL-7.3_HVM_GA-20161026-x86_64-1-Hourly2-GP2'}


def getlocalaminame(ami):
    amiName = amiNameList[ami]
    return amiName


infoIdsOnly = {
    0: {'id': 'i-0c875fafa1e71327b'},
    1: {'id': 'i-03120c2544fdf5b6f'},
    2: {'id': 'i-0014d16e7f68ce746'},
    3: {'id': 'i-0c459a77e113c6c9c'},
    4: {'id': 'i-0341963e139617c75'}}


infoNoAmiName = {
    0: {'ami': 'ami-16efb076', 'id': 'i-0c875fafa1e71327b', 'name': 'Ubuntu',
        'state': 'running'},
    1: {'ami': 'ami-165a0876', 'id': 'i-03120c2544fdf5b6f', 'name': 'Amazon',
        'state': 'running'},
    2: {'ami': 'ami-e09acc80', 'id': 'i-0014d16e7f68ce746', 'name': 'Suse',
        'state': 'stopped'},
    3: {'ami': 'ami-3e21725e', 'id': 'i-0c459a77e113c6c9c', 'name': 'Ubuntu',
        'state': 'stopping'},
    4: {'ami': 'ami-2cade64c', 'id': 'i-0341963e139617c75', 'name': 'RHEL',
        'state': 'stopped'}}


@mock.patch('awss.awsc.getaminame', getlocalaminame, create=True)
def test_display_list(capsys):
    with capsys.disabled():
        print("TEST - Display_List")
    outputTitle = "Test Report"
    list_instances(outputTitle, infoNoAmiName)
    out, err = capsys.readouterr()
    assert err == ""
