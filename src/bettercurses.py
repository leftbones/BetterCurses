# BetterCurses - bettercurses.py
# github.com/leftbones/bettercurses

# Right now this file is used almost entirely for testing, the meat and potatoes are in the other files

import curses

from terminal import Terminal
from enums import Border

from widgets.gutter import Gutter


def main(stdscr):
    terminal = Terminal(stdscr)
    term_h, term_w = terminal.get_size()

    editor = terminal.new_window(
        0, 0, term_h, term_w,
        title = "Editor"
    )

    terminal.add_window(editor)

#    gutter = Gutter(
#        parent = editor,
#        row = 0,
#        col = 1,
#        nrows = term_h,
#        ncols = 5,
#        offset = 5
#    )
#    editor.add_widget(gutter)

    while True:
        terminal.update()
        key = terminal.stdscr.getkey()

        if key == 'h': terminal.cursor.move_left()
        elif key == 'j': terminal.cursor.move_down()
        elif key == 'k': terminal.cursor.move_up()
        elif key == 'l': terminal.cursor.move_right()
        elif key == 'H': terminal.cursor.shift_left()
        elif key == 'J': terminal.cursor.shift_down()
        elif key == 'K': terminal.cursor.shift_up()
        elif key == 'L': terminal.cursor.shift_right()
        elif key == '\t': terminal.focus_next_window()


if __name__ == '__main__':
    curses.wrapper(main)
