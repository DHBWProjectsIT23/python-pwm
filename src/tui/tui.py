def tui_main(stdscr):
    stdscr.clear()

    stdscr.addstr(10, 20, "Hello, World!")

    stdscr.refresh()
    stdscr.getkey()
