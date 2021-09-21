from unittest.mock import patch

import io
from lcdui.display import ConsoleDisplay


stdout = io.StringIO()


@patch('sys.stdout', new=stdout)
def test_console_display():
    c = ConsoleDisplay(20, 4)
    c.show([
        'Hello',
        'World',
        '!',
        ''
    ])
    assert stdout.getvalue() == '''\
┌────────────────────┐
│Hello               │
│World               │
│!                   │
│                    │
└────────────────────┘
'''
