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
        if c == 'q':
            break
        elif c == 'i':
            w.handle(Event.UP)
        elif c == 'k':
            w.handle(Event.DOWN)
        elif c == 'j':
            w.handle(Event.LEFT)
        elif c == 'l':
            w.handle(Event.RIGHT)


if __name__ == "__main__":
    main()
