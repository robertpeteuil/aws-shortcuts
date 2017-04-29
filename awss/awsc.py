"""
This is part of the AWSS Utility located here:
https://github.com/robertpeteuil/aws-shortcuts

This file contains all functions which talk to AWS EC2.
They communicate via the AWS boto3 libraries.
Functions exist to to search for instances, gather certain
information about instances, and start / stop instances.
"""

from builtins import range
import boto3
import awss.debg as debg

EC2C = ""
EC2R = ""


def init():
    """Attach global vars EC2C, and EC2R to the AWS service.

    This must be called once before any other function in this module
    or they won't function.
    """
    global EC2C         # pylint: disable=global-statement
    global EC2R         # pylint: disable=global-statement
    EC2C = boto3.client('ec2')
    EC2R = boto3.resource('ec2')


def getids(qry_string=None):
    """Get All Instance-Ids that match the qry_string provided.

        input: qry_string (optional)
        returns: dict containing Instance-Ids

    the dict will contain one indexed line, in the format:
    "0: {'id': <instance-id>}" for each instance-id that matched
    the query parameters.

    Note: If no qry_string is provided, it will default
    to searching for all EC2 instances in the default-data-center
    as defined in the user's AWS config file.
    """
    if qry_string is None:
        qry_string = 'EC2C.describe_instances()'
    summary_data = eval(qry_string)     # pylint: disable=eval-used
    i_info = {}
    for i, j in enumerate(summary_data['Reservations']):
        i_info[i] = {'id': j['Instances'][0]['InstanceId']}
    debg.dprint("numInstances: ", len(i_info))
    debg.dprintx("InstanceIds Only")
    debg.dprintx(i_info, True)
    return i_info


def getdetails(i_info=None):
    """Get Details for Each Instance-Id in the dict provided.

        input: dict containing Instance-Ids (optional)
        output: dict containing additional key:value pairs
            for each instance, containing: execution_state,
            image_id, and instance 'name' if it has one.

    Note: if no dict was provided, it calls the getids func
    to create one, then proceeds with the dict returned.
    """
    if i_info is None:
        i_info = getids()
    for i in i_info:
        instance_data = EC2R.Instance(i_info[i]['id'])
        i_info[i]['state'] = instance_data.state['Name']
        i_info[i]['ami'] = instance_data.image_id
        i_info[i]['name'] = gettagvalue(i_info[i]['id'])
    debg.dprintx("Details except AMI-name")
    debg.dprintx(i_info, True)
    return i_info


def gettagvalue(inst_id, tag_title="Name"):
    """Get Tag Value fpr Specified Instance-Id, and Tag.

        input: instance-id, and tag_title (optional)

    If a tag_title is not provided, it defaults to retrieving
    the value for the 'Name' tag.
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
    """Get Image_Name for the Image_Id specified.

        input: Instance_Image_Id

    The Instance_Image_Id is easily retrieved from the
    instance object.  But, retrieving the corresponding Name
    of the Image requires connecting to the Image object, which
    is substantially slower.  Because of the time penalty in
    retriving the Image_Name, this function is only called when
    this information is specifically needed.
    """
    aminame = EC2R.Image(inst_img_id).name
    return aminame


def getsshinfo(inst_id):
    """Get Instance Information Needed for SSH.

        input: instance-id
        return: public_ip, login_key, image_id
    """
    tar_inst = EC2R.Instance(inst_id)
    inst_ip = tar_inst.public_ip_address
    inst_key = tar_inst.key_name
    inst_img_id = tar_inst.image_id
    return (inst_ip, inst_key, inst_img_id)


def startstop(inst_id, cmdtodo):
    """Start or Stop the Specified Instance.

        input: instance-id, command (start or stop)
        return: dict containing the reponse text from AWS
    """
    tar_inst = EC2R.Instance(inst_id)
    thecmd = getattr(tar_inst, cmdtodo)
    response = thecmd()
    return response
