from display import ConsoleDisplay
from event import Event
from views.window import Window
from utils import getch


def main():
    display = ConsoleDisplay()
    w = Window()
    display.show(w.lines)
    display.canvas.position = (2, 1)
    canvas = display.canvas.sub_canvas(16, 2)
    while True:
        c = getch()
        x, y = canvas.position

        if c == 'q':
            break
        elif c == 'A' and y > 0:
            canvas.position = x, y - 1
            w.handle(Event.UP)
        elif c == 'B' and y < canvas.size[1] - 1:
            canvas.position = x, y + 1
            w.handle(Event.DOWN)
        elif c == 'D' and x > 0:
            canvas.position = x - 1, y
            w.handle(Event.LEFT)
        elif c == 'C' and x < canvas.size[0] - 1:
            canvas.position = x + 1, y
            w.handle(Event.RIGHT)
        elif c == 'x':
            canvas.print('x')


if __name__ == "__main__":
    main()
