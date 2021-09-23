class PrintCanvas:
    def __init__(self, parent, parent_position, size):
        self.parent = parent
        self.parent_position = parent_position
        self.size = size
        self._position = (0, 0)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        px, py = self.parent_position
        x, y = value
        self.parent.position = (px + x, py + y)
        self._position = value

    @property
    def cursor(self):
        return self.parent.cursor

    @cursor.setter
    def cursor(self, value):
        self.parent.cursor = value

    def print(self, line):
        x, y = self._position
        remaining = self.size[0] - x
        printed = self.parent.print(line[:remaining])
        self._position = (x + printed, y)
        return printed


    def sub_canvas(self, w, h):
        return PrintCanvas(self, self.position, (w, h))
