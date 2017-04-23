
from __future__ import print_function
from awss.colors import CLRnormal, CLRtitle


def init(deb1=False, deb2=False):
    global debug
    global debugall
    debug = deb1
    debugall = deb2


def dprint(item1, item2=""):  # pragma: no cover
    if debug:
        print(item1, "%s%s%s" % (CLRtitle, item2, CLRnormal))


def dprintx(passeditem, special=False):  # pragma: no cover
    if debugall:
        if special:
            from pprint import pprint
            pprint(passeditem)
        else:
            print("%s%s%s" % (CLRtitle, passeditem, CLRnormal))
