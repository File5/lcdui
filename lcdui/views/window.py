from lcdui.event import Event
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
        self._focusable_views = self.layout.focusable_views
        self._focusable_count = len(self._focusable_views)

    def handle(self, event):
        self._focusable_views[self.focus].focused = False
        if event == Event.DOWN:
            self.focus += 1
            if self.focus >= self._focusable_count:
                self.focus = self._focusable_count - 1
        elif event == Event.UP:
            self.focus -= 1
            if self.focus < 0:
                self.focus = 0
        self._focusable_views[self.focus].focused = True

    def print(self, canvas):
        canvas.position = (0, 0)
        self.layout.print(canvas)

    def __str__(self):
        return '\n'.join(self._lines)
