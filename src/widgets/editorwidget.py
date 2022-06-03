# BetterCurses - editorwidget.py
# github.com/leftbones/bettercurses

# To Do
# - Retrieve and print in proper colors from parent's color theme
# - Add "relative" line number mode (Gutter)

import curses

from widget import Widget

class EditorWidget(Widget):
    """
    Prints lines from a file, allows editing of characters, lines, words, etc.

    Also prints a gutter on the left side of a window with line numbers and tildes representing empty lines
    Could be expanded to show folding symbols, git symbols, etc.
    """

    def __init__(self, parent, row, col, nrows, ncols, contents, offset):
        self.parent = parent
        self.contents = contents
        self.offset = offset

        self.parent.edge_left += self.offset

    def print(self):
        for row, line in enumerate(self.contents[self.parent.row_offset:self.parent.row_offset + (self.nrows - self.parent.lower_edge - 1)]):
            # Gutter
            line_number = " " * (self.offset - len(str(row + self.parent.row_offset + 1))) + str(row + self.parent.row_offset + 1)

            if row == self.parent.cursor_row - self.parent.row_offset:
                self.parent.screen.insstr(self.parent.edge_upper + row, self.col, line_number)
            else:
                self.parent.screen.insstr(self.parent.edge_upper + row, self.col, line_number, curses.A_DIM)

            # Contents
            line_text = line[self.parent.col_offset:self.parent.col_offset + self.ncols - self.parent.edge_left]
            self.parent.screen.insstr(self.parent.edge_upper + row, self.parent.edge_left, line_text)
