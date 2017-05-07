"""AWS Return Data for testing awss test scripts.

Contains:
    rawdata (dict)      = response from AWS for an instance.
    rawdata_nt (dict)   = response from AWS for an instance without tags.
    rawdata_term (dict) = response from AWS for a terminated instance.
    rawnodata (dict)    = response from AWS for no instances.
    start_resp (dict)   = response from AWS after instance started.
    stop_resp (dict)    = response from AWS after instance stopped.
"""
rawdata = {u'Reservations': [
    {u'Instances': [
        {u'SourceDestCheck': True,
         u'Monitoring': {u'State': 'disabled'},
         u'VirtualizationType': 'paravirtual', u'Hypervisor': 'xen',
         u'StateReason':
            {u'Message': 'Client.UserInitiatedShutdown:'
             ' User initiated shutdown',
             u'Code': 'Client.UserInitiatedShutdown'},
             u'PublicDnsName': 'ec2-54-219-64-145.us-west-1.'
             'compute.amazonaws.com',
             u'KeyName': 'james',
             u'State': {u'Code': 16, u'Name': 'running'},
             u'BlockDeviceMappings':
             [
            {u'DeviceName': '/dev/sda1', u'Ebs':
                {u'Status': 'attached', u'DeleteOnTermination': True,
                 u'VolumeId': 'vol-0ed3c42472dde29fc',
                 u'AttachTime': '2016-05-01-16-27-19'}}],
            u'LaunchTime': '2016-05-01-19-19-45', u'Architecture': 'x86_64',
            u'RamdiskId': 'ari-00a1c7fc', u'KernelId': 'aki-ad3667e8',
            u'Placement': {
                u'Tenancy': 'default', u'GroupName': '',
                u'AvailabilityZone': 'us-west-1a'},
            u'IamInstanceProfile': {
                u'Id': 'QRWMKZECMHCOHGGDIYZOB',
                u'Arn': 'arn:aws:iam::262637777988:instance-profile/Primary'},
            u'RootDeviceName': '/dev/sda1',
            u'PrivateIpAddress': '172.31.64.201',
            u'ProductCodes': [], u'VpcId': 'vpc-cca3dd3c',
            u'StateTransitionReason': 'User initiated'
            ' (2016-02-11 19:28:09 GMT)',
            u'InstanceId': 'i-04a10a9a89f05523d',
            u'Tags': [
                {u'Value': 'Fedora', u'Key': 'Name'},
                {u'Value': 'Regression', u'Key': 'Role'},
                {u'Value': 'IT', u'Key': 'Department'},
                {u'Value': 'Dev10a', u'Key': 'Team'},
                {u'Value': 'SysAdmin', u'Key': 'Project'}],
            u'ImageId': 'ami-3d3a6b78',
            u'PrivateDnsName': 'ip-172-31-64-201.us-west-1.compute.internal',
            u'EbsOptimized': False,
            u'SecurityGroups': [{
                u'GroupName': 'launch-wizard-29',
                u'GroupId': 'sg-0e6ea9b9'}],
            u'ClientToken': 'DPSAr5354928108794',
            u'SubnetId': 'subnet-8569addc',
            u'RootDeviceType': 'ebs',
            u'AmiLaunchIndex': 0,
            u'InstanceType': 't1.micro',
            u'NetworkInterfaces': [{
                u'SourceDestCheck': True,
                u'NetworkInterfaceId': 'eni-dae414c7',
                u'PrivateIpAddresses': [{
                    u'PrivateDnsName': 'ip-172-31-64-201.us-west-1.'
                    'compute.internal',
                    u'Primary': True,
                    u'PrivateIpAddress': '172.31.64.201'}],
                u'SubnetId': 'subnet-8569addc',
                u'Attachment': {
                    u'Status': 'attached',
                    u'DeviceIndex': 0,
                    u'DeleteOnTermination': True,
                    u'AttachmentId': 'eni-attach-fcca7e92',
                    u'AttachTime': '2016-05-01-16-27-18'},
                u'OwnerId': '262637777988',
                u'PrivateIpAddress': '172.31.64.201',
                u'Status': 'in-use',
                u'MacAddress': '06:06:b4:06:c4:2f',
                u'VpcId': 'vpc-cca3dd3c',
                u'Description': '',
                u'PrivateDnsName': 'ip-172-31-64-201.us-west-1.'
                'compute.internal',
                u'Groups': [{
                    u'GroupName': 'launch-wizard-29',
                    u'GroupId': 'sg-0e6ea9b9'}],
                u'Ipv6Addresses': []}]}],
     u'ReservationId': 'r-0fbb688d2f399e2fa',
     u'Groups': [],
     u'OwnerId': '262637777988'}],
    'ResponseMetadata': {
        'RetryAttempts': 0,
        'HTTPStatusCode': 200,
        'HTTPHeaders': {
            'date': 'Mon, 01 May 2016 01:12:21 GMT',
            'transfer-encoding': 'chunked',
            'content-type': 'text/xml;charset=UTF-8',
            'vary': 'Accept-Encoding',
            'server': 'AmazonEC2'},
        'RequestId': '171a0078-bcbd-1924-91d8-b5a26cbcb23c'}}

