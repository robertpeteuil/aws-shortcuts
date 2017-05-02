"""Generate Data for testing awss test scripts.

Contains:
    ii_noami (dict)     = instance dict without AMI name.
    ii_all (dict)       = instance dict with AMI name.
    ami_lookup (dict)   = lookup dict with ami-number: name.
    ami_user_lu (list)  = list of tuples with login-name: ami-name.
    tags_list (list)    = list of dictionaries, containing tags in
                          name: value format.
    tags_dict (dict)    = indexed dict of dictionaries containing
                          tags in name: value format.
"""

ii_noami = {
    0: {'ami': 'ami-16efb076',
        'id': 'i-0df5fd60bfd215ced',
        'pub_dns_name': '',
        'ssh_key': 'james',
        'state': 'stopped',
        'tag': {'Department': 'Operations',
                'Name': 'Ubuntu',
                'Owner': 'joe@example.org',
                'Role': 'Regression',
                'Stage': 'Archive',
                'Team': 'DataAdmins'}},
    1: {'ami': 'ami-3e21725e',
        'id': 'i-052d2bfaeb676bc86',
        'pub_dns_name': '',
        'ssh_key': 'james',
        'state': 'stopped',
        'tag': {'Department': 'Marketing',
                'Name': 'Ubuntu',
                'Owner': 'diane@example.org',
                'Project': 'Reporting',
                'Stage': 'Pre-Release'}},
    2: {'ami': 'ami-e09acc80',
        'id': 'i-0cfd71bb6ec6f0fa5',
        'pub_dns_name': '',
        'ssh_key': 'james',
        'state': 'stopped',
        'tag': {'Department': 'IT',
                'Name': 'Suse',
                'Owner': 'joe@example.org',
                'Role': 'Test',
                'Stage': 'Alpha',
                'Team': 'Dev10a'}},
    3: {'ami': 'ami-165a0876',
        'id': 'i-017df2336bf679c40',
        'pub_dns_name': '',
        'ssh_key': 'james',
        'state': 'stopped',
        'tag': {'Department': 'Operations',
                'Name': 'Amazon',
                'Owner': 'susan@example.org',
                'Role': 'Dev',
                'Team': 'TestUsers'}},
    4: {'ami': 'ami-af4333cf',
        'id': 'i-058f43c9b690e3e5f',
        'pub_dns_name': '',
        'ssh_key': 'james',
        'state': 'stopped',
        'tag': {'Name': 'CentOS',
                'Owner': 'susan@example.org',
                'Project': 'Reporting',
                'Role': 'Dev',
                'Stage': 'Production',
                'Team': 'Dev10a'}},
    5: {'ami': 'ami-0343ae47',
        'id': 'i-06a88b75aa2cb2e6f',
        'pub_dns_name': '',
        'ssh_key': 'james',
        'state': 'stopped',
        'tag': {'Name': 'Debian',
                'Owner': 'joe@example.org',
                'Project': 'POS-Migration',
                'Role': 'Dev',
                'Stage': 'Beta'}},
    6: {'ami': 'ami-2cade64c',
        'id': 'i-054cd4e8d31bd2181',
        'pub_dns_name': '',
        'ssh_key': 'james',
        'state': 'stopped',
        'tag': {'Department': 'IT',
                'Name': 'RHEL',
                'Project': 'SysAdmin',
                'Role': 'Test',
                'Stage': 'Beta'}},
    7: {'ami': 'ami-02765547',
        'id': 'i-0e0919c061f20ef77',
        'pub_dns_name': '',
        'ssh_key': 'james',
        'state': 'stopped',
        'tag': {'Name': 'CentOS',
                'Owner': 'susan@example.org',
                'Role': 'Community',
                'Stage': 'Pre-Alpha'}},
    8: {'ami': 'ami-3d3a6b78',
        'id': 'i-04a10a9a89f05523d',
        'pub_dns_name': '',
        'ssh_key': 'james',
        'state': 'stopped',
        'tag': {'Department': 'IT',
                'Name': 'Fedora',
                'Project': 'SysAdmin',
                'Role': 'Regression',
                'Team': 'Dev10a'}},
    9: {'ami': 'ami-a2346fc2',
        'id': 'i-06dc920a34316ea29',
        'pub_dns_name': '',
        'ssh_key': 'james',
        'state': 'stopped',
        'tag': {'Department': 'IT',
                'Name': 'WordPress',
                'Project': 'Web UI',
                'Stage': 'Alpha',
                'Team': 'Dev10a'}}}

