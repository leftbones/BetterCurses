# BetterCurses - cursor.py
# github.com/leftbones/bettercurses

class Cursor:
    """
    Handler class for positioning the cursor as well as moving it around the screen and keeping it in bounds
    """

    def __init__(self, parent):
        self.parent = parent
        self.window = None
        self.row = 0
        self.col = 0

    def update(self):
        """
        Update the current window's cursor memory
        """
        self.window.cursor_row = self.row
        self.window.cursor_col = self.col

    def move_window(self, window):
        """
        Move the cursor to a different window and update it's position to the window's cursor memory
        """
        self.window = window
        self.row = self.window.cursor_row
        self.col = self.window.cursor_col

    """
    Move cursor up/down/left/right one row/col
    """
    def move_up(self):
        if self.row > 0:
            self.row -= 1
            self.update()
            self.window.scroll(self)

    def move_down(self):
        if self.row < self.window.nrows - self.window.edge_lower - self.window.edge_upper:
            self.row += 1
            self.update()
            self.window.scroll(self)

    def move_left(self):
        if self.col > 0:
            self.col -= 1
            self.update()
            self.window.scroll(self)

    def move_right(self):
        if self.col < self.window.ncols - self.window.edge_right - self.window.edge_left:
            self.col += 1
            self.update()
            self.window.scroll(self)

    """
    Shift window up/down/left/right one row/col
    """
    def shift_up(self):
        if self.window.row > 0:
            self.window.move(self.window.row - 1, self.window.col)
            self.update()

    def shift_down(self):
        if self.window.row + self.window.nrows < self.parent.nrows:
            self.window.move(self.window.row + 1, self.window.col)
            self.update()

    def shift_left(self):
        if self.window.col > 0:
            self.window.move(self.window.row, self.window.col - 1)
            self.update()

    def shift_right(self):
        if self.window.col + self.window.ncols < self.parent.ncols:
            self.window.move(self.window.row, self.window.col + 1)
            self.update()
