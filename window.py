# BetterCurses - window.py
# github.com/leftbones/bettercurses

import curses

from enums import Border

class Window:
    """
    Visual representation of a standard curses window
    Acts as a container for widgets and can be focused by the cursor
    """
    def __init__(
            self,
            parent,
            screen,
            wid,
            row, col,
            nrows, ncols,
            title,
            border,
            margins,
            vscrolloffset,
            hscrolloffset,
        ):
        self.parent = parent
        self.screen = screen
        self.wid = wid
        self.row = row
        self.col = col
        self.nrows = nrows
        self.ncols = ncols
        self.title = title
        self.border = border
        self.margins = margins

        # Cursor Memory
        self.cursor_row = 0
        self.cursor_col = 0

        # Configs
        self.vscrolloffset = vscrolloffset
        self.hscrolloffset = hscrolloffset

        self.row_offset = 0
        self.col_offset = 0

        # Margins
        self.edge_upper = 0 + self.margins[0]
        self.edge_lower = 1 + self.margins[1]
        self.edge_left = 0 + self.margins[2]
        self.edge_right = 1 + self.margins[3]

        if self.border:
            self.edge_upper += 1
            self.edge_lower += 2
            self.edge_left += 1
            self.edge_right += 2

        # Widgets
        self.widgets = []

        # Attributes
        self.attrs = ()

        # Experimental
        self.dimmed = False
        self.corner_style = Border.Square

    @property
    def bottom(self):
        return self.row_offset + (self.nrows - self.edge_lower)

    @property
    def right(self):
        return (self.col_offset + self.ncols) - self.edge_left

    def add_widget(self, widget):
        """
        Add a widget to the window
        """
        widget.parent = self
        self.widgets.append(widget)

    def resize(self, nrows, ncols):
        """
        Resize the window
        """
        self.nrows = nrows
        self.ncols = ncols
        self.screen.resize(nrows, ncols)

    def move(self, row, col):
        """
        Move the window to a new location
        """
        self.row = row
        self.col = col
        self.screen.mvderwin(row, col)

    def add_attr(self, attr):
        """
        Add an attribute to the list of active attributes
        """
        attrs = list(self.attrs)
        try: attrs.append(attr)
        except: pass
        self.attrs = tuple(attrs)

    def del_attr(self, attr):
        """
        Remove an attribute from the list of active attributes
        """
        attrs = list(self.attrs)
        try: attrs.remove(attr)
        except: pass
        self.attrs = tuple(attrs)

    def print(self):
        """
        Print the contents of the window to the terminal's screen
        """
        # Attributes
        if self.dimmed and curses.A_DIM not in self.attrs: self.add_attr(curses.A_DIM)
        elif not self.dimmed and curses.A_DIM in self.attrs: self.del_attr(curses.A_DIM)

        # Background
        self.screen.bkgd(' ', *self.attrs);
        for row in range(self.nrows):
            for col in range(self.ncols):
                self.screen.delch(row, col)
                self.screen.insch(row, col, ' ', *self.attrs)

        # Border
        if self.border:
            self.screen.box()
            self.screen.delch(0, 0)
            self.screen.delch(0, self.ncols - 1)
            self.screen.delch(self.nrows - 1, 0)
            self.screen.delch(self.nrows - 1, self.ncols - 1)
            self.screen.insstr(0, 0, self.corner_style[0], *self.attrs)
            self.screen.insstr(0, self.ncols - 1, self.corner_style[1], *self.attrs)
            self.screen.insstr(self.nrows - 1, 0, self.corner_style[2], *self.attrs)
            self.screen.insstr(self.nrows - 1, self.ncols - 1, self.corner_style[3], *self.attrs)

            # Title (requires border)
            if self.title:
                self.screen.addstr(0, 1, f" {self.title} ", *self.attrs)

    def translate_pos(self, cursor):
        """
        Translate the cursor's screen position into the cursor's window position (relative to the window's origin)
        """
        return (
            self.row + (cursor.row - self.row_offset) + self.edge_upper,
            self.col + (cursor.col - self.col_offset) + self.edge_left
        )

    def scroll(self, cursor):
        """
        Scroll the contents of the window horizontally or vertically if the cursor is outside of the allowed boundaries
        Boundaries are determined by the actual size of the window as well as vscrolloffset and hscrolloffset
        """
        #while cursor.row <= (self.row_offset + self.vscrolloffset) - 1 and self.row_offset > 0: self.row_offset -= 1
        #while cursor.row >= (self.bottom - self.vscrolloffset) + 1 and self.bottom < len(self.contents) + self.edge_lower: self.row_offset += 1

        #while cursor.col <= (self.col_offset + self.hscrolloffset) - 1 and self.col_offset > 0: self.col_offset -= 1
        #while cursor.col >= (self.right - self.hscrolloffset) - 1: self.col_offset += 1
