
DUNGEON_COLORS = {
    'dark_blue_wall': (0, 0, 100),
    'dark_gray_wall': (75, 75, 75),
    'light_wall': (130, 110, 50),
    'dark_ground': (75, 75, 75),
    'light_ground': (160, 144, 40),
}


# Create a dictionary that maps keys to vectors.
# Names of the available keys can be found in the online documentation:
# http://packages.python.org/tdl/tdl.event-module.html
KEY_MAPPINGS = {

    # standard arrow keys
    'UP': [0, -1],
    'DOWN': [0, 1],
    'LEFT': [-1, 0],
    'RIGHT': [1, 0],

    # diagonal keys
    # keep in mind that the keypad won't use these keys even if
    # num-lock is off
    'HOME': [-1, -1],
    'PAGEUP': [1, -1],
    'PAGEDOWN': [1, 1],
    'END': [-1, 1],

    # number-pad keys
    # These keys will always show as KPx regardless if num-lock
    # is on or off.  Keep in mind that some keyboards and laptops
    # may be missing a keypad entirely.
    # 7 8 9
    # 4   6
    # 1 2 3
    'KP1': [-1, 1],
    'KP2': [0, 1],
    'KP3': [1, 1],
    'KP4': [-1, 0],
    'KP6': [1, 0],
    'KP7': [-1, -1],
    'KP8': [0, -1],
    'KP9': [1, -1],
}

LEVELS = [
    {
        'id': 1,
        'name': 'Level One',
        'max_room_size': 14,
        'min_room_size': 10,
        'max_rooms': 10,
        'max_room_monsters': 1,
        'num_items': 0
    },
    {
        'id': 2,
        'name': 'Level Two',
        'max_room_size': 13,
        'min_room_size': 9,
        'max_rooms': 15,
        'max_room_monsters': 1,
        'num_items': 1
    },
    {
        'id': 3,
        'name': 'Level Three',
        'max_room_size': 12,
        'min_room_size': 8,
        'max_rooms': 20,
        'max_room_monsters': 2,
        'num_items': 2
    },
    {
        'id': 4,
        'name': 'Level Four',
        'max_room_size': 11,
        'min_room_size': 7,
        'max_rooms': 25,
        'max_room_monsters': 2,
        'num_items': 2
    },
    {
        'id': 5,
        'name': 'Level Five',
        'max_room_size': 10,
        'min_room_size': 6,
        'max_rooms': 30,
        'max_room_monsters': 3,
        'num_items': 3
    }
]
