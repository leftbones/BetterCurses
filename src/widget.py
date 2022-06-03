# BetterCurses - widget.py
# github.com/leftbones/bettercurses

class Widget:
    """
    Base class for all widgets to inherit
    """
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
        try: self.parent.screen.insstr(self.row, self.col, 'This widget has no print method!')
        except: pass
