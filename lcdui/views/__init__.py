from abc import ABCMeta


class View(metaclass=ABCMeta):
    def __init__(self, parent=None):
        self.parent = parent
        self.size = (0, 0)

    def print(self, canvas):
        pass
