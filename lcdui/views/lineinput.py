from lcdui.display import Cursor
from lcdui.views import View


class LineInput(View):
    def __init__(self, width=5, placeholder='_', parent=None):
        super().__init__(parent=parent)
        self.width = width
        self.placeholder = placeholder
        self.size = (width, 1)
    
    def print(self, canvas):
        printed = canvas.print(self.placeholder * self.width)
        canvas.position = (0, 0)
        canvas.cursor = Cursor.BLOCK
        return printed
