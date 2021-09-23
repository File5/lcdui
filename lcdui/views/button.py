from lcdui.views import View


class Button(View):
    PREFIX = '<'
    SUFFIX = '>'

    def __init__(self, text="", parent=None):
        super().__init__(parent=parent)
        self.text = text
        self.size = (len(text) + 2, 1)
    
    def print(self, canvas):
        return canvas.print(self.PREFIX + self.text + self.SUFFIX)
