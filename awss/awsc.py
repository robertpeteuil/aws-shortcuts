"""Communicates with AWS services.

Functions exist to to search for instances, gather certain
information about instances, and start / stop instances.
"""

import awss.debg as debg
import boto3
from builtins import range

EC2C = ""
EC2R = ""


def init():
    """Attach global vars EC2C, and EC2R to the AWS service.

    Must be called before any other functions in this module
    will work in production mode.

    To allow testing on CI servers without AWS credentials,
    this assignment is done in this function instead of the
    module itself - as the boto3 methods below require AWS
    credentials on the host.

    """
    global EC2C         # pylint: disable=global-statement
    global EC2R         # pylint: disable=global-statement
    EC2C = boto3.client('ec2')
    EC2R = boto3.resource('ec2')


def get_inst_info(qry_string):
    """Get details for instances that match the qry_string.

    Execute a query against the AWS EC2 client object, that is
    based on the contents of qry_string.

    Args:
        qry_string (str): the query to be used against the aws ec2 client.
    Returns:
        i_info (dict): information on instances and details.

    """
    qry_prefix = "EC2C.describe_instances("
    qry_real = qry_prefix + qry_string + ")"
    summary_data = eval(qry_real)     # pylint: disable=eval-used
    i_info = {}
    for i, j in enumerate(summary_data['Reservations']):
        i_info[i] = {'id': j['Instances'][0]['InstanceId']}
        i_info[i]['state'] = j['Instances'][0]['State']['Name']
        i_info[i]['ami'] = j['Instances'][0]['ImageId']
        i_info[i]['ssh_key'] = j['Instances'][0]['KeyName']
        i_info[i]['pub_dns_name'] = j['Instances'][0]['PublicDnsName']
        inst_tags = j['Instances'][0]['Tags']
        for k in range(len(inst_tags)):
            tagname = inst_tags[k]['Key']
            i_info[i]["tag:" + tagname] = inst_tags[k]['Value']
    debg.dprint("numInstances: ", len(i_info))
    debg.dprintx("Details except AMI-name")
    debg.dprintx(i_info, True)
    return i_info


def gettagvalue(inst_id, tag_title="Name"):
    """Get value for tag in specified instance..

    Args:
        inst_id (str): instance-id to get tag value from.
        tag_title (str): (optional) name of tag to get
                         value from. defaults to 'Name'.
    Returns:
        tagvalue (str): value of the tag and instance specified

    """
    instance_tags = EC2R.Instance(inst_id).tags
    qty_tags = len(instance_tags)
    if qty_tags:
        for j in range(qty_tags):
            if instance_tags[j]['Key'] == tag_title:
                tagvalue = instance_tags[j]['Value']
                break
    else:
        tagvalue = ""
    return tagvalue


def getaminame(inst_img_id):
    """Get Image_Name for the image_id specified.

    Connects to ec2 resource.Image object, which is slower
    than retrieving info from the ec2 resource.Instance object.

    Args:
        inst_img_id (str): image_id to get name value from.
    Returns:
        aminame (str): name of the image.

    """
    aminame = EC2R.Image(inst_img_id).name
    return aminame


def startstop(inst_id, cmdtodo):
    """Start or Stop the Specified Instance.

    Args:
        inst_id (str): instance-id to perform command against
        cmdtodo (str): command to perform (start or stop)
    Returns:
        response (dict): reponse returned from AWS after
                         performing specified action.

    """
    tar_inst = EC2R.Instance(inst_id)
    thecmd = getattr(tar_inst, cmdtodo)
    response = thecmd()
    return response
