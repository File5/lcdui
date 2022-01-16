from lcdui.views import View


class Button(View):
    PREFIX = '<'
    SUFFIX = '>'
    FOCUSED_PREFIX = '['
    FOCUSED_SUFFIX = ']'

    def __init__(self, text="", parent=None):
        super().__init__(parent=parent)
        self.focusable = True
        self.focused = False
        self.text = text
        self.size = (len(text) + 2, 1)
    
    def print(self, canvas, final=False):
        if self.focused:
            prefix = self.FOCUSED_PREFIX
            suffix = self.FOCUSED_SUFFIX
        else:
            prefix = self.PREFIX
            suffix = self.SUFFIX

        return canvas.print(prefix + self.text + suffix)
