from collections import Iterable

from lcdui.focus import FocusGrid
from lcdui.views import View


class Layout(View):
    def __init__(self, layout, parent=None):
        super().__init__(parent)
        self.layout = layout
        self.focus_grid = FocusGrid(parent.size, self.layout)
        self.size = (0, 0)  # to be calculated

    def __iter__(self):
        return iter(self.layout)

    def __getitem__(self, key):
        return self.layout[key]

    def handle(self, event):
        self.focus_grid.handle(event)

    def print(self, canvas, final=False):
        cols, rows = self.parent.size
        focused = []  # print focused views again at the end
        for i, row in enumerate(self.layout):
            if i >= rows:
                break  # no more rows on the screen

            if isinstance(row, Iterable):
                j = 0
                for w in row:
                    final = True
                    w_pos = (j, i)
                    canvas.position = w_pos
                    if w.focused:
                        final = False
                        focused.append((w_pos, w))
                    j += w.print(canvas.sub_canvas(*w.size), final=final)
                    if j >= cols - 1:
                        break  # no more space on this row
            else:
                w = row
                canvas.position = (0, i)
                w.print(canvas.sub_canvas(*w.size))

        if len(focused) > 0:
            for position, w in focused:
                canvas.position = position
                w.print(canvas.sub_canvas(*w.size), final=True)
