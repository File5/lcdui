from lcdui.display import Cursor
from lcdui.event import EventType
from lcdui.views import View


class LineInput(View):
    BACKSPACE = '\x7f'

    def __init__(self, width=5, placeholder='_', parent=None):
        super().__init__(parent=parent)
        self.focusable = True
        self.focused = False
        self.width = width
        self.placeholder = placeholder
        self.size = (width, 1)
        self.value = ''
    
    def print(self, canvas, final=False):
        f = '{:' + self.placeholder + '<' + str(self.width) + '}'
        s = f.format(self.value)
        printed = canvas.print(s)
        canvas.position = (len(self.value), 0)
        if final and self.focused:
            canvas.cursor = Cursor.BLOCK
        else:
            canvas.cursor = Cursor.NONE
        return printed

    def handle(self, event):
        if event.type == EventType.INPUT:
            if len(self.value) < self.width:
                if event.value == self.BACKSPACE:
                    self.value = self.value[:-1]
                else:
                    self.value += event.value
                return True
        return False
