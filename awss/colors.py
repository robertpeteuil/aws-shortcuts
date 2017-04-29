"""Determine color capability, define color vars and theme."""

import sys

try:
    import colorama
    colorama.init(strip=(not sys.stdout.isatty()))
    GREEN, YELLOW, RED = (colorama.Fore.GREEN, colorama.Fore.YELLOW,
                          colorama.Fore.RED)
    BLUE, CYAN, WHITE = (colorama.Fore.BLUE, colorama.Fore.CYAN,
                         colorama.Fore.WHITE)
except ImportError:  # pragma: no cover
    # No colorama, fallback to no-color mode
    GREEN = YELLOW = RED = BLUE = CYAN = WHITE = ''

# Create 'color theme' by aliasing color vars to vars that
#       are imported and used by other modules.
#   User can change colors used in modules by simply changing
#       their assignment here, thus avoiding having to change
#       the color var-name throughout the module.
C_NORM = WHITE
C_HEAD = GREEN
C_HEAD2 = BLUE
C_TI = CYAN
C_TI2 = YELLOW
C_GOOD = GREEN
C_WARN = YELLOW
C_ERR = RED

# Color dictionary for setting color names for item status of commands
C_STAT = {"running": C_GOOD, "start": C_GOOD, "ssh": C_GOOD,
          "stopped": C_ERR, "stop": C_ERR, "stopping": C_WARN,
          "pending": C_WARN, "starting": C_WARN}
