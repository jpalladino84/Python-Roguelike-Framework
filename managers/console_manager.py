"""
Console Manager: handles the creation and rendering of all consoles.
"""

import tdl
import os
from tdl import Console


class ConsoleManager:

    def __init__(self):
        self.main_console_w = 80
        self.main_console_h = 60
        font_path = os.path.normpath(os.path.join(os.path.realpath(__file__), "..", "..", "terminal8x8_gs_ro.png"))
        tdl.setFont(font_path)
        self.main_console = tdl.init(self.main_console_w, self.main_console_h, 'Roguelike Game')

    def render_console(self, console, pos_x, pos_y):
        self.main_console.blit(console, pos_x, pos_y)

    def clear(self):
        self.main_console.clear()

    @staticmethod
    def create_new_console(width, height, mode='scroll'):
        console = tdl.Console(width, height)
        console.setMode(mode)
        return console

    def _close_font(self):
        """
        Close font resource for unittests.
        """
        tdl.file.close()


class Menu(Console):
    def __init__(self, name, options, width, height):
        Console.__init__(self, width, height)
        self.name = name
        self.max_options_len = 26
        self.options = options
        self.letter_index = ord('a')

    def print_str(self, text, pos_x, pos_y):
        self.move(pos_x, pos_y)
        self.printStr(text)
