"""Test module for list_instances function in awss."""

from __future__ import print_function

from awss.core import list_instances
import awss.debg as debg

# import dictionary of 10 instances filled with sample data
from awstidydata import ii_all


def test_display_list(capsys):
    """Test list_instances function in awss."""
    debg.init(False, False)
    outputTitle = "Test Report"
    list_instances(outputTitle, ii_all)
    out, err = capsys.readouterr()
    assert err == ""
