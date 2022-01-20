from lcdui.views import View
from lcdui.views.layout import Layout


class Window(View):
    layout = None

    def __init__(self, w=None, h=None):
        assert w and h or w is None and h is None
        self.size = (w, h)
        
        if self.layout is not None:
            self.layout = Layout(self.layout, self)
        else:
            self.layout = Layout([], self)
        self.focus = 0

    def handle(self, event):
        return self.layout.handle(event)

    def print(self, canvas, final=False):
        canvas.position = (0, 0)
        self.layout.print(canvas)

    def __str__(self):
        return '\n'.join(self._lines)
