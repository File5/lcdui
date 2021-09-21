from abc import ABCMeta

from lcdui.utils import ensure_line_count


class Display(metaclass=ABCMeta):
    def show(self, lines):
        pass


class ConsoleDisplay(Display):
    PADDING_LINES = 2
    PADDING_IN_LINE = 2

    def __init__(self, cols=20, rows=4):
        self.cols = cols
        self.rows = rows
        self._need_go_back = False

    def show(self, lines):
        self._go_back()
        print('┌' + '─' * self.cols + '┐')
        for line in ensure_line_count(lines, self.rows):
            print('│{:<20s}│'.format(line))
        print('└' + '─' * self.cols + '┘')
        self._need_go_back = True

    def _go_back(self):
        if self._need_go_back:
            print('\033[{}F'.format(self.rows + self.PADDING_LINES + 1))
            self._need_go_back = False

    def clear(self):
        self.show([''] * self.rows)


class RPLCDDisplay(Display):
    NEWLINE = '\r\n'

    def __init__(self, cols=20, rows=4, lcd=None):
        self.cols = cols
        self.rows = rows
        if lcd:
            self.lcd = lcd
        else:
            from RPLCD.i2c import CharLCD
            self.lcd = CharLCD('PCF8574', 0x27)

    def show(self, lines):
        self._go_back()
        for i, line in enumerate(ensure_line_count(lines, self.rows)):
            end = self.NEWLINE if i < len(lines) - 1 else ''
            self.lcd.write_string(line + end)

    def clear(self):
        self.lcd.clear()
