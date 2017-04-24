
from builtins import range
import boto3
import awss.debg as debg


def init():
    global ec2C
    global ec2R
    ec2C = boto3.client('ec2')
    ec2R = boto3.resource('ec2')


def getids(QueryString=None):
    if QueryString is None:
        QueryString = 'ec2C.describe_instances()'
    instanceSummaryData = eval(QueryString)
    iInfo = {}
    for i, v in enumerate(instanceSummaryData['Reservations']):
        instID = v['Instances'][0]['InstanceId']
        iInfo[i] = {'id': instID}
    debg.dprint("numInstances: ", len(iInfo))
    debg.dprintx("InstanceIds Only")
    debg.dprintx(iInfo, True)
    return (iInfo)


def getdetails(iInfo=None):
    if iInfo is None:
        iInfo = getids()
    for i in range(len(iInfo)):
        instanceData = ec2R.Instance(iInfo[i]['id'])
        iInfo[i]['state'] = instanceData.state['Name']
        iInfo[i]['ami'] = instanceData.image_id
        iInfo[i]['name'] = gettagvalue(iInfo[i]['id'])
        # instanceTag = instanceData.tags
        # for j in range(len(instanceTag)):
        #     if instanceTag[j]['Key'] == 'Name':
        #         iInfo[i]['name'] = instanceTag[j]['Value']
        #         break
    debg.dprintx("Details except AMI-name")
    debg.dprintx(iInfo, True)
    return (iInfo)


def gettagvalue(instID, Tag="Name"):
    instanceData = ec2R.Instance(instID)
    instanceTag = instanceData.tags
    if len(instanceTag) > 0:
        for j in range(len(instanceTag)):
            if instanceTag[j]['Key'] == Tag:
                tagvalue = instanceTag[j]['Value']
                break
    else:
        tagvalue = ""
    return tagvalue


def getaminame(instanceImgID):
    aminame = ec2R.Image(instanceImgID).name
    return (aminame)


def getsshinfo(instID):
    tarInstance = ec2R.Instance(instID)
    instanceIP = tarInstance.public_ip_address
    instanceKey = tarInstance.key_name
    instanceImgID = tarInstance.image_id
    return (instanceIP, instanceKey, instanceImgID)


def startstop(instID, cmdtodo):
    tarInstance = ec2R.Instance(instID)
    thecmd = getattr(tarInstance, cmdtodo)
    response = thecmd()
    return (response)
