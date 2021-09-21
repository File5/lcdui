from unittest.mock import patch

import io
from lcdui.display import ConsoleDisplay


stdout_factory = lambda: io.StringIO()


@patch('sys.stdout', new_callable=stdout_factory)
def test_console_display(stdout):
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


@patch('sys.stdout', new_callable=stdout_factory)
def test_console_display_less_lines(stdout):
    c = ConsoleDisplay(20, 4)
    c.show([
        'Hello',
        'World'
    ])
    assert stdout.getvalue() == '''\
┌────────────────────┐
│Hello               │
│World               │
│                    │
│                    │
└────────────────────┘
'''


@patch('sys.stdout', new_callable=stdout_factory)
def test_console_display_more_lines(stdout):
    c = ConsoleDisplay(20, 4)
    c.show([
        'Hello',
        'World',
        'test1',
        'test2',
        'test3',
        'test4',
    ])
    assert stdout.getvalue() == '''\
┌────────────────────┐
│Hello               │
│World               │
│test1               │
│test2               │
└────────────────────┘
'''
