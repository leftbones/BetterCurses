# BetterCurses - bettercurses.py
# github.com/leftbones/bettercurses

import curses

from terminal import Terminal
from enums import Border


# Testing
def main(stdscr):
    terminal = Terminal(stdscr)
    term_h, term_w = terminal.get_size()

    editor = terminal.new_window(
        0, 0, term_h, term_w,
        title = "Editor"
    )

    terminal.add_window(editor)

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
