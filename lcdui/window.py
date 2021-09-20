class Window:
    def __init__(self):
        pass

    def __str__(self):
        return 'Text\r\n' + \
               'Label:' + '_' * (20 - 6) + '\r\n' + \
               '<Button> (*)Radio\r\n' + \
               '|X|CheckBox'
