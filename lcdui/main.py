from display import ConsoleDisplay
from event import Event
from views.window import Window
from utils import getch


def main():
    display = ConsoleDisplay()
    w = Window()
    display.show(w.lines)
    while True:
        c = getch()
        x, y = display.position

        if c == 'q':
            break
        elif c == 'A' and y > 0:
            display.position = x, y - 1
            w.handle(Event.UP)
        elif c == 'B' and y < display.rows - 1:
            display.position = x, y + 1
            w.handle(Event.DOWN)
        elif c == 'D' and x > 0:
            display.position = x - 1, y
            w.handle(Event.LEFT)
        elif c == 'C' and x < display.cols - 1:
            display.position = x + 1, y
            w.handle(Event.RIGHT)
        elif c == 'x':
            display.print('x')


if __name__ == "__main__":
    main()
