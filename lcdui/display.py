from abc import ABCMeta

from lcdui.canvas import PrintCanvas
from lcdui.utils import ensure_line_count


class Display(metaclass=ABCMeta):
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.canvas = None

    @property
    def position(self):
        return self.canvas.position

    @position.setter
    def position(self, value):
        pass

    def print(self, line):
        pass

    def show(self, lines):
        self.position = x, y = (0, 0)
        for line in ensure_line_count(lines, self.rows):
            self.canvas.print(line[:self.cols])
            self.position = x, y = (0, y + 1)


class ConsoleDisplay(Display):
    PADDING_LINES = 2
    PADDING_IN_LINE = 2

    def __init__(self, cols=20, rows=4):
        super().__init__(cols, rows)
        self.canvas = PrintCanvas(self, (0, 0), (self.cols, self.rows))

    @property
    def position(self):
        return self.canvas.position

    @position.setter
    def position(self, value):
        col, row = self.position
        new_col, new_row = value
        col_diff, row_diff = (new_col - col), (new_row - row)
        if row_diff > 0:
            print('\033[{}B'.format(row_diff))
        elif row_diff < 0:
            print('\033[{}A'.format(-row_diff))
        if col_diff > 0:
            print('\033[{}C'.format(col_diff))
        elif col_diff < 0:
            print('\033[{}D'.format(-col_diff))

    def print(self, line):
        print(line, end='')

    def show(self, lines):
        self.position = (0, 0)
        print('┌' + '─' * self.cols + '┐')
        for line in ensure_line_count(lines, self.rows):
            print('│{:<20s}│'.format(line))
        print('└' + '─' * self.cols + '┘')

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
