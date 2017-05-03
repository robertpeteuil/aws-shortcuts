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
