from collections import Iterable


class FocusGrid:

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
            if isinstance(row, Iterable):
                x = 0
                for i, w in enumerate(row):
                    first = x == 0
                    last = i == len(row) - 1
                    cell = self.Cell((x, y), w.size, w, first=first, last=last)
                    grid_row.append(cell)
                    x += w.size[0]

                    if x >= cols - 1:
                        break  # no more space on this row
            else:
                w = row
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
