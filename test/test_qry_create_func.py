"""Test module for qry_create function in awss."""

from __future__ import print_function
import pytest
from awss.core import qry_create
import awss.debg as debg

debg.init(False, False)


@pytest.fixture(params=["-i 123456", ""])
def genid(request):
    """Provide instance-id params to test function."""
    return request.param


@pytest.fixture(params=["server", ""])
def genname(request):
    """Provide name params to test function."""
    return request.param


@pytest.fixture(params=["running", "stopped", ""])
def genstate(request):
    """Provide instance-state params to test function."""
    return request.param


class holdOptions():
    """Hold options used by qry_create function."""

    def __init__(self, idnum, instname, inst_state):
        """Initialize options to specified values."""
        self.id = idnum
        self.instname = instname
        self.inst_state = inst_state


idlu = {"-i 123456": 0b0001, "": 0b0000}
namelu = {"server": 0b0010, "": 0b0000}
statelu = {"running": 0b1000, "stopped": 0b0100, "": 0b0000}

expected_results = {
    0: {'title': "All",
        'query': ""},
    1: {'title': "id: '-i 123456'",
        'query': "InstanceIds=['-i 123456']"},
    2: {'title': "name: 'server'",
        'query': "Filters=[{'Name': 'tag:Name', 'Values': ['server']}]"},
    3: {'title': "id: '-i 123456', name: 'server'",
        'query': "InstanceIds=['-i 123456'], Filters=[{'Name': 'tag:Name',"
                 " 'Values': ['server']}]"},
    4: {'title': "state: 'stopped'",
        'query': "Filters=[{'Name': 'instance-state-name',"
                 "'Values': ['stopped']}]"},
    5: {'title': "id: '-i 123456', state: 'stopped'",
        'query': "InstanceIds=['-i 123456'], Filters=[{'Name':"
                 " 'instance-state-name','Values': ['stopped']}]"},
    6: {'title': "name: 'server', state: 'stopped'",
        'query': "Filters=[{'Name': 'tag:Name', 'Values': ['server']},"
                 " {'Name': 'instance-state-name','Values': ['stopped']}]"},
    7: {'title': "id: '-i 123456', name: 'server', state: 'stopped'",
        'query': "InstanceIds=['-i 123456'], Filters=[{'Name': 'tag:Name',"
                 " 'Values': ['server']}, {'Name': 'instance-state-name',"
                 "'Values': ['stopped']}]"},
    8: {'title': "state: 'running'",
        'query': "Filters=[{'Name': 'instance-state-name',"
                 "'Values': ['running']}]"},
    9: {'title': "id: '-i 123456', state: 'running'",
        'query': "InstanceIds=['-i 123456'], Filters=[{'Name':"
                 " 'instance-state-name','Values': ['running']}]"},
    10: {'title': "name: 'server', state: 'running'",
         'query': "Filters=[{'Name': 'tag:Name', 'Values': ['server']},"
                  " {'Name': 'instance-state-name','Values': ['running']}]"},
    11: {'title': "id: '-i 123456', name: 'server', state: 'running'",
         'query': "InstanceIds=['-i 123456'], Filters=[{'Name': 'tag:Name',"
                  " 'Values': ['server']}, {'Name': 'instance-state-name',"
                  "'Values': ['running']}]"}}


def test_query_generation(genid, genname, genstate):
    """Test all valid variations of params with qry_create function in awss."""
    print("TEST - Query_Parser  -   id: %s, name: %s, state: %s" %
          (genid, genname, genstate))

    qryoptions = holdOptions(genid, genname, genstate)
    debg.init(True, False)
    (genQuery, genTitle) = qry_create(qryoptions)

    resultIndex = idlu[genid] + namelu[genname] + statelu[genstate]
    expectedTitle = expected_results[resultIndex]['title']
    expectedQuery = expected_results[resultIndex]['query']

    assert genTitle == expectedTitle
    assert genQuery == expectedQuery
