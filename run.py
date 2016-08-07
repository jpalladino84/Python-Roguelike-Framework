#!/usr/bin/env python
"""
The main entry point for the game
"""

from managers.game_manager import GameManager
from load import load_game

if __name__ == '__main__':
    load_game()
    game_manager = GameManager()
    game_manager.show_main_menu()
