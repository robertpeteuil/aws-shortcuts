#!/usr/bin/env python

from __future__ import print_function
from builtins import range
import pytest
import mock

from awss.colors import CLRnormal, CLRheading, CLRtitle, CLRwarning, \
    CLRerror, statCLR
import awss.awsc as awsc
import awss.debg as debg
from awss import determineTarget, userPicklist, displayList, userKeyEntry

debg.init()  # turn off debug-print messages


@pytest.mark.parametrize(("ids", "kys", "anames", "ilist", "ide", "idx"), [
    ({0: {'id': 'i-0c875fafa1e71327b'},
     1: {'id': 'i-03120c2544fdf5b6f'},
     2: {'id': 'i-0014d16e7f68ce746'},
     3: {'id': 'i-0c459a77e113c6c9c'},
     4: {'id': 'i-0341963e139617c75'}},
     ['a', 'P', '.', '9', '3'],
     {'ami-16efb076': 'ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64',
      'ami-3e21725e': 'ubuntu/images/hvm-ssd/ubuntu-trusty-14.04-amd64',
      'ami-e09acc80': 'suse-sles-12-sp2-v20161214-hvm-ssd-x86_64',
      'ami-165a0876': 'amzn-ami-hvm-2016.09.1.20170119-x86_64-gp2',
      'ami-2cade64c': 'RHEL-7.3_HVM_GA-20161026-x86_64-1-Hourly2-GP2'},
     {0: {'ami': 'ami-16efb076', 'id': 'i-0c875fafa1e71327b', 'name': 'Ubuntu',
          'state': 'running'},
      1: {'ami': 'ami-165a0876', 'id': 'i-03120c2544fdf5b6f', 'name': 'Amazon',
          'state': 'running'},
      2: {'ami': 'ami-e09acc80', 'id': 'i-0014d16e7f68ce746', 'name': 'Suse',
          'state': 'running'},
      3: {'ami': 'ami-3e21725e', 'id': 'i-0c459a77e113c6c9c', 'name': 'Ubuntu',
          'state': 'running'},
      4: {'ami': 'ami-2cade64c', 'id': 'i-0341963e139617c75', 'name': 'RHEL',
          'state': 'running'}},
     'i-0014d16e7f68ce746', 2),
    ({0: {'id': 'i-0341963e139617c75'}},
     ['1'],
     {'ami-2cade64c': 'RHEL-7.3_HVM_GA-20161026-x86_64-1-Hourly2-GP2'},
     {0: {'ami': 'ami-2cade64c', 'id': 'i-0341963e139617c75', 'name': 'RHEL',
          'state': 'running'}},
     'i-0341963e139617c75', 0),
    ({}, ['1'], {}, {}, '0', 0)])
def test_det_target(ids, kys, anames, ilist, ide, idx):
    global counter
    counter = 0

    def getlocaldetails(info):
        return ilist

    def getlocalaminame(ami):
        amiName = anames[ami]
        return amiName

    def RetKey(item1):
        global counter
        keye = kys[counter]
        counter += 1
        if counter > len(kys):
            counter = 0
        try:
            value = int(keye)
        except ValueError:
            value = "999"
        return value

    with mock.patch('awss.awsc.getdetails', getlocaldetails, create=True):
        with mock.patch('awss.awsc.getaminame', getlocalaminame, create=True):
            with mock.patch('awss.getchar._Getch.int', RetKey, create=True):
                if ide != '0':
                    (tarID, tarIndex) = determineTarget("ssh", ids,
                                                        "TEST")
                    assert tarID == ide
                    assert tarIndex == idx
                else:
                    with pytest.raises(SystemExit):
                        (tarID, tarIndex) = determineTarget("ssh", ids,
                                                            "TEST")
                        pass
