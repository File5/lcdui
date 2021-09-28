from lcdui.views import View


class Radio(View):
    PREFIX = '('
    SUFFIX = ')'
    FOCUSED_PREFIX = '['
    FOCUSED_SUFFIX = ']'
    SELECTED = '*'
    DESELECTED = ' '

    FORMAT = '{}{}{}{}'

    def __init__(self, text="", parent=None):
        super().__init__(parent=parent)
        self.focusable = True
        self.focused = False
        self.text = text
        self.size = (len(text) + 3, 1)
    
    def print(self, canvas):
        if self.focused:
            prefix = self.FOCUSED_PREFIX
            suffix = self.FOCUSED_SUFFIX
        else:
            prefix = self.PREFIX
            suffix = self.SUFFIX

        return canvas.print(self.FORMAT.format(
            prefix, self.SELECTED, suffix, self.text
        ))
