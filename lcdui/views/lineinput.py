from lcdui.display import Cursor
from lcdui.views import View


class LineInput(View):
    def __init__(self, width=5, placeholder='_', parent=None):
        super().__init__(parent=parent)
        self.focusable = True
        self.focused = False
        self.width = width
        self.placeholder = placeholder
        self.size = (width, 1)
    
    def print(self, canvas):
        printed = canvas.print(self.placeholder * self.width)
        canvas.position = (0, 0)
        if self.focused:
            canvas.cursor = Cursor.BLOCK
        else:
            canvas.cursor = Cursor.NONE
        return printed
