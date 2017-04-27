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
except ImportError:  # pragma: no cover
    # No colorama, so let's fallback to no-color mode
    GREEN = YELLOW = RED = BLUE = CYAN = WHITE = ''

C_NORM = WHITE
C_HEAD = GREEN
C_HEAD2 = BLUE
C_TI = CYAN
C_TI2 = YELLOW
C_GOOD = GREEN
C_WARN = YELLOW
C_ERR = RED

C_STAT = {"running": C_GOOD, "start": C_GOOD, "ssh": C_GOOD,
          "stopped": C_ERR, "stop": C_ERR, "stopping": C_WARN,
          "pending": C_WARN, "starting": C_WARN}
