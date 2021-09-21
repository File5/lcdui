class Window:
    def __init__(self):
        self.lines = [
            'Text',
            'Label:' + '_' * (20 - 6),
            '<Button> (*)Radio',
            '|X|CheckBox'
        ]
        self.focus = None

    def handle(self, event):
        pass

    def __str__(self):
        return '\r\n'.join(self.lines)
