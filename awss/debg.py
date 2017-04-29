"""Debug print functions that execute if debug mode initialized.

The debug print functions only print if one of the debug-modes
was set by a previous call to this module's init() function.

There are two debug-modes:
    DEBUG allows calls to the dprint function to print
    DEBUGALL allows calls to the dprintx function to print
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

    Returns:
        None

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

    Returns:
        None

    """
    if DEBUG:
        print(item1, "%s%s%s" % (C_TI, item2, C_NORM))


def dprintx(passeditem, special=False):
    """Print Text if DEBUGALL set, optionally with PrettyPrint.

    Args:
        passeditem (str): item to print
        special (bool): determines if item prints with PrettyPrint
                        or regular print.

    Returns:
        None

    """
    if DEBUGALL:
        if special:
            from pprint import pprint
            pprint(passeditem)
        else:
            print("%s%s%s" % (C_TI, passeditem, C_NORM))
