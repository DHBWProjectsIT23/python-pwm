import sys
import os
import unittest
import curses

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from src.tui.window import Window


class TestWindow(unittest.TestCase):
    def test_init(self):
        stdscr = curses.initscr()
        self.window = Window(stdscr)
        curses.endwin()

    def test_size(self):
        window = get_window()
        height_1, width_1 = window().getmaxyx()
        height_2, width_2 = window.getSize()
        self.assertEqual(height_1, height_2)
        self.assertEqual(width_1, width_2)
        curses.endwin()


def get_window():
    stdscr = curses.initscr()
    return Window(stdscr)
