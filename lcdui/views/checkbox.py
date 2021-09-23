from lcdui.views import View


class CheckBox(View):
    PREFIX = '|'
    SUFFIX = '|'
    SELECTED = 'X'
    DESELECTED = ' '

    FORMAT = '{}{}{}{}'

    def __init__(self, text="", parent=None):
        super().__init__(parent=parent)
        self.text = text
        self.size = (len(text) + 3, 1)
    
    def print(self, canvas):
        return canvas.print(self.FORMAT.format(
            self.PREFIX, self.SELECTED, self.SUFFIX, self.text
        ))