rawdata_nt = {u'Reservations': [
    {u'Instances': [
        {u'SourceDestCheck': True,
         u'Monitoring': {u'State': 'disabled'},
         u'VirtualizationType': 'paravirtual', u'Hypervisor': 'xen',
         u'StateReason':
            {u'Message': 'Client.UserInitiatedShutdown:'
             ' User initiated shutdown',
             u'Code': 'Client.UserInitiatedShutdown'},
             u'PublicDnsName': 'ec2-54-219-64-145.us-west-1.'
             'compute.amazonaws.com',
             u'KeyName': 'james',
             u'State': {u'Code': 16, u'Name': 'running'},
             u'BlockDeviceMappings':
             [
            {u'DeviceName': '/dev/sda1', u'Ebs':
                {u'Status': 'attached', u'DeleteOnTermination': True,
                 u'VolumeId': 'vol-0ed3c42472dde29fc',
                 u'AttachTime': '2016-05-01-16-27-19'}}],
            u'LaunchTime': '2016-05-01-19-19-45', u'Architecture': 'x86_64',
            u'RamdiskId': 'ari-00a1c7fc', u'KernelId': 'aki-ad3667e8',
            u'Placement': {
                u'Tenancy': 'default', u'GroupName': '',
                u'AvailabilityZone': 'us-west-1a'},
            u'IamInstanceProfile': {
                u'Id': 'QRWMKZECMHCOHGGDIYZOB',
                u'Arn': 'arn:aws:iam::262637777988:instance-profile/Primary'},
            u'RootDeviceName': '/dev/sda1',
            u'PrivateIpAddress': '172.31.64.201',
            u'ProductCodes': [], u'VpcId': 'vpc-cca3dd3c',
            u'StateTransitionReason': 'User initiated'
            ' (2016-02-11 19:28:09 GMT)',
            u'InstanceId': 'i-04a10a9a89f05523d',
            u'ImageId': 'ami-3d3a6b78',
            u'PrivateDnsName': 'ip-172-31-64-201.us-west-1.compute.internal',
            u'EbsOptimized': False,
            u'SecurityGroups': [{
                u'GroupName': 'launch-wizard-29',
                u'GroupId': 'sg-0e6ea9b9'}],
            u'ClientToken': 'DPSAr5354928108794',
            u'SubnetId': 'subnet-8569addc',
            u'RootDeviceType': 'ebs',
            u'AmiLaunchIndex': 0,
            u'InstanceType': 't1.micro',
            u'NetworkInterfaces': [{
                u'SourceDestCheck': True,
                u'NetworkInterfaceId': 'eni-dae414c7',
                u'PrivateIpAddresses': [{
                    u'PrivateDnsName': 'ip-172-31-64-201.us-west-1.'
                    'compute.internal',
                    u'Primary': True,
                    u'PrivateIpAddress': '172.31.64.201'}],
                u'SubnetId': 'subnet-8569addc',
                u'Attachment': {
                    u'Status': 'attached',
                    u'DeviceIndex': 0,
                    u'DeleteOnTermination': True,
                    u'AttachmentId': 'eni-attach-fcca7e92',
                    u'AttachTime': '2016-05-01-16-27-18'},
                u'OwnerId': '262637777988',
                u'PrivateIpAddress': '172.31.64.201',
                u'Status': 'in-use',
                u'MacAddress': '06:06:b4:06:c4:2f',
                u'VpcId': 'vpc-cca3dd3c',
                u'Description': '',
                u'PrivateDnsName': 'ip-172-31-64-201.us-west-1.'
                'compute.internal',
                u'Groups': [{
                    u'GroupName': 'launch-wizard-29',
                    u'GroupId': 'sg-0e6ea9b9'}],
                u'Ipv6Addresses': []}]}],
     u'ReservationId': 'r-0fbb688d2f399e2fa',
     u'Groups': [],
     u'OwnerId': '262637777988'}],
    'ResponseMetadata': {
        'RetryAttempts': 0,
        'HTTPStatusCode': 200,
        'HTTPHeaders': {
            'date': 'Mon, 01 May 2016 01:12:21 GMT',
            'transfer-encoding': 'chunked',
            'content-type': 'text/xml;charset=UTF-8',
            'vary': 'Accept-Encoding',
            'server': 'AmazonEC2'},
        'RequestId': '171a0078-bcbd-1924-91d8-b5a26cbcb23c'}}

