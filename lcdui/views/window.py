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

    def print(self, canvas):
        for i, line in enumerate(self._lines):
            canvas.position = (0, i)
            canvas.print(line)

    def __str__(self):
        return '\n'.join(self._lines)
