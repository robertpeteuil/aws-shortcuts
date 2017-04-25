#!/usr/bin/env python

from __future__ import print_function
import pytest
from awss import queryCreate, queryHelper
import awss.debg as debg

debg.init()


@pytest.fixture(params=["-i 123456", ""])
def genid(request):
    return request.param


@pytest.fixture(params=["server", ""])
def genname(request):
    return request.param


@pytest.fixture(params=["running", "stopped", ""])
def genstate(request):
    return request.param


class holdOptions():
    def __init__(self, idnum, instname, inState):
        self.id = idnum
        self.instname = instname
        self.inState = inState


idlu = {"-i 123456": 0b0001, "": 0b0000}
namelu = {"server": 0b0010, "": 0b0000}
statelu = {"running": 0b1000, "stopped": 0b0100, "": 0b0000}

expected_results = {
    0: {'title': "All",
        'query': "ec2C.describe_instances()"},
    1: {'title': "id: '-i 123456'",
        'query': "ec2C.describe_instances(InstanceIds=['-i 123456'])"},
    2: {'title': "name: 'server'",
        'query': "ec2C.describe_instances(Filters=[{'Name': 'tag:Name',"
                 " 'Values': ['server']}])"},
    3: {'title': "id: '-i 123456', name: 'server'",
        'query': "ec2C.describe_instances(InstanceIds=['-i 123456'],"
                 " Filters=[{'Name': 'tag:Name', 'Values': ['server']}])"},
    4: {'title': "state: 'stopped'",
        'query': "ec2C.describe_instances(Filters=[{'Name':"
                 " 'instance-state-name','Values': ['stopped']}])"},
    5: {'title': "id: '-i 123456', state: 'stopped'",
        'query': "ec2C.describe_instances(InstanceIds=['-i 123456'], Filters"
                 "=[{'Name': 'instance-state-name','Values': ['stopped']}])"},
    6: {'title': "name: 'server', state: 'stopped'",
        'query': "ec2C.describe_instances(Filters=[{'Name': 'tag:Name',"
                 " 'Values': ['server']}, {'Name': 'instance-state-name',"
                 "'Values': ['stopped']}])"},
    7: {'title': "id: '-i 123456', name: 'server', state: 'stopped'",
        'query': "ec2C.describe_instances(InstanceIds=['-i 123456'], Filters"
                 "=[{'Name': 'tag:Name', 'Values': ['server']}, {'Name':"
                 " 'instance-state-name','Values': ['stopped']}])"},
    8: {'title': "state: 'running'",
        'query': "ec2C.describe_instances(Filters=[{'Name':"
                 " 'instance-state-name','Values': ['running']}])"},
    9: {'title': "id: '-i 123456', state: 'running'",
        'query': "ec2C.describe_instances(InstanceIds=['-i 123456'], Filters"
                 "=[{'Name': 'instance-state-name','Values': ['running']}])"},
    10: {'title': "name: 'server', state: 'running'",
         'query': "ec2C.describe_instances(Filters=[{'Name': 'tag:Name',"
                  " 'Values': ['server']}, {'Name': 'instance-state-name',"
                  "'Values': ['running']}])"},
    11: {'title': "id: '-i 123456', name: 'server', state: 'running'",
         'query': "ec2C.describe_instances(InstanceIds=['-i 123456'], Filters"
                  "=[{'Name': 'tag:Name', 'Values': ['server']}, {'Name':"
                  " 'instance-state-name','Values': ['running']}])"}}


def test_query_generation(genid, genname, genstate):
    print("TEST - Query_Parser  -   id: %s, name: %s, state: %s" %
          (genid, genname, genstate))
    qryoptions = holdOptions(genid, genname, genstate)
    (genQuery, genTitle) = queryCreate(qryoptions)

    resultIndex = idlu[genid] + namelu[genname] + statelu[genstate]
    expectedTitle = expected_results[resultIndex]['title']
    expectedQuery = expected_results[resultIndex]['query']

    assert genTitle == expectedTitle
    assert genQuery == expectedQuery
