# BetterCurses - gutter.py
# github.com/leftbones/bettercurses

# To Do
# - Retrieve and print in proper colors from parent's color theme
# - Add "relative" line number mode

import curses

from widget import Widget

class Gutter(Widget):
    """
    Prints a gutter on the left side of a window with line numbers and tildes representing empty lines
    Could be expanded to show folding symbols, git symbols, etc.
    """

    def __init__(self, parent, row, col, nrows, ncols, offset):
        super().__init__(parent, row, col, nrows, ncols)
        self.offset = offset
        self.parent.edge_left += self.offset

    def print(self):
        for row in range(self.parent.nrows - self.parent.edge_upper):
            line_number = " " * (self.offset - len(str(row + self.parent.row_offset + 1))) + str(row + self.parent.row_offset + 1)

            if row == self.parent.cursor_row - self.parent.row_offset:
                self.parent.screen.insstr(self.parent.edge_upper + row, self.col, line_number)
            else:
                self.parent.screen.insstr(self.parent.edge_upper + row, self.col, line_number, curses.A_DIM)
