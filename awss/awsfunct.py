
from builtins import range
import boto3
from awss.debug import debugPrint, debugPrintAll


def awsInit():
    global ec2C
    global ec2R
    ec2C = boto3.client('ec2')
    ec2R = boto3.resource('ec2')


def awsGetList(QueryString=None):
    if QueryString is None:
        QueryString = 'ec2C.describe_instances()'
    instanceSummaryData = eval(QueryString)
    iInfo = {}
    for i, v in enumerate(instanceSummaryData['Reservations']):
        inID = v['Instances'][0]['InstanceId']
        iInfo[i] = {'id': inID}
    # numInstances = len(iInfo)
    debugPrint("numInstances: ", len(iInfo))
    debugPrintAll("InstanceIds Only")
    debugPrintAll(iInfo, True)
    return (iInfo)


def awsGetDetails(iInfo=None):
    if iInfo is None:
        iInfo = awsGetList()
    for i in range(len(iInfo)):
        instanceData = ec2R.Instance(iInfo[i]['id'])
        iInfo[i]['state'] = instanceData.state['Name']
        iInfo[i]['ami'] = instanceData.image_id
        instanceTag = instanceData.tags
        for j in range(len(instanceTag)):
            if instanceTag[j]['Key'] == 'Name':
                iInfo[i]['name'] = instanceTag[j]['Value']
                break
    debugPrintAll("Details except AMI-name")
    debugPrintAll(iInfo, True)
    return (iInfo)


def awsGetAmiName(instanceImgID):
    aminame = ec2R.Image(instanceImgID).name
    return (aminame)


def awsGetSsh(tarID):
    tarInstance = ec2R.Instance(tarID)
    instanceIP = tarInstance.public_ip_address
    instanceKey = tarInstance.key_name
    instanceImgID = tarInstance.image_id
    return (instanceIP, instanceKey, instanceImgID)


def awsDoToggle(tarID, cmdtodo):
    tarInstance = ec2R.Instance(tarID)
    thecmd = getattr(tarInstance, cmdtodo)
    response = thecmd()
    return (response)
