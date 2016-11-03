"""
Character Config

This is where you will create all your characters, and their classes, to place in your dungeon.

Character: The main actor in the dungeon.
    - name: Character name
    - ascii_char: The ascii character that will represent your character in the dungeon
    - fgcolor: The color of your ascii character
            (See setting.py see a list of all colors or add one)
    - bgcolor: The background color of your ascii character
            (See setting.py see a list of all colors or add one)
    - character_state: Typically 'alive'.
    - character_class: The class you would like your character to have.

Example:
    The main actor which the user will control

    PLAYER = {
        'name': 'player',
        'ascii_char': '@',
        'fgcolor': COLORS['white'],
        'bgcolor': COLORS['black'],
        'character_state': 'alive',
        'character_class': FIGHTER
    }

CharacterClass: Defines the Characters attributes such has health, defence, speed, etc...
    - name: Name of the class
    - max_hp: The upper limit on how much health the character has
    - hp: The current amount of health the character has
    - defence: How resilient the character is
    - attack: How powerful the character is
    - speed: How quick the character is (doesn't really have any effect right now)

Example:
    The fighter class, has strong attacks, high health, and has some resilience against enemy attacks

    FIGHTER = {
        'name': 'Fighter',
        'max_hp': 30,
        'hp': 30,
        'defense': 2,
        'attack': 5,
        'speed': 3
    }
"""

from settings import Colors

FIGHTER = {
    'name': 'Fighter',
    'max_hp': 30,
    'hp': 30,
    'defense': 2,
    'attack': 5,
    'speed': 3
}

ORC_FIGHTER = {
    'name': 'Orc Fighter',
    'max_hp': 10,
    'hp': 10,
    'defense': 0,
    'attack': 3,
    'speed': 2
}

TROLL_FIGHTER = {
    'name': 'Troll Fighter',
    'max_hp': 16,
    'hp': 16,
    'defense': 1,
    'attack': 4,
    'speed': 1
}

PLAYER = {
    'name': 'player',
    'ascii_char': '@',
    'fgcolor': Colors.WHITE_COLOR,
    'bgcolor': Colors.BLACK_COLOR,
    'character_state': 'alive',
    'character_class': FIGHTER
}

ORC = {
    'name': 'Orc',
    'ascii_char': 'o',
    'fgcolor': Colors.ORC_GREEN,
    'bgcolor': Colors.BLACK_COLOR,
    'character_state': 'alive',
    'character_class': ORC_FIGHTER
}

TROLL = {
    'name': 'Troll',
    'ascii_char': 'T',
    'fgcolor': Colors.ORC_GREEN,
    'bgcolor': Colors.BLACK_COLOR,
    'character_state': 'alive',
    'character_class': TROLL_FIGHTER
}
