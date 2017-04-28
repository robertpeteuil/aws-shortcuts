"""Getchar Module holding cross-platform class for reading single keypresses

When the object is instantiated, it configures itself for the operating
system in use (windows or linux/mac).

Called directly - the object returns the key pressed.
Called via the int method - the object coverted the key pressed into
int and returns it.  If the key pressed cannot be converted to int,
then the string "999" is returned.
"""

from builtins import object


class _Getch(object):
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):     # pragma: no cover
        return self.impl()

    def int(self):          # pragma: no cover
        """ Coverts a read keystroke to int or returns "999" """
        try:
            value = int(self.impl())
        except ValueError:
            value = "999"
        return value


class _GetchUnix(object):
    def __init__(self):
        import tty          # noqa: F401 pylint: disable=unused-variable
        import sys          # noqa: F401 pylint: disable=unused-variable

    def __call__(self):     # pragma: no cover
        import sys          # noqa: F401
        import tty          # noqa: F401
        import termios      # noqa: F401
        file_desc = sys.stdin.fileno()
        old_settings = termios.tcgetattr(file_desc)
        try:
            tty.setraw(sys.stdin.fileno())
            chr_read = sys.stdin.read(1)
        finally:
            termios.tcsetattr(file_desc, termios.TCSADRAIN, old_settings)
        return chr_read


class _GetchWindows(object):
    def __init__(self):
        # pylint: disable=unused-variable,import-error
        import msvcrt       # noqa: F401

    def __call__(self):     # pragma: no cover
        import msvcrt       # pylint: disable=import-error
        return msvcrt.getch()
