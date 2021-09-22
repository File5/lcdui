from lcdui.views import View


class Window(View):
    def __init__(self):
        self._lines = [
            'Text',
            'Label:' + '_' * (20 - 6),
            '<Button> (*)Radio',
            '|X|CheckBox'
        ]
        self.focus = None

    def handle(self, event):
        #print(event)
        pass

    @property
    def lines(self):
        return self._lines

    def __str__(self):
        return '\n'.join(self._lines)
