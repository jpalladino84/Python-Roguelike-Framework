"""
Level config

Define your levels here.

Level:
    id -- The level id
    name -- Name of the level
    desc -- A flavor description for the level
    max_room_size -- Tells the generator the max size a room can be
    min_room_size -- Tells the generator the min size a room can be
    max_rooms -- Tells the generator the max number rooms for that level
    is_final_level -- A flag to determine if the level is the last
    items -- A list of items you want to appear on that level. Duplicates are allowed
             if you want to see an item appear more than once.

Example:
    {
        'id': 1,
        'name': 'Level One',
        'desc': None,
        'max_room_size': 14,
        'min_room_size': 10,
        'max_rooms': 10,
        'is_final_level': False,
        'items': [
            HEALTH_POTION,
            HEALTH_POTION
        ]
    }
"""

from item.config import HEALTH_POTION, CONE_OF_DUNSHIRE
from character.config import ORC, TROLL


LEVELS = [
    {
        'id': 1,
        'name': 'Level One',
        'desc': None,
        'max_room_size': 14,
        'min_room_size': 10,
        'max_rooms': 10,
        'max_num_items': 1,
        'is_final_level': False,
        'items': [HEALTH_POTION],
        'monsters': [
            ORC,
            ORC,
            TROLL
        ]
    },
    {
        'id': 2,
        'name': 'Level Two',
        'desc': None,
        'max_room_size': 13,
        'min_room_size': 9,
        'max_rooms': 15,
        'is_final_level': False,
        'items': [
            HEALTH_POTION
        ],
        'monsters': []
    },
    {
        'id': 3,
        'name': 'Level Three',
        'desc': None,
        'max_room_size': 12,
        'min_room_size': 8,
        'max_rooms': 20,
        'is_final_level': False,
        'items': [
            HEALTH_POTION
        ],
        'monsters': []
    },
    {
        'id': 4,
        'name': 'Level Four',
        'desc': None,
        'max_room_size': 11,
        'min_room_size': 7,
        'max_rooms': 25,
        'is_final_level': False,
        'items': [
            HEALTH_POTION,
            HEALTH_POTION
        ],
        'monsters': []
    },
    {
        'id': 5,
        'name': 'Level Five',
        'desc': None,
        'max_room_size': 10,
        'min_room_size': 6,
        'max_rooms': 30,
        'is_final_level': True,
        'items': [
            HEALTH_POTION,
            CONE_OF_DUNSHIRE
        ],
        'monsters': []
    }
]
