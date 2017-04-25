#!/usr/bin/env python

from __future__ import print_function
import pytest

from awss import setupParser
parser = setupParser()


def awsparse(args):
    options = parser.parse_args(args)
    return options


@pytest.fixture(params=["start ", "stop "])
def cmdname(request):
    return request.param


@pytest.fixture(params=[("server ", "server"), ("", None)])
def inname(request):
    return request.param


@pytest.fixture(params=[("-i 123456 ", "123456"), ("", None)])
def innum(request):
    return request.param


@pytest.fixture(params=[("", None), ("-r ", "running"), ("-s ", "stopped")])
def instate(request):
    return request.param


@pytest.fixture(params=[("", 0), ("-d ", 1), ("-dd ", 2)])
def debugstate(request):
    return request.param


@pytest.fixture(params=[("", None), ("-p ", True)])
def pemstate(request):
    return request.param


@pytest.fixture(params=[("", None), ("-u TestUser ", "TestUser")])
def username(request):
    return request.param


def test_list_parse_valid(inname, innum, instate, debugstate):
    print("test - list_parse_valid for:   name: %s, id: %s, state: %s,"
          " debug: %s" % (inname[0], innum[0], instate[0], debugstate[0]))
    args = "list " + inname[0] + innum[0] + instate[0] + debugstate[0]
    options = awsparse(args.split())
    assert options.command == 'list'
    assert options.debug == debugstate[1]
    assert options.instname == inname[1]
    assert options.id == innum[1]
    assert options.inState == instate[1]


def test_startstop_parse_valid(cmdname, inname, innum, debugstate):
    print("test - start/stop_parse_valid for:   command: %s, name: %s, id: %s,"
          " debug: %s" % (cmdname, inname[0], innum[0], debugstate[0]))
    args = cmdname + inname[0] + innum[0] + debugstate[0]
    options = awsparse(args.split())
    assert options.command == cmdname[:-1]
    assert options.debug == debugstate[1]
    assert options.instname == inname[1]
    assert options.id == innum[1]


def test_ssh_parse_valid(inname, innum, debugstate):
    print("test - ssh_parse_valid for:   name: %s, id: %s, debug: %s" %
          (inname[0], innum[0], debugstate[0]))
    args = "ssh " + inname[0] + innum[0] + debugstate[0]
    options = awsparse(args.split())
    assert options.command == "ssh"
    assert options.debug == debugstate[1]
    assert options.instname == inname[1]
    assert options.id == innum[1]
