from lcdui.event import Event

from collections import Iterable


class FocusGrid:
    MOVE_EVENTS = (Event.UP, Event.DOWN, Event.LEFT, Event.RIGHT)

    class Cell:
        def __init__(self, pos, size, view, first=False, last=False):
            self.x, self.y = pos
            self.w, self.h = size
            self.view = view
            self.first = first
            self.last = last

        @property
        def pos(self):
            return self.x, self.y

        @property
        def size(self):
            return self.w, self.h

    def __init__(self, size, layout):
        self.size = size
        self._focus = (0, 0)
        self._grid = []
        
        cols, rows = self.size
        for y, row in enumerate(layout):
            if y >= rows:
                break  # no more rows on the screen

            grid_row = []
            first = True
            last_cell = None
            if isinstance(row, Iterable):
                x = 0
                for i, w in enumerate(row):
                    last = i == len(row) - 1
                    if w.focusable:
                        cell = self.Cell((x, y), w.size, w, first=first, last=last)
                        grid_row.append(cell)
                        first = False
                        last_cell = cell
                    x += w.size[0]

                    if x >= cols - 1:
                        break  # no more space on this row
                last_cell.last = True
            else:
                w = row
                if w.focusable:
                    first = last = True
                    grid_row.append(self.Cell((0, y), w.size, w, first=first, last=last))

            self._grid.append(grid_row)

    def __str__(self):
        result = []
        for row in self._grid:
            result_row = []
            for cell in row:
                first_str = '<' if cell.first else '{'
                last_str = '>' if cell.last else '}'
                if cell.w >= 3:
                    size_str = '{}x{}'.format(*cell.size)
                    if len(size_str) > cell.w - 2:
                        size_str = ' ' * (cell.w - 2)
                    else:
                        size_str_format = '{:^' + str(cell.w - 2) + '}'
                        size_str = size_str_format.format(size_str)
                    cell_str = '{}{}{}'.format(
                        first_str,
                        size_str,
                        last_str
                    )
                elif cell.w == 2:
                    cell_str = first_str + last_str
                elif cell.w == 1:
                    cell_str = 'l' if cell.last else 'o'
                    if cell.first:
                        cell_str = cell_str.upper()
                else:
                    cell_str = ''
                result_row.append(cell_str)
            result.append(result_row)
        return '\n'.join(map(lambda r: ''.join(r), result))

    def __getitem__(self, key):
        x, y = key
        row = self._grid[y]
        for cell in row:
            if cell.x <= x < cell.x + cell.w:
                return cell  # exact match

        # otherwise, find the nearest cell
        prev = None
        for cell in row:
            if x < cell.x:
                if prev is None:
                    return cell  # to the left of the first cell

                dist_prev = x - (prev.x + prev.w - 1)
                dist_cell = cell.x - x

                if dist_prev > dist_cell:
                    return cell  # between prev and cell (cell is closer)
                else:
                    return prev  # between prev and cell

            prev = cell

        # otherwise, just the last cell
        if row:
            return row[-1]  # rightmost
        return None

    def _find_prev(self, cell):
        x, y = cell.pos
        row = self._grid[y]
        prev = None
        for c in row:
            if c == cell:
                if prev is not None:
                    return prev.pos
            prev = c
        return cell.pos

    def _find_next(self, cell):
        x, y = cell.pos
        row = self._grid[y]
        prev = None
        for c in row:
            if prev is not None and prev == cell:
                return c.pos
            prev = c
        return cell.pos

    def handle(self, event):
        w, h = self.size
        x, y = self._focus
        cell = self[self._focus]
        if cell and event not in self.MOVE_EVENTS:
            cell.view.handle(event)
        if cell:
            cell.view.focused = False
        if event == Event.UP:
            if y > 0:
                y -= 1
                self._focus = (x, y)
        elif event == Event.DOWN:
            if y < h - 1:
                y += 1
                self._focus = (x, y)
        elif event == Event.LEFT:
            if cell and not cell.first and x > 0:
                #x -= (x - cell.x) + 1  # TODO find left neighbor
                x = self._find_prev(cell)[0]
                self._focus = (x, y)
        elif event == Event.RIGHT:
            if cell and not cell.last and x < w - 1:
                #x += cell.w
                x = self._find_next(cell)[0]
                self._focus = (x, y)
        cell = self[self._focus]
        if cell:
            cell.view.focused = True
