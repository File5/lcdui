from abc import ABCMeta


__all__ = ['View', 'Text', 'Window']


class View(metaclass=ABCMeta):
    def __init__(self, parent=None):
        self.parent = parent
        self.size = (0, 0)

    def print(self, canvas):
        pass


from lcdui.views.text import Text
from lcdui.views.window import Window
