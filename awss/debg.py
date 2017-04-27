"""
This is part of the AWSS Utility located here:
https://github.com/robertpeteuil/aws-shortcuts

This file contains debug print functions that only print
if this module's init() function is called in the form:
    init(DEBUG, DEBUGALL)

DEBUG allows calls to the dprint function to print
DEBUGALL allows calls to the dprintx function to print
"""

from __future__ import print_function
from awss.colors import C_NORM, C_TI

DEBUG = False
DEBUGALL = False


def init(deb1=False, deb2=False):
    """
    initialize the values of DEBUG and DEBUGALL
        if this init is not called, they default to False, and
        all calls to the debug print functions, dprint and dprintx
        will not generate output.
    """

    global DEBUG
    global DEBUGALL
    DEBUG = deb1
    DEBUGALL = deb2


def dprint(item1, item2=""):
    """
    Debug Print - only print is debug mode is set
        input: item_to_print, 2nd_item (optional)

    This prints the first paramter sent without change, so color
    strings can be inserted before calling.
    If the optional 2nd paramter is passed, it will print in CYAN.
    This allows for easy printing of variable names (in WHITE) and
    their values (in CYAN) like this: dprint(item, value)
    """
    if DEBUG:
        print(item1, "%s%s%s" % (C_TI, item2, C_NORM))


def dprintx(passeditem, special=False):
    """
    Extra Debug Print with optional PrettyPrint
        input: item_to_print, pretty_print_mode (optional)

    If DEBUGALL is set, the item passed is printed with the
    normal pritn command, or PrettyPrint if a 2nd 'True' param
    is passed.  This provides a method of printing out entire
    dictionaries on occasion, without making them part of the
    normal debug display.
    Calling without passing a 2nd param is ideal for printing
    titles that you want to display before a pprint output of
    a dict.
    """

    if DEBUGALL:
        if special:
            from pprint import pprint
            pprint(passeditem)
        else:
            print("%s%s%s" % (C_TI, passeditem, C_NORM))
