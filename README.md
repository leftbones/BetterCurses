# BetterCurses

This is a simple wrapper around curses to make it widget-based and more user-friendly in general. Right now, this is being developed specifically for use in my other project, [Ink](https://github.com/leftbones/ink). However, it could easily be applied to other projects as well, and I may continue to expand it past Ink.

This project is still under breaking changes, but here is a basic usage example.

This example code creates an empty window in the center of the terminal screen approximately 1/4th the size of the window. `hjkl` moves the cursor inside the window, and `HJKL` moves the window around the screen. If you were to add a second window, `Tab` would move the cursor's focus between the windows. With more than two windows, it cycles through the windows in order of creation.

``````
import curses
from bettercurses.terminal import Terminal

def main(stdscr):
    # Create a Terminal instance
    terminal = Terminal(stdscr)
    term_h, term_w = terminal.get_size()

    # Create a new window
    editor = terminal.new_window(
        term_h//2, term_w//2, # Position
        term_h//2, term_w//2, # Size
        title = "Window"
    )

    # Add the window to the Terminal
    terminal.add_window(editor)

    while True:
        terminal.update()
        key = terminal.stdscr.getkey()

        # hjkl moves the cursor, HJKL moves the window
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
``````
