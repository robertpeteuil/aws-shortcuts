"""Test module for parser functions in awss."""

from __future__ import print_function
import mock
import sys

from awss.core import main


@mock.patch('awss.awsc.init')
def test_list_parse_valid(awsc_mock):
    """Test the main function, all valid variations of the list command."""

    teststrg = "awss list -i i-04a10a9a89f05523d"
    testlist = teststrg.split()

    def cmd_list(options_rec):
        assert options_rec.command == 'list'
        assert options_rec.id == 'i-04a10a9a89f05523d'

    with mock.patch('awss.core.cmd_list', cmd_list, create=True):
        with mock.patch.object(sys, 'argv', testlist):
            try:
                main()
            except SystemExit:
                pass
