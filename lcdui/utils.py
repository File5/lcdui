import argparse

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


def clear():
    from RPLCD.i2c import CharLCD
    lcd = CharLCD('PCF8574', 0x27)
    lcd.clear()
    lcd.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Helper utils")
    parser.add_argument('action', help="action to perform")
    args = parser.parse_args()
    if args.action == 'clear':
        clear()
