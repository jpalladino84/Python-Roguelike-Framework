"""
Loads data from config files into the database
This needs to happen before the game fully loads.
"""
import json
from areas.config import LEVELS
from characters.config import PLAYER


# TODO as a game gets bigger this could take longer... Should maybe insert a loading screen.
def load_game():
    load_levels()
    load_player()


def load_levels():
    pass


def load_monsters(level_config):
    pass


def load_player():
    pass
