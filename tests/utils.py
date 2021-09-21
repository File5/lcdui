from lcdui.utils import ensure_line_count


def test_ensure_line_count():
    assert ensure_line_count([''], 4) == [''] * 4
    assert ensure_line_count(['a', 'b', 'c'], 4) == ['a', 'b', 'c', '']
    assert ensure_line_count([''] * 10, 4) == [''] * 4
    assert ensure_line_count(
        [i for i in 'abcdef'] * 10, 4
    ) == ['a', 'b', 'c', 'd']
