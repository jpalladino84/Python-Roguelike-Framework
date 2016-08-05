from settings import COLORS

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
    'fgcolor': COLORS['white'],
    'bgcolor': COLORS['black'],
    'character_state': 'alive',
    'character_class': FIGHTER
}

ORC = {
    'name': 'Orc',
    'ascii_char': 'o',
    'fgcolor': COLORS['orc green'],
    'bgcolor': COLORS['black'],
    'character_state': 'alive',
    'character_class': ORC_FIGHTER
}

TROLL = {
    'name': 'Troll',
    'ascii_char': 'T',
    'fgcolor': COLORS['orc green'],
    'bgcolor': COLORS['black'],
    'character_state': 'alive',
    'character_class': TROLL_FIGHTER
}
