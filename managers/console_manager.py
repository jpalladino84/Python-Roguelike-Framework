"""
Console Manager: handles the creation and rendering of all consoles.
"""
import textwrap

import tdl
import os
from tdl import Console


class ConsoleManager:

    def __init__(self):
        self.main_console_w = 100
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
    """
    Create console for displaying choices to the player
    """
    MENU_TEMPLATE = "{menu_text}\n\n{options}"

    OPTION_TEMPLATE = "({option_char:}) {option_description}"

    def __init__(self, name, text, options, width, height):
        Console.__init__(self, width, height)
        self.name = name
        self.text = text
        self.options = options
        self.max_options_len = 26
        self.letter_index = ord('a')

    def create_menu(self, pos_x, pos_y):
        self.move(pos_x, pos_y)
        self.printStr(self.MENU_TEMPLATE.format(
            menu_text=self.text,
            options=self._build_options()
        ))

    def _build_options(self):
        option_msg = []
        for option_text in self.options:
            option = self.OPTION_TEMPLATE.format(
                option_char=chr(self.letter_index),
                option_description=option_text
            )
            option_msg.append(option)
            self.letter_index += 1
        return textwrap.indent("\n\n".join(option_msg), "             ")  # TODO: this could be nicer...

    def print_str(self, text, pos_x, pos_y):
        self.move(pos_x, pos_y)
        self.printStr(text)
