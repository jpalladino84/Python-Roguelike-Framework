import enum

import settings
import tdl
from characters import actions
from characters.character import Character
from generators.dungeon_generator import DungeonGenerator
from areas.level import Level
from managers.console_manager import ConsoleManager, CONSOLES
from tdl import map


class GameState(enum):
    PLAYING = 0
    ENDED = 1


class GameManager(object):
    """
    Game Manager: Handles setup and progression of the game

    Admittedly this is a bit of a mess and will need to be cleaned up.
    """
    game_state = GameState.PLAYING

    player_action = None
    dungeon = None
    maze = None
    level = None
    player = None
    monsters = []
    items = []
    show_inventory = False

    colors = settings.DUNGEON_COLORS
    movement_keys = settings.KEY_MAPPINGS
    console_manager = ConsoleManager()

    def __init__(self):
        # Pre-load levels into database
        self.dungeon_generator = DungeonGenerator()

    def show_main_menu(self):
        self.console_manager.render_main_menu()

        key_event = tdl.event.keyWait()
        if key_event.keychar.upper() == 'A':
            self.new_game()
            # TODO Before playing, we need to LOAD game data.
            self.play_game()
        elif key_event.keychar.upper() == 'B':
            # Halt the script using SystemExit
            raise SystemExit('The window has been closed.')

    def new_game(self):
        # TODO This should prepare the first level
        level = Level()
        tdl.setTitle(level.name)
        self.init_dungeon(level)

    def init_dungeon(self, level):
        self.dungeon_generator.generate(level)
        # TODO The player must be built and retrieved here.
        self.player = Character("player", "player", None, None, None, None, None, None, None)
        self.maze = self.dungeon.maze

    def player_wins(self):
        # the game ended
        self.game_state = GameState.ENDED

    def render_gui(self):
        CONSOLES['status'].drawStr(0, 2, "Health: {}\n\n".format(int(self.player.character_class.hp)))
        CONSOLES['status'].drawStr(0, 5, "Attack Power: {}\n\n".format(self.player.character_class.attack))
        CONSOLES['status'].drawStr(0, 8, "Defense: {}\n\n".format(self.player.character_class.defense))
        CONSOLES['status'].drawStr(0, 11, "Speed: {}\n\n".format(self.player.character_class.speed))

        self.console_manager.render_console(CONSOLES['action_log'], 0, 45)
        self.console_manager.render_console(CONSOLES['status'], 41, 45)

    def render_all(self):
        """
        Render the areas, characters, items, etc..
        """
        console = self.console_manager.main_console
        colors = self.colors

        self.render_gui()

        # go through all tiles, and set their background color
        for y in range(self.dungeon.height):
            for x in range(self.dungeon.width):
                tile = self.maze[x][y]
                wall = tile.block_sight
                ground = tile.is_ground

                if tile.is_explored:
                    if wall:
                        console.drawChar(x, y, '#', fgcolor=colors['dark_gray_wall'])
                    elif ground:
                        console.drawChar(x, y, '.', fgcolor=colors['dark_ground'])

        player_x, player_y = self.player.location.coords
        self.player.fov = map.quickFOV(player_x, player_y, self.is_transparent, 'basic')
        for x, y in self.player.fov:
            if self.maze[x][y].is_blocked:
                console.drawChar(x, y, '#', fgcolor=colors['light_wall'])
                self.maze[x][y].is_explored = True
            if self.maze[x][y].is_ground is True:
                console.drawChar(x, y, '.', fgcolor=colors['light_ground'])
                self.maze[x][y].is_explored = True

        # NB: Order in which things are render is important
        # 1. draw items
        # 2. draw monsters
        # 3. draw player

        for item in self.items:
            x, y = item.location.coords
            if (x, y) in self.player.fov:
                console.drawChar(x, y, **item.display.get_draw_info())

        # draw monsters
        for monster in self.monsters:
            x, y = monster.location.coords
            if (x, y) in self.player.fov:
                console.drawChar(x, y, **monster.display.get_draw_info())

        # draw player
        console.drawChar(player_x, player_y, self.player.display.get_draw_info())

    def is_transparent(self, x, y):
        """
        Used by map.quickFOV to determine which tile fall within the players "field of view"
        """
        try:
            # Pass on IndexErrors raised for when a player gets near the edge of the screen
            # and tile within the field of view fall out side the bounds of the maze.
            tile = self.maze[x][y]
            if tile.block_sight and tile.is_blocked:
                return False
            else:
                return True
        except IndexError:
            pass

    def play_game(self):
        """
        The main game loop
        """
        while True:  # Continue in an infinite game loop.
            self.game_state = GameState.PLAYING if not self.player.is_dead() else None
            self.console_manager.main_console.clear()  # Blank the console.
            self.render_all()

            if self.player.is_dead():
                CONSOLES['status'].drawStr(0, 4, 'You have died!')

            # TODO: Fix win condition
            # elif player.character_state == 'done':
            #     STATUS.move(0, 4)
            #     STATUS.printStr('CONGRATULATIONS!\n\nYou have found a Cone of Dunshire!')

            tdl.flush()  # Update the window.
            self.listen_for_events()

    def listen_for_events(self):
        """
        Any keyboard interaction from the user occurs here
        """
        # TODO We need a binding system.
        # TODO Possibly just a dictionary with keyboard input as keys and Action Enum as value
        for event in tdl.event.get():  # Iterate over recent events.
            if event.type == 'KEYDOWN':
                if self.game_state == GameState.PLAYING:

                    # TODO: Fix inventory system
                    # if self.show_inventory:
                    #     if event.keychar in self.player.inventory:
                    #         self.player.heal_damage()
                    #         del self.player.inventory[event.keychar]
                    #     elif event.keychar.upper() == 'I':
                    #         self.show_inventory = False
                    #         tdl.setTitle(self.level.name)

                    # We mix special keys with normal characters so we use keychar.
                    if event.keychar.upper() in self.movement_keys:
                        # Get the vector and unpack it into these two variables.
                        key_x, key_y = self.movement_keys[event.keychar.upper()]
                        # Then we add the vector to the current player position.

                        # player moves or attacks in the specified direction
                        actions.player_move_or_attack(self.player, key_x, key_y, self.maze)

                        # TODO: Fix the stairs
                        # if (self.areas.stairs and
                        #    (self.areas.stairs.x, self.areas.stairs.y) == (self.player.x, self.player.y)):
                        #     self.next_level()

                        # let monsters take their turn
                        if self.game_state == GameState.PLAYING:
                            for monster in self.monsters:
                                actions.monster_take_turn(monster, self.player, self.maze)

                    # TODO: Fix pick up and inventory menu functions
                    # else:
                    #     if event.keychar.upper() == 'G':
                    #         # pick up an items
                    #         for object in self.areas.objects:  # look for an items in the player's tile
                    #             if object.x == self.player.x and object.y == self.player.y and object.items:
                    #                 is_cone = object.items.pickUp(self.areas.objects)
                    #                 if is_cone:
                    #                     self.player_wins()
                    #                 else:  # user picked up a health potion
                    #                     letter_index = ord('a')
                    #
                    #                     while chr(letter_index) in self.player.inventory:
                    #                         letter_index += 1
                    #
                    #                     self.player.inventory[chr(letter_index)] = object
                    #
                    #     elif event.keychar.upper() == 'I':
                    #         if len(self.player.inventory) > 0 and self.show_inventory is False:
                    #             self.show_inventory = True

            if event.type == 'QUIT':
                # Halt the script using SystemExit
                raise SystemExit('The window has been closed.')

    def load_game_data(self):
        """
        This is where the data is loaded.
        """
        # TODO This should load all templates to be instantiated later.

        self.monsters = []
        self.items = []
