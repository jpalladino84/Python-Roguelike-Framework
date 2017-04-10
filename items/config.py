"""
Items

Items created here will show up in the dungeon.

Item Properties:
    level_id -- The level where the item lives
    name -- The name of the item
    desc -- A description of what the item is/does
    stat_mod -- The stat that the item modifies, can be null
    op -- The operation effect the item has on the stat, can be null.
    value -- The amount the stat is raise or lowered by, can be null.

Example
    A simple health potion might recover the players health by 10:

    HEALTH_POTION = {
        'name': 'Health Potion',
        'desc': 'Heals 10 points of damage.',
        'stat_mod': 'hp',
        'op': 'add',
        'value': 10
    }
"""
from util.colors import Colors

# Item Categories
CONSUMABLE = 'CONSUMABLE'
ARTIFACT = 'Artifact'
SCROLL = 'SCROLL'
WEAPON = 'WEAPON'
ARMOR = 'ARMOR'


HEALTH_POTION = {
    'name': 'Health Potion',
    'desc': 'Heals 10 points of damage.',
    'ascii_char': '!',
    'fgcolor': Colors.WHITE_COLOR,
    'bgcolor': Colors.BLACK_COLOR,
    'inventory_list': 'dungeon_list',
    'category': CONSUMABLE,
    'stat_mod': 'hp',
    'op': 'add',
    'value': 10
}

CONE_OF_DUNSHIRE = {
    'name': 'Cone of Dunshire',
    'desc': 'An ancient artifact that once belonged to the Architect, Ben Wyatt.',
    'ascii_char': '!',
    'fgcolor': Colors.BLOOD_RED,
    'bgcolor': Colors.BLACK_COLOR,
    'inventory_list': 'dungeon_list',
    'category': ARTIFACT,
    'stat_mod': None,
    'op': None,
    'value': None
}


ITEMS = [HEALTH_POTION, CONE_OF_DUNSHIRE]
