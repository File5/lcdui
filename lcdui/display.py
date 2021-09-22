from abc import ABCMeta

from lcdui.canvas import PrintCanvas
from lcdui.utils import ensure_line_count


class Display(metaclass=ABCMeta):
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.canvas = PrintCanvas(self, (0, 0), (self.cols, self.rows))

    @property
    def position(self):
        return self.canvas.position

    @position.setter
    def position(self, value):
        pass

    def print(self, line):
        pass

    def show(self, lines):
        self.canvas.position = x, y = (0, 0)
        for i, line in enumerate(ensure_line_count(lines, self.rows)):
            self.canvas.print(line[:self.cols])
            if i < self.rows - 1:
                self.canvas.position = x, y = (0, y + 1)


class ConsoleDisplay(Display):
    PADDING_LINES = 2
    PADDING_IN_LINE = 2

    def __init__(self, cols=20, rows=4):
        super().__init__(cols, rows)
        self._position = (0, 0)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        col, row = self.position
        new_col, new_row = value
        col_diff, row_diff = (new_col - col), (new_row - row)
        if row_diff > 0:
            print('\033[{}B'.format(row_diff), end='')
        elif row_diff < 0:
            print('\033[{}A'.format(-row_diff), end='')
        if col_diff > 0:
            print('\033[{}C'.format(col_diff), end='')
        elif col_diff < 0:
            print('\033[{}D'.format(-col_diff), end='')
        self._position = value

    def print(self, line):
        x, y = self._position
        remaining = self.cols - x
        print(line[:remaining], end='')
        printed = len(line[:remaining])
        self._position = x + printed, y

        x, y = self._position
        if x >= self.cols:
            self.position = x - 1, y
            printed -= 1
        return printed

    def show(self, lines):
        self.canvas.position = (0, 0)
        print('┌' + '─' * self.cols + '┐')
        for line in ensure_line_count(lines, self.rows):
            print('│{:<20s}│'.format(line))
        print('└' + '─' * self.cols + '┘')
        print('\033[{}F\033[1C'.format(1 + self.rows), end='')

    def clear(self):
        self.show([''] * self.rows)


class RPLCDDisplay(Display):
    NEWLINE = '\r\n'

    def __init__(self, cols=20, rows=4, lcd=None):
        super().__init__(cols, rows)
        if lcd:
            self.lcd = lcd
        else:
            from RPLCD.i2c import CharLCD
            self.lcd = CharLCD('PCF8574', 0x27)

    @property
    def position(self):
        return self.lcd.cursor_pos[::-1]

    @position.setter
    def position(self, value):
        self.lcd.cursor_pos = value[::-1]

    @property
    def cursor_mode(self):
        return self.lcd.cursor_mode

    @cursor_mode.setter
    def cursor_mode(self, value):
        self.lcd.cursor_mode = value

    def print(self, line):
        x, y = self.position
        remaining = self.cols - x
        self.lcd.write_string(line[:remaining])
        printed = len(line[:remaining])

        if x + printed < self.cols:
            self.position = x + printed, y
        else:
            self.position = self.cols - 1, y
            return self.cols - 1 - x
        return printed

    def clear(self):
        self.lcd.clear()
