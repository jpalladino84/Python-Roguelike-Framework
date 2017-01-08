"""
Console Manager: handles the creation and rendering of all consoles.
"""

import tdl
from tdl import Console


class ConsoleManager:

    def __init__(self):
        self.main_console_w = 80
        self.main_console_h = 60
        tdl.setFont('terminal8x8_gs_ro.png')
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
