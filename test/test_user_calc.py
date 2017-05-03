"""Test function for ssh user calculation function in awss."""

import pytest
import awss.debg as debg
from awss.core import cmd_ssh_user


@pytest.mark.parametrize(("username", "aminame"), [
    ('ubuntu', 'ubuntu/images/hvm-ssd/ubuntu-xenial-16.04'
     '-amd64-server-20170221'),
    ('ubuntu', 'ubuntu/images/hvm-ssd/ubuntu-trusty-14.04'
     '-amd64-server-20170110'),
    ('ec2-user', 'suse-sles-12-sp2-v20161214-hvm-ssd-x86_64'),
    ('ec2-user', 'amzn-ami-hvm-2016.09.1.20170119-x86_64-gp2'),
    ('centos', 'CentOS Linux 7 x86_64 HVM EBS '
     '1602-b7ee8a69-ee97-4a49-9e68-afaee216db2e-ami-d7e1d2bd.3'),
    ('admin', 'debian-jessie-amd64-hvm-2015-04-25-23-22-ebs'),
    ('ec2-user', 'RHEL-7.3_HVM_GA-20161026-x86_64-1-Hourly2-GP2'),
    ('centos', 'RightImage_CentOS_6.3_x64_v5.8.8.8_EBS'),
    ('root', 'fedora-8-x86_64-v1.14-std'),
    ('ubuntu', 'bitnami-wordpress-4.7.3-0-linux-ubuntu-14.04.3-x86_64'
     '-ebs-mp-dff9bfa7-e43e-4c06-bafd-756e9d331d18-ami-6cac0a7a.4'),
    ('ec2-user', 'Made up Name'),
    ('ec2-user', '\tbad formatting\n\n\n')])
def test_calc_sshuser(username, aminame):
    """Test calculation of ssh login user based on image name."""

    debg.init(False, False)

    name_returned = cmd_ssh_user(aminame)

    assert name_returned == username
