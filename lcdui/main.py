from display import ConsoleDisplay, RPLCDDisplay
from event import Event
from lcdui.views import Window, Text
from utils import getch


class MainWindow(Window):
    layout = [
        Text('Title'),
        Text('Label:' + '_' * 14),
        Text('<Button> (*)Radio'),
        Text('|X|CheckBox'),
    ]


def main():
    ESC = '\033'
    MOVE_SEQ = [ESC, '[']
    display = ConsoleDisplay()
    display.show([''] * 4)  # draw the display
    w = MainWindow(20, 4)
    display.canvas.position = (0, 0)
    canvas = display.canvas.sub_canvas(20, 4)
    w.print(canvas)
    canvas.position = (0, 0)
    #display.cursor_mode = 'blink'
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
                canvas.position = x, y - 1
                w.handle(Event.UP)
        elif seq == MOVE_SEQ + ['B']:
            if y < canvas.size[1] - 1:
                canvas.position = x, y + 1
                w.handle(Event.DOWN)
        elif seq == MOVE_SEQ + ['D']:
            if x > 0:
                canvas.position = x - 1, y
                w.handle(Event.LEFT)
        elif seq == MOVE_SEQ + ['C']:
            if x < canvas.size[0] - 1:
                canvas.position = x + 1, y
                w.handle(Event.RIGHT)
        elif seq[-1] != ESC and seq[-2:] != MOVE_SEQ:
            canvas.print(c)


if __name__ == "__main__":
    main()
