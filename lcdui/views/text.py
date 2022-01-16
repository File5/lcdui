from lcdui.views import View


class Text(View):
    def __init__(self, text="", parent=None):
        super().__init__(parent=parent)
        self.text = text
        self.size = (len(text), 1)
    
    def print(self, canvas, final=False):
        return canvas.print(self.text)
