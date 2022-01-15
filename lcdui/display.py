from abc import ABCMeta
from enum import Enum

from lcdui.canvas import PrintCanvas
from lcdui.utils import ensure_line_count


class Cursor(Enum):
    NONE = 0
    BLOCK = 1
    UNDERLINE = 2


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

    @property
    def cursor(self):
        return Cursor.NONE

    @cursor.setter
    def cursor(self, value):
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

    @property
    def cursor(self):
        return Cursor.BLOCK
    
    @cursor.setter
    def cursor(self, value):
        pass

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


class BufferedMixin:
    def __init__(self, cols=20, rows=4):
        super().__init__(cols, rows)
        self.buffer = [' ' * cols] * rows
        self._buffer_position = (0, 0)
        self._cursor = super(BufferedMixin, self).cursor

    @property
    def position(self):
        return super(BufferedMixin, self).position

    @position.setter
    def position(self, value):
        self._buffer_position = value
        if self._cursor != Cursor.NONE:
            super(BufferedMixin, self.__class__).position.fset(self, value)

    @property
    def cursor(self):
        return self._cursor
    
    @cursor.setter
    def cursor(self, value):
        if value != self._cursor:
            self._cursor = value
            super(BufferedMixin, self.__class__).cursor.fset(self, value)
        if value != Cursor.NONE:
            self.position = self._buffer_position  # show cursor at position

    def print(self, line):
        x, y = self._buffer_position
        remaining = self.cols - x
        to_write = line[:remaining]
        existing = self.buffer[y][x:x + len(to_write)]
        if to_write != existing:
            self.buffer[y] = self.buffer[y][:x] + line[:len(to_write)] + self.buffer[y][x + len(to_write):]
            super(BufferedMixin, self.__class__).position.fset(self, self._buffer_position)
            printed = super().print(to_write)
        else:
            printed = len(existing)
        if x + printed < self.cols:
            self._buffer_position = x + printed, y
        else:
            self._buffer_position = self.cols - 1, y
            return self.cols - 1 - x
        return printed

    def clear(self):
        super().clear()
        self.buffer = [' ' * self.cols] * self.rows
        self._buffer_position = super(BufferedMixin, self).position
        self._cursor = super(BufferedMixin, self).cursor


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
    def cursor(self):
        if self.lcd.cursor_mode == 'hide':
            return Cursor.NONE
        elif self.lcd.cursor_mode == 'blink':
            return Cursor.BLOCK
        elif self.lcd.cursor_mode == 'line':
            return Cursor.UNDERLINE

    @cursor.setter
    def cursor(self, value):
        if value == Cursor.NONE:
            self.lcd.cursor_mode = 'hide'
        elif value == Cursor.BLOCK:
            self.lcd.cursor_mode = 'blink'
        elif value == Cursor.UNDERLINE:
            self.lcd.cursor_mode = 'line'

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


class BufferedConsoleDisplay(BufferedMixin, ConsoleDisplay):
    pass


class BufferedRPLCDDisplay(BufferedMixin, RPLCDDisplay):
    pass
