from lcdui.views.lineinput import LineInput
from lcdui.display import BufferedConsoleDisplay, BufferedRPLCDDisplay, Cursor
from lcdui.event import Event
from lcdui.views import Window, Button, CheckBox, Radio, Text, LineInput
from lcdui.utils import getch


def focused(view):
    view.focused = True
    return view


class MainWindow(Window):
    layout = [
        Text('Title'),
        [Text('Label:'), LineInput(14)],
        [Button('Button'), Text(' '), Radio('Radio')],
        CheckBox('CheckBox'),
    ]


def main():
    ESC = '\033'
    MOVE_SEQ = [ESC, '[']
    display = BufferedConsoleDisplay()
    display.show([''] * 4)  # draw the display
    w = MainWindow(20, 4)
    display.canvas.position = (0, 0)
    canvas = display.canvas.sub_canvas(20, 4)
    w.print(canvas)
    canvas.position = (0, 0)
    display.cursor = Cursor.BLOCK
    seq = []
    while True:
        c = getch()
        seq.append(c)
        seq = seq[-3:]
        x, y = canvas.position

        if seq[-2:] == [ESC] * 2:
            break
        elif seq == MOVE_SEQ + ['A']:
            if y > 0:
                pass#canvas.position = x, y - 1
            w.handle(Event.UP)
        elif seq == MOVE_SEQ + ['B']:
            if y < canvas.size[1] - 1:
                pass#canvas.position = x, y + 1
            w.handle(Event.DOWN)
        elif seq == MOVE_SEQ + ['D']:
            if x > 0:
                pass#canvas.position = x - 1, y
            w.handle(Event.LEFT)
        elif seq == MOVE_SEQ + ['C']:
            if x < canvas.size[0] - 1:
                pass#canvas.position = x + 1, y
            w.handle(Event.RIGHT)
        elif seq[-1] != ESC and seq[-2:] != MOVE_SEQ:
            canvas.print(c)
        w.print(canvas)
        x, y = w.size
        canvas.position = w.layout.focus_grid._focus
        display.cursor = Cursor.BLOCK


if __name__ == "__main__":
    main()
