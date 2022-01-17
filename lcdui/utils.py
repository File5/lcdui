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


def test():
    from RPLCD.i2c import CharLCD
    lcd = CharLCD('PCF8574', 0x27)
    lcd.clear()
    bitmap1 = (
        0b00000,
        0b01010,
        0b01010,
        0b00000,
        0b10001,
        0b10001,
        0b01110,
        0b00000,
    )
    bitmap2 = (
        0b00000,
        0b01010,
        0b01010,
        0b00000,
        0b01110,
        0b10001,
        0b10001,
        0b00000,
    )
    lcd.create_char(0, bitmap1)
    lcd.write(0x00)
    _ = input()
    lcd.create_char(0, bitmap2)
    lcd.close()


def digits():
    from RPLCD.i2c import CharLCD
    lcd = CharLCD('PCF8574', 0x27)
    lcd.clear()
    s1 = (
        0b01111,
        0b01111,
        0b01100,
        0b01100,
        0b01100,
        0b01100,
        0b01111,
        0b01111,
    )
    s2 = (
        0b11110,
        0b11110,
        0b00110,
        0b00110,
        0b00110,
        0b00110,
        0b11110,
        0b11110,
    )
    s3 = (
        0b01110,
        0b01110,
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b01110,
        0b01110,
    )
    s4 = (
        0b01111,
        0b01111,
        0b01100,
        0b01100,
        0b01100,
        0b00000,
        0b00000,
        0b00000,
    )
    s5 = (
        0b01100,
        0b01100,
        0b01100,
        0b01111,
        0b01111,
        0b00000,
        0b00000,
        0b00000,
    )
    s6 = (
        0b00110,
        0b00110,
        0b00110,
        0b11110,
        0b11110,
        0b00000,
        0b00000,
        0b00000,
    )
    s7 = (
        0b00000,
        0b00000,
        0b00000,
        0b01110,
        0b01110,#?
        0b00000,
        0b00000,
        0b00000,
    )
    s8 = (
        0b00110,
        0b00110,
        0b00110,
        0b00110,
        0b00110,
        0b00000,
        0b00000,
        0b00000,
    )
    segments = [s1, s2, s3, s4, s5, s6, s7, s8]
    for i, s in enumerate(segments):
        lcd.create_char(i, s)
    line1 = [4, 8, 0, 8, 3, 2, 3, 2, 5, 8, 1, 3, 1, 3, 4, 8, 1, 2, 1, 2]
    assert len(line1) == 20
    line2 = [5, 6, 0, 8, 5, 7, 7, 6, 0, 8, 7, 6, 5, 6, 0, 8, 5, 6, 7, 6]
    assert len(line2) == 20
    for s in line1 + line2:
        if s > 0:
            lcd.write(s - 1)
        else:
            lcd.write(ord(' '))
    lcd.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Helper utils")
    parser.add_argument('action', help="action to perform")
    args = parser.parse_args()
    if args.action == 'clear':
        clear()
    elif args.action == 'test':
        test()
    elif args.action == 'digits':
        digits()
