'''Module holding constants used to format lines that are printed to the
terminal.
'''

import sys
try:
    import colorama
    colorama.init(strip=(not sys.stdout.isatty()))
    GREEN, YELLOW, RED = (colorama.Fore.GREEN, colorama.Fore.YELLOW,
                          colorama.Fore.RED)
    BLUE, CYAN, WHITE = (colorama.Fore.BLUE, colorama.Fore.CYAN,
                         colorama.Fore.WHITE)
    # BRIGHT, RESET = colorama.Style.BRIGHT, colorama.Style.RESET_ALL
except ImportError:  # pragma: no cover
    # No colorama, so let's fallback to no-color mode
    GREEN = YELLOW = RED = BLUE = CYAN = WHITE = ''

CLRnormal = WHITE
CLRheading = GREEN
CLRheading2 = BLUE
CLRtitle = CYAN
CLRtitle2 = YELLOW
CLRsuccess = GREEN
CLRwarning = YELLOW
CLRerror = RED

statCLR = {"running": CLRsuccess, "start": CLRsuccess, "ssh": CLRsuccess,
           "stopped": CLRerror, "stop": CLRerror, "stopping": CLRwarning,
           "pending": CLRwarning, "starting": CLRwarning}
