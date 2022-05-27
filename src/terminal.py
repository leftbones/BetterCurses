# BetterCurses - terminal.py
# github.com/leftbones/bettercurses

import curses

from cursor import Cursor
from window import Window


class Terminal():
    """
    Technically this is the default window returned by curses.initscr()
    Acts as a container for all other windows
    """

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.cursor = Cursor(self)
        self.nrows, self.ncols = self.get_size()

        self.windows = []

        # Configs
        self.dim_inactive = True

    def update(self):
        """
        Update all windows contained in the terminal
        """  
        self.stdscr.erase()
        self.stdscr.move(0, 0)

        for window in self.windows:
            if window != self.active_window:
                if self.dim_inactive: window.dimmed = True
                window.print()

        self.active_window.dimmed = False
        self.active_window.print()

        self.stdscr.move(*self.cursor.window.translate_pos(self.cursor))

    def new_window(
            self,
            row, col, # Required
            nrows, ncols, # Required
            title = None,
            border = True,
            margins = [0, 0, 1, 2],
            vscrolloffset = 5,
            hscrolloffset = 10,
        ):

        """
        Create and return a new window
        """

        window = Window(
            self,
            screen = self.stdscr.derwin(nrows, ncols, row, col),
            wid = len(self.windows) + 1,
            row = row,
            col = col,
            nrows = nrows,
            ncols = ncols,
            title = title,
            border = border,
            margins = margins,
            vscrolloffset = vscrolloffset,
            hscrolloffset = hscrolloffset,
        )

        return window

    def add_window(self, window):
        """
        Add a window to the terminal
        """
        self.windows.append(window)

        if not self.cursor.window:
            self.focus_window(window)

    def focus_window(self, window):
        """
        Move cursor focus to a particular window and set that window as active so it's printed on top of other windows
        """
        self.active_window = window
        self.cursor.move_window(self.active_window)

    def focus_next_window(self):
        """
        Cycle the windows in the list and set the cursor's focus to the new top window
        """
        try: 
            self.windows.append(self.windows.pop(0))
            self.active_window = self.windows[0]
        except IndexError:
            self.active_window = self.windows[0]
        self.cursor.move_window(self.active_window)

    def get_size(self):
        """
        Return a tuple containing the terminal window size in characters
        """
        return self.stdscr.getmaxyx()