ii_all = {
    0: {'ami': 'ami-16efb076',
        'aminame': 'ubuntu/images/hvm-ssd/ubuntu-xenial-16.04'
        '-amd64-server-20170221',
        'id': 'i-0df5fd60bfd215ced',
        'pub_dns_name': '',
        'ssh_key': 'james',
        'state': 'stopped',
        'tag': {'Department': 'Operations',
                'Name': 'Ubuntu',
                'Owner': 'joe@example.org',
                'Role': 'Regression',
                'Stage': 'Archive',
                'Team': 'DataAdmins'}},
    1: {'ami': 'ami-3e21725e',
        'aminame': 'ubuntu/images/hvm-ssd/ubuntu-trusty-14.04'
        '-amd64-server-20170110',
        'id': 'i-052d2bfaeb676bc86',
        'pub_dns_name': '',
        'ssh_key': 'james',
        'state': 'stopped',
        'tag': {'Department': 'Marketing',
                'Name': 'Ubuntu',
                'Owner': 'diane@example.org',
                'Project': 'Reporting',
                'Stage': 'Pre-Release'}},
    2: {'ami': 'ami-e09acc80',
        'aminame': 'suse-sles-12-sp2-v20161214-hvm-ssd-x86_64',
        'id': 'i-0cfd71bb6ec6f0fa5',
        'pub_dns_name': '',
        'ssh_key': 'james',
        'state': 'stopped',
        'tag': {'Department': 'IT',
                'Name': 'Suse',
                'Owner': 'joe@example.org',
                'Role': 'Test',
                'Stage': 'Alpha',
                'Team': 'Dev10a'}},
    3: {'ami': 'ami-165a0876',
        'aminame': 'amzn-ami-hvm-2016.09.1.20170119-x86_64-gp2',
        'id': 'i-017df2336bf679c40',
        'pub_dns_name': '',
        'ssh_key': 'james',
        'state': 'stopped',
        'tag': {'Department': 'Operations',
                'Name': 'Amazon',
                'Owner': 'susan@example.org',
                'Role': 'Dev',
                'Team': 'TestUsers'}},
    4: {'ami': 'ami-af4333cf',
        'aminame': 'CentOS Linux 7 x86_64 HVM EBS '
        '1602-b7ee8a69-ee97-4a49-9e68-afaee216db2e-ami-d7e1d2bd.3',
        'id': 'i-058f43c9b690e3e5f',
        'pub_dns_name': '',
        'ssh_key': 'james',
        'state': 'stopped',
        'tag': {'Name': 'CentOS',
                'Owner': 'susan@example.org',
                'Project': 'Reporting',
                'Role': 'Dev',
                'Stage': 'Production',
                'Team': 'Dev10a'}},
    5: {'ami': 'ami-0343ae47',
        'aminame': 'debian-jessie-amd64-hvm-2015-04-25-23-22-ebs',
        'id': 'i-06a88b75aa2cb2e6f',
        'pub_dns_name': '',
        'ssh_key': 'james',
        'state': 'stopped',
        'tag': {'Name': 'Debian',
                'Owner': 'joe@example.org',
                'Project': 'POS-Migration',
                'Role': 'Dev',
                'Stage': 'Beta'}},
    6: {'ami': 'ami-2cade64c',
        'aminame': 'RHEL-7.3_HVM_GA-20161026-x86_64-1-Hourly2-GP2',
        'id': 'i-054cd4e8d31bd2181',
        'pub_dns_name': '',
        'ssh_key': 'james',
        'state': 'stopped',
        'tag': {'Department': 'IT',
                'Name': 'RHEL',
                'Project': 'SysAdmin',
                'Role': 'Test',
                'Stage': 'Beta'}},
    7: {'ami': 'ami-02765547',
        'aminame': 'RightImage_CentOS_6.3_x64_v5.8.8.8_EBS',
        'id': 'i-0e0919c061f20ef77',
        'pub_dns_name': '',
        'ssh_key': 'james',
        'state': 'stopped',
        'tag': {'Name': 'CentOS',
                'Owner': 'susan@example.org',
                'Role': 'Community',
                'Stage': 'Pre-Alpha'}},
    8: {'ami': 'ami-3d3a6b78',
        'aminame': 'fedora-8-x86_64-v1.14-std',
        'id': 'i-04a10a9a89f05523d',
        'pub_dns_name': '',
        'ssh_key': 'james',
        'state': 'stopped',
        'tag': {'Department': 'IT',
                'Name': 'Fedora',
                'Project': 'SysAdmin',
                'Role': 'Regression',
                'Team': 'Dev10a'}},
    9: {'ami': 'ami-a2346fc2',
        'aminame': 'bitnami-wordpress-4.7.3-0-linux-ubuntu-14.04.3-x86_64'
        '-ebs-mp-dff9bfa7-e43e-4c06-bafd-756e9d331d18-ami-6cac0a7a.4',
        'id': 'i-06dc920a34316ea29',
        'pub_dns_name': '',
        'ssh_key': 'james',
        'state': 'stopped',
        'tag': {'Department': 'IT',
                'Name': 'WordPress',
                'Project': 'Web UI',
                'Stage': 'Alpha',
                'Team': 'Dev10a'}}}

