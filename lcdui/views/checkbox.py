from lcdui.event import EventType
from lcdui.views import View


class CheckBox(View):
    PREFIX = '|'
    SUFFIX = '|'
    FOCUSED_PREFIX = '['
    FOCUSED_SUFFIX = ']'
    SELECTED = 'X'
    DESELECTED = ' '

    FORMAT = '{}{}{}{}'

    def __init__(self, text="", parent=None):
        super().__init__(parent=parent)
        self.focusable = True
        self.focused = False
        self.text = text
        self.size = (len(text) + 3, 1)
        self.checked = False
    
    def print(self, canvas, final=False):
        if self.focused:
            prefix = self.FOCUSED_PREFIX
            suffix = self.FOCUSED_SUFFIX
        else:
            prefix = self.PREFIX
            suffix = self.SUFFIX
        if self.checked:
            value = self.SELECTED
        else:
            value = self.DESELECTED

        return canvas.print(self.FORMAT.format(
            prefix, value, suffix, self.text
        ))

    def handle(self, event):
        if event.type == EventType.ACTION:
            self.checked = not self.checked
            return True
        return False
