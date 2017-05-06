"""Test module for parser functions in awss."""

from __future__ import print_function
import pytest
import mock
import sys

from awss.core import main


@pytest.fixture(scope="module", params=[("", False), ("-p ", True)])
def inpem(request):
    """Provide 'nopem' flag attribute and expected result to test function."""
    return request.param


@pytest.fixture(scope="module", params=[("", None),
                ("-u AdminUser ", "AdminUser")])
def inuser(request):
    """Provide username and expected results to test function."""
    return request.param


@pytest.fixture(scope="module", params=[("", 0), ("-d ", 1), ("-dd ", 2)])
def debugstate(request):
    """Provide debug-state and expected results to test function."""
    return request.param


@pytest.fixture(params=[("", None), ("-r ", "running"), ("-s ", "stopped")])
def instate(request):
    """Provide instance-state and expected result to test function."""
    return request.param


@mock.patch('awss.awsc.init')
def test_main_list(awsc_mock, instate, debugstate):
    """Test the main function for the list command."""

    teststrg = "awss list -i i-04a10a9a89f05523d " + instate[0] + debugstate[0]
    testlist = teststrg.split()

    def cmd_list(options_rec):
        assert options_rec.command == 'list'
        assert options_rec.id == 'i-04a10a9a89f05523d'
        assert options_rec.debug == debugstate[1]
        assert options_rec.inst_state == instate[1]

    with mock.patch('awss.core.cmd_list', cmd_list, create=True):
        with mock.patch.object(sys, 'argv', testlist):
            try:
                main()
            except SystemExit:
                pass


@mock.patch('awss.awsc.init')
def test_main_ssh(awsc_mock, debugstate, inuser, inpem):
    """Test the main function for the ssh command."""

    teststrg = "awss ssh -i i-04a10a9a89f05523d "
    teststrg += debugstate[0] + inuser[0] + inpem[0]
    testlist = teststrg.split()

    def cmd_ssh(options_rec):
        assert options_rec.command == 'ssh'
        assert options_rec.id == 'i-04a10a9a89f05523d'
        assert options_rec.debug == debugstate[1]
        assert options_rec.user == inuser[1]
        assert options_rec.nopem == inpem[1]

    with mock.patch('awss.core.cmd_ssh', cmd_ssh, create=True):
        with mock.patch.object(sys, 'argv', testlist):
            try:
                main()
            except SystemExit:
                pass
