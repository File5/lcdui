from RPLCD.i2c import CharLCD

from event import Event
from window import Window
from utils import getch


def main():
    lcd = CharLCD('PCF8574', 0x27)
    w = Window()
    lcd.write_string(str(w))
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
