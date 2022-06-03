# BetterCurses - tabwidget.py
# github.com/leftbones/bettercurses

import curses


class TabWidget:
    """
    A window with tabs that can be focused individually
    Each tab can contain other windows
    """
    def __init__(
        self,
        parent,
        row, col,
        nrows, ncols,
    ):
        self.parent = parent
        self.row = row
        self.col = col
        self.nrows = nrows
        self.ncols = ncols
        self.borders = True
        self.active_tab = 0
        self.tabs = []

    def print(self):
        tab_pos = 2
        for num, tab in enumerate(self.tabs):
            if num == self.active_tab: self.parent.screen.insstr(self.row, tab_pos, f" {num + 1} {tab[0]} ")
            else: self.parent.screen.insstr(self.row, tab_pos, f" {num + 1} {tab[0]} ", curses.A_DIM)
            tab_pos += 6 + len(tab[0])

        self.tabs[self.active_tab][1].print()

    def add_tab(self, window):
        self.tabs.append([window.title, window])

    def goto_tab(self, tab):
        if tab - 1 < len(self.tabs):
            self.active_tab = tab - 1

    def next_tab(self):
        if self.active_tab < len(self.tabs) - 1: self.active_tab += 1;
        else: self.active_tab = 0;