rawdata_term = {
    u'Reservations': [
        {u'Groups': [],
         u'Instances': [{
             u'AmiLaunchIndex': 0,
             u'Architecture': 'x86_64',
             u'BlockDeviceMappings': [],
             u'ClientToken': 'DPSAr5354928108794',
             u'EbsOptimized': False,
             u'Hypervisor': 'xen',
             u'ImageId': 'ami-05cf2265',
             u'InstanceId': 'i-04a10a9a89f05523d',
             u'InstanceType': 't2.micro',
             u'KeyName': 'james',
             u'LaunchTime': '2016-05-01-19-19-45',
             u'Monitoring': {u'State': 'disabled'},
             u'NetworkInterfaces': [],
             u'Placement': {
                 u'AvailabilityZone': 'us-west-2a',
                 u'GroupName': '',
                 u'Tenancy': 'default'},
             u'PrivateDnsName': '',
             u'ProductCodes': [],
             u'PublicDnsName': '',
             u'RootDeviceName': '/dev/sda1',
             u'RootDeviceType': 'ebs',
             u'SecurityGroups': [],
             u'State': {
                 u'Code': 48,
                 u'Name': 'terminated'},
             u'StateReason': {
                 u'Code': 'Client.UserInitiatedShutdown',
                 u'Message': 'Client.UserInitiatedShutdown:'
                 '     initiated shutdown'},
             u'StateTransitionReason': 'User initiated (2016-05-01'
             '    1:05 GMT)',
             u'VirtualizationType': 'hvm'}],
         u'OwnerId': '262637777988',
         u'ReservationId': 'r-0fbb688d2f399e2fa'}],
    'ResponseMetadata': {
        'HTTPHeaders': {
            'content-type': 'text/xml;charset=UTF-8',
            'date': 'Mon, 01 May 2016 01:12:21 GMT',
            'server': 'AmazonEC2',
            'transfer-encoding': 'chunked',
            'vary': 'Accept-Encoding'},
        'HTTPStatusCode': 200,
        'RequestId': '171a0078-ac7c-4b15-91c0-b5a26cbcb23c',
        'RetryAttempts': 0}}

rawnodata = {
    u'Reservations': [],
    'ResponseMetadata': {
        'RetryAttempts': 0,
        'HTTPStatusCode': 200,
        'RequestId': '171a0078-1924-91d8-bcbd-b5a26cbcb23c',
        'HTTPHeaders': {
            'transfer-encoding': 'chunked',
            'vary': 'Accept-Encoding',
            'server': 'AmazonEC2',
            'content-type': 'text/xml;charset=UTF-8',
            'date': 'Mon, 01 May 2016 01:32:10 GMT'}}}

start_resp = {
    u'StartingInstances':
    [{u'InstanceId': 'i-04a10a9a89f05523d', u'CurrentState':
     {u'Code': 0, u'Name': 'pending'},
      u'PreviousState': {u'Code': 80, u'Name': 'stopped'}}],
    'ResponseMetadata':
    {'RetryAttempts': 0, 'HTTPStatusCode': 200,
     'RequestId': '20fe24aa-0e0e-4389-bc38-49d9a8c4dd55',
     'HTTPHeaders':
         {'transfer-encoding': 'chunked', 'vary': 'Accept-Encoding',
          'server': 'AmazonEC2', 'content-type': 'text/xml;charset=UTF-8',
          'date': 'Mon, 01 May 2016 01:12:21 GMT'}}}

stop_resp = {
    u'StoppingInstances':
    [{u'InstanceId': 'i-04a10a9a89f05523d', u'CurrentState':
     {u'Code': 64, u'Name': 'stopping'},
      u'PreviousState': {u'Code': 16, u'Name': 'running'}}],
    'ResponseMetadata':
    {'RetryAttempts': 0, 'HTTPStatusCode': 200,
     'RequestId': '1aa0dcfd-b6c5-4121-bdeb-8c9abf0de921',
     'HTTPHeaders':
        {'transfer-encoding': 'chunked', 'vary': 'Accept-Encoding',
         'server': 'AmazonEC2', 'content-type': 'text/xml;charset=UTF-8',
         'date': 'Mon, 01 May 2016 01:12:21 GMT'}}}
