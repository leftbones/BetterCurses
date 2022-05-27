# BetterCurses - widget.py
# github.com/leftbones/bettercurses

class Widget:
    def __init__(
        self,
        row, col,
        nrows, ncols,
    ):
        self.parent = None
        self.row = row
        self.col = col
        self.nrows = nrows
        self.ncols = ncols

    def print(self):
        pass
