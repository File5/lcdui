from RPLCD.i2c import CharLCD

from window import Window


def main():
    lcd = CharLCD('PCF8574', 0x27)
    w = Window()
    lcd.write_string(str(w))


if __name__ == "__main__":
    main()
