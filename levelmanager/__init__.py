

from dungeon import Dungeon_Generator

LEVELS = [
    {
        'id': 1,
        'name': 'Level One',
        'max_room_size': 20,
        'min_room_size': 16,
        'max_rooms': 10,
        'max_room_monsters': 1,
        'num_items': 1
    },
    {
        'id': 2,
        'name': 'Level One',
        'max_room_size': 18,
        'min_room_size': 14,
        'max_rooms': 15,
        'max_room_monsters': 1,
        'num_items': 1
    },
    {
        'id': 3,
        'name': 'Level One',
        'max_room_size': 15,
        'min_room_size': 11,
        'max_rooms': 20,
        'max_room_monsters': 2,
        'num_items': 2
    },
    {
        'id': 4,
        'name': 'Level One',
        'max_room_size': 13,
        'min_room_size': 9,
        'max_rooms': 25,
        'max_room_monsters': 2,
        'num_items': 2
    },
    {
        'id': 5,
        'name': 'Level One',
        'max_room_size': 10,
        'min_room_size': 6,
        'max_rooms': 30,
        'max_room_monsters': 3,
        'num_items': 3
    }
]


class LevelManager:
    def __init__(self):
        self.current_level = 1
        self.game_state = 'active'
        self.player_action = None
        self.dungeon = None

    def setup_level(self):
        level = self._getCurrentLevel()
        new_level = Level(level.get('name'), level.get('max_room_size'), level.get('min_room_size'),
                          level.get('max_rooms'), level.get('max_room_monsters'), level.get('num_items'))
        self.dungeon = Dungeon_Generator(new_level)

    def _getCurrentLevel(self):
        for level in LEVELS:
            if level.get('id') == self.current_level:
                return level


class Level:
    def __init__(self, name, max_room_size, min_room_size, max_rooms, max_room_monsters, num_items):
        self.name = name
        self.player_state = 'playing'
        self.max_room_size = max_room_size  # max number of tiles a room can be
        self.min_room_size = min_room_size  # min number of tiles a room can be
        self.max_rooms = max_rooms  # max number of rooms
        self.max_room_monsters = max_room_monsters  # max number of monsters in a room
        self.num_items = num_items  # number of items in the level
