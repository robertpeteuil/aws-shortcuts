"""Communicate with AWS EC2 to get data and interact with instances.

Functions for retrieving data for queried instances, retrieving
the name of the image of an instance (AMI Name), and for starting
or stopping instances.
"""

import boto3

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
        qry_results (dict): raw information returned from AWS.

    """
    qry_prefix = "EC2C.describe_instances("
    qry_real = qry_prefix + qry_string + ")"
    qry_results = eval(qry_real)     # pylint: disable=eval-used
    return qry_results


def get_all_aminames(i_info):
    """Get Image_Name for each instance in i_info.

    Args:
        i_info (dict): information on instances and details.
    Returns:
        i_info (dict): i_info is returned with the aminame
                       added for each instance.

    """
    for i in i_info:
        # pylint: disable=maybe-no-member
        i_info[i]['aminame'] = EC2R.Image(i_info[i]['ami']).name
    return i_info


def get_one_aminame(inst_img_id):
    """Get Image_Name for the image_id specified.

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
