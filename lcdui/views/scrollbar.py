from lcdui.views import View


class VScrollBar(View):
    EMPTY_BAR = '|'
    POINTER = '#'

    def __init__(self, max_value=None, h=None, parent=None):
        super().__init__(parent=parent)
        self.h = h
        if h is None:
            self.h = parent.size[1]
        self.max_value = max_value
        if max_value is None:
            self.max_value = self.h - 1
        self.size = (1, self.h)
        self.value = 0

    def print(self, canvas, final=False):
        i = int(self.value / self.max_value * self.h)
        if i >= self.h:
            i = self.h - 1

        w = self.h // self.max_value
        if w == 0:
            w = 1

        s = [self.EMPTY_BAR] * self.h
        if i <= self.h - w:
            s[i:i + w] = [self.POINTER] * w
        else:
            s[self.h - w:] = [self.POINTER] * w

        printed = []
        for j, line in enumerate(s):
            canvas.position = (0, j)
            printed.append(canvas.print(line))
        canvas.position = (0, 0)
        return max(printed)
