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
        self._position = value
        px, py = self.parent_position
        x, y = value
        self.parent.position = (px + x, py + y)

    def print(self, line):
        self.display.print(line)

    def sub_canvas(self, size):
        return PrintCanvas(self, self.position, size)
