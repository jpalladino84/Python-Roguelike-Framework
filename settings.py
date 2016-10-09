
DEVELOPMENT = True

DATABASE_NAME = 'roguelike.db'


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








class Colors:
    BLACK_COLOR = (0, 0, 0)
    WHITE_COLOR = (255, 255, 255)
    DARK_BLUE = (0, 0, 100)
    DARK_GRAY = (75, 75, 75)
    TROLL_GREEN = (100, 180, 150)
    ORC_GREEN = (150, 250, 230)
    BLOOD_RED = (255, 50, 50)


