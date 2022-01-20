from lcdui.views import View


class ListItem(View):
    PREFIX = ' '
    SUFFIX = ' '
    FOCUSED_PREFIX = '['
    FOCUSED_SUFFIX = ']'

    def __init__(self, text="", width=None, parent=None):
        super().__init__(parent=parent)
        self.text = text
        self.width = width
        if width is None:
            self.width = len(text) + 2
        self.size = (self.width, 1)
        self.focusable = True
        self.text_format = '{}{:<%d}{}' % (self.width - 2)

    def print(self, canvas, final=False):
        if self.focused:
            prefix = self.FOCUSED_PREFIX
            suffix = self.FOCUSED_SUFFIX
        else:
            prefix = self.PREFIX
            suffix = self.SUFFIX
        s = self.text_format.format(prefix, self.text, suffix)
        return canvas.print(s)
