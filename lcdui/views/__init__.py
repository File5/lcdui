from abc import ABCMeta


__all__ = ['View', 'Button', 'CheckBox', 'Radio', 'Text', 'LineInput', 'Window']


class View(metaclass=ABCMeta):
    def __init__(self, parent=None):
        self.parent = parent
        self.size = (0, 0)
        self.focusable = False
        self.focused = False

    @property
    def focusable_views(self):
        if self.focusable:
            return [self]
        else:
            return []

    def print(self, canvas):
        pass


from lcdui.views.button import Button
from lcdui.views.checkbox import CheckBox
from lcdui.views.radio import Radio
from lcdui.views.text import Text
from lcdui.views.lineinput import LineInput
from lcdui.views.window import Window
