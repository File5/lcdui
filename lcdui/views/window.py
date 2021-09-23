from lcdui.views import View
from lcdui.views.layout import Layout
from lcdui.views.text import Text


class Window(View):
    def __init__(self, w=None, h=None):
        self._layout = Layout([
            Text('Title'),
            Text('Label:' + '_' * 14),
            Text('<Button> (*)Radio'),
            Text('|X|CheckBox'),
        ], self)
        assert w and h or w is None and h is None
        self.size = (w, h)
        self.focus = None

    def handle(self, event):
        #print(event)
        pass

    def print(self, canvas):
        canvas.position = (0, 0)
        self._layout.print(canvas)

    def __str__(self):
        return '\n'.join(self._lines)
