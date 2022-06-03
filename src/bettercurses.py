# BetterCurses - bettercurses.py
# github.com/leftbones/bettercurses

# Right now this file is used almost entirely for testing, the meat and potatoes are in the other files

import curses

from terminal import Terminal
from enums import Border

from widgets.tabwidget import TabWidget
from widgets.editorwidget import EditorWidget


def main(stdscr):
    with open('bettercurses.py') as f:
        lines = f.readlines();

    terminal = Terminal(stdscr)
    term_h, term_w = terminal.get_size()

    container = terminal.new_window(0, 0, term_h, term_w)
    window = terminal.new_window(0, 0, term_h, term_w)

    tabwidget = TabWidget(
        parent = container,
        row = 0,
        col = 0,
        nrows = 0,
        ncols = term_w,
    )

    editor = EditorWidget(
        parent = window,
        row = 0,
        col = 0,
        nrows = term_h,
        ncols = term_w,
        contents = lines,
        offset = 6
    )

    container.add_widget(tabwidget)
    window.add_widget(editor)

    tabwidget.add_tab(window)

    terminal.add_window(container)

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
        elif key == '\t': tabwidget.next_tab()

        elif key == '1': tabwidget.goto_tab(1)
        elif key == '2': tabwidget.goto_tab(2)
        elif key == '3': tabwidget.goto_tab(3)
        elif key == '4': tabwidget.goto_tab(4)


if __name__ == '__main__':
    curses.wrapper(main)
