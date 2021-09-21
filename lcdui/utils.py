#https://stackoverflow.com/a/28143542
def getch():
    import termios
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    return _getch()


def ensure_line_count(lines, count):
    if len(lines) < count:
        lines.extend([''] * (count - len(lines)))
    elif len(lines) > count:
        lines = lines[:count]
    return lines
