"""
Game Manager: Handles setup and progression of the game
"""

import tdl
from tdl import map

from dungeon import Dungeon_Generator
from managers.console_manager import ConsoleManager
from classes.characters import Fighter, Player

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


class GameManager:
    def __init__(self):
        self.current_level = 0
        self.player_state = 'playing'
        self.player_action = None
        self.dungeon = None
        self.level = None
        self.player = None
        self.show_inventory = False

        self.colors = {
            'dark_blue_wall': (0, 0, 100),
            'dark_gray_wall': (75, 75, 75),
            'light_wall': (130, 110, 50),
            'dark_ground': (75, 75, 75),
            'light_ground': (160, 144, 40),
        }

        # Create a dictionary that maps keys to vectors.
        # Names of the available keys can be found in the online documentation:
        # http://packages.python.org/tdl/tdl.event-module.html
        self.movement_keys = {
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

        self.console_manager = ConsoleManager()
        self._create_new_player()

    def show_main_menu(self):

        self.console_manager.render_main_menu()

        key_event = tdl.event.keyWait()

        if key_event.keychar.upper() == 'A':
            self.new_game()
            self.play_game()
        elif key_event.keychar.upper() == 'B':
            # Halt the script using SystemExit
            raise SystemExit('The window has been closed.')

    def new_game(self):
        self.next_level()
        self.create_gui()

    def next_level(self):
        self.create_new_level()
        tdl.setTitle(self.level.name)

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
        fighter_component = Fighter(hp=30, defense=2, power=5, speed=3, death_function=self.player_death)
        self.player = Player(0, 0, '@', 'Hero', blocks=True, fighter=fighter_component)

    def player_death(self, player):
        #the game ended!
        print 'You died!'
        self.player_state = 'dead'

        # for added effect, transform the player into a corpse!
        self.player.char = '%'
        self.player.fgcolor = (255, 50, 50)

    def player_wins(self, player):
        # the game ended
        self.player_state = 'done'

    def isTransparent(self, x, y):

        try:
            if self.dungeon.map[x][y].block_sight and self.dungeon.map[x][y].blocked:
                return False
            else:
                return True
        except IndexError:
            pass

    def create_gui(self):
        self.console_manager.create_new_console('status_sheet', 40, 15)
        self.console_manager.create_new_console('action_log', 40, 15)

    def render_gui(self):
        plHealth = self.player.name + " Health: " + str("%02d" % self.player.fighter.hp)
        self.console_manager.consoles['status_sheet'].drawStr(0, 2, plHealth)

        self.console_manager.render_console(self.console_manager.consoles['action_log'], 0, 45)
        self.console_manager.render_console(self.console_manager.consoles['status_sheet'], 41, 45)

    def render_all(self):

        console = self.console_manager.main_console
        dungeon = self.dungeon
        player = self.player
        colors = self.colors

        self.render_gui()

        #go through all tiles, and set their background color
        for y in range(dungeon.height):
            for x in range(dungeon.width):
                wall = dungeon.map[x][y].block_sight
                ground = dungeon.map[x][y].ground
                if dungeon.map[x][y].explored:
                    if wall:
                        console.drawChar(x, y, '#', fgcolor=colors['dark_gray_wall'])
                    elif ground:
                        console.drawChar(x, y, '.', fgcolor=colors['dark_ground'])

        player.fov_coords = map.quickFOV(player.x, player.y, self.isTransparent, 'basic')

        for x, y in player.fov_coords:
            if dungeon.map[x][y].blocked is not False:
                console.drawChar(x, y, '#', fgcolor=colors['light_wall'])

                dungeon.map[x][y].explored = True
            if dungeon.map[x][y].ground is True:
                console.drawChar(x, y, '.', fgcolor=colors['light_ground'])
                dungeon.map[x][y].explored = True

        #draw all objects in the list
        for object in dungeon.objects:
            if (object.x, object.y) in player.fov_coords:
                console.drawChar(object.x, object.y, object.char, fgcolor=object.fgcolor, bgcolor=object.bgcolor)

            if self.show_inventory:
                self.console_manager.render_inventory_menu(self.player.inventory)

    def play_game(self):

        while True:  # Continue in an infinite game loop.

            self.console_manager.main_console.clear()  # Blank the console.

            self.render_all()

            if self.player_state == 'dead':
                self.console_manager.consoles['status_sheet'].drawStr(0, 4, 'You have died!')
            elif self.player_state == 'done':
                # pdb.set_trace()
                self.console_manager.consoles['status_sheet'].move(0, 4)
                self.console_manager.consoles['status_sheet'].printStr('CONGRADULATIONS!\n\nYou have found a Cone of Dunshire!')

            tdl.flush()  # Update the window.
            self.listen_for_events()

    def listen_for_events(self):
        action_log = self.console_manager.consoles['action_log']

        for event in tdl.event.get():  # Iterate over recent events.
            if event.type == 'KEYDOWN':
                if self.player_state == 'playing':
                    if self.show_inventory:
                        if event.keychar in self.player.inventory:
                            self.player.heal_damage()
                            del self.player.inventory[event.keychar]
                        elif event.keychar.upper() == 'I':
                            self.show_inventory = False
                            tdl.setTitle(self.level.name)

                    # We mix special keys with normal characters so we use keychar.
                    elif event.keychar.upper() in self.movement_keys:
                        # Get the vector and unpack it into these two variables.
                        keyX, keyY = self.movement_keys[event.keychar.upper()]
                        # Then we add the vector to the current player position.

                        self.player.move_or_attack(keyX, keyY, self.dungeon, action_log)

                        if (self.dungeon.stairs and
                           (self.dungeon.stairs.x, self.dungeon.stairs.y) == (self.player.x, self.player.y)):
                            self.next_level()

                        #let monsters take their turn
                        if self.player_state == 'playing':
                            for object in self.dungeon.objects:
                                if object.ai:
                                    object.ai.take_turn(self.dungeon, action_log)

                    else:
                        if event.keychar.upper() == 'G':
                            #pick up an item
                            for object in self.dungeon.objects:  # look for an item in the player's tile
                                if object.x == self.player.x and object.y == self.player.y and object.item:
                                    is_cone = object.item.pickUp(self.dungeon.objects,
                                                                 action_log)
                                    if is_cone:
                                        self.player_wins(self.player)
                                    else:  # user picked up a health potion
                                        letter_index = ord('a')

                                        while chr(letter_index) in self.player.inventory:
                                            letter_index += 1

                                        self.player.inventory[chr(letter_index)] = object

                        elif event.keychar.upper() == 'I':
                            if len(self.player.inventory) > 0 and self.show_inventory is False:
                                self.show_inventory = True

            if event.type == 'QUIT':
                # Halt the script using SystemExit
                raise SystemExit('The window has been closed.')


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