ami_lookup = {
    'ami-16efb076': 'ubuntu/images/hvm-ssd/ubuntu-xenial-16.04'
    '-amd64-server-20170221',
    'ami-3e21725e': 'ubuntu/images/hvm-ssd/ubuntu-trusty-14.04'
    '-amd64-server-20170110',
    'ami-e09acc80': 'suse-sles-12-sp2-v20161214-hvm-ssd-x86_64',
    'ami-165a0876': 'amzn-ami-hvm-2016.09.1.20170119-x86_64-gp2',
    'ami-af4333cf': 'CentOS Linux 7 x86_64 HVM EBS '
    '1602-b7ee8a69-ee97-4a49-9e68-afaee216db2e-ami-d7e1d2bd.3',
    'ami-0343ae47': 'debian-jessie-amd64-hvm-2015-04-25-23-22-ebs',
    'ami-2cade64c': 'RHEL-7.3_HVM_GA-20161026-x86_64-1-Hourly2-GP2',
    'ami-02765547': 'RightImage_CentOS_6.3_x64_v5.8.8.8_EBS',
    'ami-3d3a6b78': 'fedora-8-x86_64-v1.14-std',
    'ami-a2346fc2': 'bitnami-wordpress-4.7.3-0-linux-ubuntu-14.04.3-x86_64'
    '-ebs-mp-dff9bfa7-e43e-4c06-bafd-756e9d331d18-ami-6cac0a7a.4'}

# default name for ec2: https://alestic.com/2014/01/ec2-ssh-username/
ami_user_lu = [
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
     '-ebs-mp-dff9bfa7-e43e-4c06-bafd-756e9d331d18-ami-6cac0a7a.4')]

tags_list = [
    {'Name': 'Ubuntu', 'Owner': 'joe@example.org', 'Role': 'Regression',
     'Team': 'DataAdmins', 'Department': 'Operations', 'Stage': 'Archive'},
    {'Department': 'Marketing', 'Owner': 'diane@example.org',
     'Project': 'Reporting', 'Name': 'Ubuntu', 'Stage': 'Pre-Release'},
    {'Name': 'Suse', 'Owner': 'joe@example.org', 'Role': 'Test',
     'Team': 'Dev10a', 'Department': 'IT', 'Stage': 'Alpha'},
    {'Department': 'Operations', 'Owner': 'susan@example.org',
     'Role': 'Dev', 'Name': 'Amazon', 'Team': 'TestUsers'},
    {'Name': 'CentOS', 'Project': 'Reporting', 'Role': 'Dev',
     'Team': 'Dev10a', 'Owner': 'susan@example.org', 'Stage': 'Production'},
    {'Owner': 'joe@example.org', 'Project': 'POS-Migration',
     'Role': 'Dev', 'Name': 'Debian', 'Stage': 'Beta'},
    {'Department': 'IT', 'Project': 'SysAdmin', 'Role': 'Test',
     'Name': 'RHEL', 'Stage': 'Beta'},
    {'Owner': 'susan@example.org', 'Role': 'Community',
     'Name': 'CentOS', 'Stage': 'Pre-Alpha'},
    {'Department': 'IT', 'Project': 'SysAdmin', 'Role': 'Regression',
     'Name': 'Fedora', 'Team': 'Dev10a'},
    {'Department': 'IT', 'Project': 'Web UI', 'Team': 'Dev10a',
     'Name': 'WordPress', 'Stage': 'Alpha'}]

tags_dict = {
    0: {'Name': 'Ubuntu', 'Owner': 'joe@example.org', 'Role': 'Regression',
        'Team': 'DataAdmins', 'Department': 'Operations', 'Stage': 'Archive'},
    1: {'Department': 'Marketing', 'Owner': 'diane@example.org',
        'Project': 'Reporting', 'Name': 'Ubuntu', 'Stage': 'Pre-Release'},
    2: {'Name': 'Suse', 'Owner': 'joe@example.org', 'Role': 'Test',
        'Team': 'Dev10a', 'Department': 'IT', 'Stage': 'Alpha'},
    3: {'Department': 'Operations', 'Owner': 'susan@example.org',
        'Role': 'Dev', 'Name': 'Amazon', 'Team': 'TestUsers'},
    4: {'Name': 'CentOS', 'Project': 'Reporting', 'Role': 'Dev',
        'Team': 'Dev10a', 'Owner': 'susan@example.org', 'Stage': 'Production'},
    5: {'Owner': 'joe@example.org', 'Project': 'POS-Migration',
        'Role': 'Dev', 'Name': 'Debian', 'Stage': 'Beta'},
    6: {'Department': 'IT', 'Project': 'SysAdmin', 'Role': 'Test',
        'Name': 'RHEL', 'Stage': 'Beta'},
    7: {'Owner': 'susan@example.org', 'Role': 'Community',
        'Name': 'CentOS', 'Stage': 'Pre-Alpha'},
    8: {'Department': 'IT', 'Project': 'SysAdmin', 'Role': 'Regression',
        'Name': 'Fedora', 'Team': 'Dev10a'},
    9: {'Department': 'IT', 'Project': 'Web UI', 'Team': 'Dev10a',
        'Name': 'WordPress', 'Stage': 'Alpha'}}
