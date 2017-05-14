"""Debug print functions that execute if debug mode initialized.

The debug print functions only print if one of the debug-modes
was set by a previous call to this module's init() function.

There are two debug-modes:
    DEBUG allows calls to the dprint function to print
    DEBUGALL allows calls to the dprintx function to print

License:

    AWSS - Control and connect to AWS EC2 instances from command line
    Copyright (C) 2017  Robert Peteuil

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

URL:       https://github.com/robertpeteuil/aws-shortcuts
Author:    Robert Peteuil

"""
from __future__ import print_function
from awss.colors import C_NORM, C_TI

DEBUG = False
DEBUGALL = False


def init(deb1, deb2=False):
    """Initialize DEBUG and DEBUGALL.

    Allows other modules to set DEBUG and DEBUGALL, so their
    call to dprint or dprintx generate output.

    Args:
        deb1 (bool): value of DEBUG to set
        deb2 (bool): optional - value of DEBUGALL to set,
                     defaults to False.

    """
    global DEBUG        # pylint: disable=global-statement
    global DEBUGALL     # pylint: disable=global-statement
    DEBUG = deb1
    DEBUGALL = deb2


def dprint(item1, item2=""):
    """Print Text if DEBUG set.

    Args:
        item1 (str): item to print
        item2 (str): optional 2nd item to print

    """
    if DEBUG:
        print(item1, "%s%s%s" % (C_TI, item2, C_NORM))


def dprintx(passeditem, special=False):
    """Print Text if DEBUGALL set, optionally with PrettyPrint.

    Args:
        passeditem (str): item to print
        special (bool): determines if item prints with PrettyPrint
                        or regular print.

    """
    if DEBUGALL:
        if special:
            from pprint import pprint
            pprint(passeditem)
        else:
            print("%s%s%s" % (C_TI, passeditem, C_NORM))
