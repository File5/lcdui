from collections import Iterable
from lcdui.views import View


class Layout(View):
    def __init__(self, layout, parent=None):
        super().__init__(parent)
        self.layout = layout
        self.size = (0, 0)  # to be calculated

    def __iter__(self):
        return iter(self.layout)

    def __getitem__(self, key):
        return self.layout[key]

    @property
    def focusable_views(self):
        children = []
        for row in self.layout:
            if isinstance(row, Iterable):
                for w in row:
                    children.extend(w.focusable_views)
            else:
                w = row
                children.extend(w.focusable_views)
        return children

    def print(self, canvas):
        cols, rows = self.parent.size
        for i, row in enumerate(self.layout):
            if i >= rows:
                break  # no more rows on the screen

            if isinstance(row, Iterable):
                j = 0
                for w in row:
                    canvas.position = (j, i)
                    j += w.print(canvas.sub_canvas(*w.size))
                    if j >= cols - 1:
                        break  # no more space on this row
            else:
                w = row
                canvas.position = (0, i)
                w.print(canvas.sub_canvas(*w.size))
