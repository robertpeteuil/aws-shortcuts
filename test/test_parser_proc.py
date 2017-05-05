"""Test module for parser functions in awss."""

from __future__ import print_function
import pytest

from awss.core import parser_setup


@pytest.fixture(params=["start ", "stop "])
def cmdname(request):
    """Provide command params to test function."""
    return request.param


@pytest.fixture(params=[("server ", "server"), ("", None)])
def inname(request):
    """Provide name and expected result params to test function."""
    return request.param


@pytest.fixture(params=[("-i 123456 ", "123456"), ("", None)])
def innum(request):
    """Provide instance-id and expected result params to test function."""
    return request.param


@pytest.fixture(params=[("", None), ("-r ", "running"), ("-s ", "stopped")])
def instate(request):
    """Provide instance-state and expected result params to test function."""
    return request.param


@pytest.fixture(params=[("", 0), ("-d ", 1), ("-dd ", 2)])
def debugstate(request):
    """Provide debug-state and expected result params to test function."""
    return request.param


@pytest.fixture(params=[("", None), ("-p ", True)])
def pemstate(request):
    """Provide pem-mode and expected result params to test function."""
    return request.param


@pytest.fixture(params=[("", None), ("-u TestUser ", "TestUser")])
def username(request):
    """Provide user-name and expected result params to test function."""
    return request.param


@pytest.fixture(params=[("", "-h"), ("list ", "-h"), ("start ", "-h"),
                        ("stop ", "-h"), ("ssh ", "-h")])
def inhelp(request):
    """Provide help params for each parser and subparser to test function."""
    return request.param


def test_list_parse_valid(inname, innum, instate, debugstate):
    """Test all valid variations of the list command."""
    print("test - list_parse_valid for:   name: %s, id: %s, state: %s,"
          " debug: %s" % (inname[0], innum[0], instate[0], debugstate[0]))

    args = "list " + inname[0] + innum[0] + instate[0] + debugstate[0]
    parser = parser_setup()
    options = parser.parse_args(args.split())

    assert options.command == 'list'
    assert options.debug == debugstate[1]
    assert options.instname == inname[1]
    assert options.id == innum[1]
    assert options.inst_state == instate[1]


def test_startstop_parse_valid(cmdname, inname, innum, debugstate):
    """Test all valid variations of the start and stop command."""
    print("test - start/stop_parse_valid for:   command: %s, name: %s, id: %s,"
          " debug: %s" % (cmdname, inname[0], innum[0], debugstate[0]))

    args = cmdname + inname[0] + innum[0] + debugstate[0]
    parser = parser_setup()
    options = parser.parse_args(args.split())

    assert options.command == cmdname[:-1]
    assert options.debug == debugstate[1]
    assert options.instname == inname[1]
    assert options.id == innum[1]


def test_ssh_parse_valid(inname, innum, debugstate):
    """Test all valid variations of the ssh command."""
    print("test - ssh_parse_valid for:   name: %s, id: %s, debug: %s" %
          (inname[0], innum[0], debugstate[0]))

    args = "ssh " + inname[0] + innum[0] + debugstate[0]
    parser = parser_setup()
    options = parser.parse_args(args.split())

    assert options.command == "ssh"
    assert options.debug == debugstate[1]
    assert options.instname == inname[1]
    assert options.id == innum[1]


def test_list_parse_help(inhelp):
    """Test help for each parser and subparser."""
    print("test - list_parse_help for:   command: %s" % (inhelp[0]))

    args = inhelp[0] + inhelp[1]
    parser = parser_setup()
    with pytest.raises(SystemExit):
        options = parser.parse_args(args.split())  # noqa: F841
        pass
