

from dungeon import Dungeon_Generator
from characters import Fighter, Player

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


class LevelManager:
    def __init__(self):
        self.current_level = 0
        self.player_state = 'playing'
        self.player_action = None
        self.dungeon = None
        self.level = None
        self.player = None

        self._create_new_player()

    def create_new_level(self):

        self.current_level += 1
        level_config = self._getCurrentLevel()
        new_level = Level(level_config.get('name'),
                          level_config.get('max_room_size'),
                          level_config.get('min_room_size'),
                          level_config.get('max_rooms'),
                          level_config.get('max_room_monsters'),
                          level_config.get('num_items'),
                          level_config.get('id'))

        new_level.player = self.player
        self.dungeon = Dungeon_Generator(new_level)
        self.level = new_level

    def _getCurrentLevel(self):
        for lvl_config in LEVELS:
            if lvl_config.get('id') == self.current_level:
                return lvl_config

    def _create_new_player(self):
        # create player and place him in the room
        # this is the first room, where the player starts at
        fighter_component = Fighter(hp=30, defense=2, power=5, death_function=self.player_death)
        self.player = Player(0, 0, '@', 'Hero', True, fighter=fighter_component)

    def player_death(self, player):
        #the game ended!
        print 'You died!'
        self.player_state = 'dead'

        # for added effect, transform the player into a corpse!
        self.player.char = '%'

    def player_wins(self, player):
        # the game ended
        self.player_state = 'done'


class Level:
    def __init__(self, name, max_room_size, min_room_size, max_rooms, max_room_monsters, num_items, level_id):
        self.id = level_id
        self.name = name
        self.max_room_size = max_room_size  # max number of tiles a room can be
        self.min_room_size = min_room_size  # min number of tiles a room can be
        self.max_rooms = max_rooms  # max number of rooms
        self.max_room_monsters = max_room_monsters  # max number of monsters in a room
        self.num_items = num_items  # number of items in the level
        self.player = None
