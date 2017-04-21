import logging
import random
from enum import Enum

import tdl

import settings
from areas.level import Level
from base.scene import BaseScene
from stats.enums import StatsEnum
from managers.action_manager import ActionManager
from generators.dungeon_generator import DungeonGenerator
from managers.echo import EchoService
from settings import DUNGEON_COLORS as COLORS
from data.python_templates.characters import character_templates
from data.python_templates.items import item_templates

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class GameConsoles(Enum):
    ActionLog = 0
    Status = 1


class GameScene(BaseScene):
    """
    This handles everything relating to the UI in the game window.
    """
    ID = "Game"

    def __init__(self, console_manager, scene_manager, game_context):
        super().__init__(console_manager, scene_manager, game_context)
        # TODO Eventually we will want to map more than just movement keys
        self.loaded_levels = []
        self.movement_keys = settings.KEY_MAPPINGS
        self.consoles = {
            GameConsoles.ActionLog: self.console_manager.create_new_console(80, 15),
            GameConsoles.Status: self.console_manager.create_new_console(20, 15)
        }
        self.action_manager = ActionManager(self.consoles[GameConsoles.ActionLog])
        self.echo_service = EchoService(self.consoles[GameConsoles.ActionLog], game_context)

        game_context.echo_service = self.echo_service
        logger.info("Initialized GameScene")
        logger.info("Starting new game.")
        self.new_game()

    def render(self, **kwargs):
        """
        Render the areas, characters, items, etc..
        """
        if "player" not in kwargs:
            logger.error("Render: Player was not given in kwargs.")
            return

        player = kwargs["player"]
        current_level = player.location.level
        self.render_gui(player)
        self.set_tiles_background_color(current_level)

        player_x = player.location.local_x
        player_y = player.location.local_y

        def is_transparent_callback(x, y):
            if x <= 0 or y <= 0:
                return False
            return self.is_transparent(current_level, x, y)

        player.fov = tdl.map.quickFOV(player_x, player_y, is_transparent_callback, 'basic')
        # NB: Order in which things are render is important
        self.render_map(current_level, player.fov)
        self.render_items(player, current_level)
        self.render_characters(player, current_level)
        self.render_player(player)
        if player.is_dead():
            self.consoles[GameConsoles.Status].drawStr(0, 4, 'You have died!')

    def handle_input(self, **kwargs):
        """
        Any keyboard interaction from the user occurs here
        """
        if "player" not in kwargs:
            logger.error("Handle Input: Player was not given in kwargs.")
            return

        player = kwargs["player"]
        current_level = player.location.level
        moved = False

        key_events = kwargs["key_events"]
        for key_event in key_events:
            if key_event.type == 'KEYDOWN':
                # TODO Make Inventory System, Switch to Inventory Scene
                # TODO Make stairs system to go up or down
                # TODO Add Action to pick up items

                # We mix special keys with normal characters so we use keychar.
                if not player.is_dead():
                    if key_event.key == 'KP5' or key_event.key == '.':
                        moved = True

                    if key_event.keychar.upper() in self.movement_keys:
                        key_x, key_y = self.movement_keys[key_event.keychar.upper()]
                        self.action_manager.move_or_attack(player, key_x, key_y)
                        moved = True

                    if key_event.keychar == "i":
                        self.scene_manager.enter_inventory_screen(**kwargs)

                    if moved:
                        for monster in current_level.spawned_monsters:
                            self.action_manager.monster_take_turn(monster, player)
                        moved = False

    def new_game(self):
        # TODO This should prepare the first level
        level = Level()
        level.name = "DEFAULT"
        level.min_room_size = 1
        level.max_room_size = 10
        level.max_rooms = 10
        level.width = 80
        level.height = 45
        self.init_dungeon(level)

    def init_dungeon(self, level):
        # TODO The player must be built and retrieved here.
        dungeon_generator = DungeonGenerator(self.game_context.factory_service)
        player = self.game_context.player
        player.is_player = True
        dungeon_generator.generate(level)
        self.place_dungeon_objects(level, player)

    def place_dungeon_objects(self, level, player):
        character_factory = self.game_context.character_factory
        item_factory = self.game_context.item_factory
        level.monster_spawn_list = [character_factory.build(uid) for uid, monster in character_templates.items()]
        level.item_spawn_list = [item_factory.build(uid) for uid, item in item_templates.items()]

        forerunner = Forerunner(level, player)
        forerunner.run()

    def render_gui(self, player):
        status_console = self.consoles[GameConsoles.Status]
        status_console.drawStr(0, 2, "Health: {}\n\n".format(int(player.stats.get_current_value(StatsEnum.Health))))
        status_console.drawStr(0, 5, "Attack Power: {}\n\n".format(player.get_attack_modifier()))
        status_console.drawStr(0, 8, "Defense: {}\n\n".format(player.get_armor_class()))
        status_console.drawStr(0, 11, "Speed: {}\n\n".format(player.get_speed_modifier()))

        self.console_manager.render_console(self.consoles[GameConsoles.ActionLog], 0, 45)
        self.console_manager.render_console(status_console, 80, 45)

    def render_map(self, current_level, viewer_fov):
        for x, y in viewer_fov:
            if not x >= len(current_level.maze) and not y >= len(current_level.maze[x]):
                if current_level.maze[x][y].is_blocked:
                    self.main_console.drawChar(x, y, '#', fgcolor=COLORS['light_wall'])
                    current_level.maze[x][y].is_explored = True
                if current_level.maze[x][y].is_ground is True:
                    self.main_console.drawChar(x, y, '.', fgcolor=COLORS['light_ground'])
                    current_level.maze[x][y].is_explored = True

    def render_items(self, player, level):
        for item in level.spawned_items:
            x, y = item.location.coords
            if (x, y) in player.fov:
                self.main_console.drawChar(x, y, **item.display.get_draw_info())

    def render_characters(self, player, level):
        # draw monsters
        for monster in level.spawned_monsters:
            x, y = monster.location.get_local_coords()
            if (x, y) in player.fov:
                self.main_console.drawChar(x, y, **monster.display.get_draw_info())

    def render_player(self, player):
        self.main_console.drawChar(
            player.location.local_x,
            player.location.local_y,
            **player.display.get_draw_info()
        )

    def set_tiles_background_color(self, current_level):
        # TODO Instead of using a different color, we should darken whatever color it is.
        # TODO Allowing us to use many colors as walls and tiles to create levels with different looks.
        for y in range(current_level.height):
            for x in range(current_level.width):
                tile = current_level.maze[x][y]
                wall = tile.block_sight
                ground = tile.is_ground

                if tile.is_explored:
                    if wall:
                        self.main_console.drawChar(x, y, '#', fgcolor=COLORS['dark_gray_wall'])
                    elif ground:
                        self.main_console.drawChar(x, y, '.', fgcolor=COLORS['dark_ground'])

    @staticmethod
    def is_transparent(current_level, x, y):
        """
        Used by map.quickFOV to determine which tile fall within the players "field of view"
        """
        try:
            # Pass on IndexErrors raised for when a player gets near the edge of the screen
            # and tile within the field of view fall out side the bounds of the maze.
            tile = current_level.maze[x][y]
            if tile.block_sight and tile.is_blocked:
                return False
            else:
                return True
        except IndexError:
            return False


class Forerunner(object):
    """ 
    The Forerunner will traverse the dungeon and place dungeon objects such as monsters and items
    
    Usage:
        forerunner = Forefunner(level, player)
        forerunner.run()
    """
    # TODO: figure out someplace besides game.py where this should live

    def __init__(self, level, player):
        self.level = level
        self.player = player

    def run(self):
        # place the player in the center of the first room
        first_room = self.level.rooms[0]
        x, y = first_room.center()
        tile = self.level.maze[x][y]
        self._place_player(self.level, tile, self.player)

        self._place_monsters_in_rooms()
        # self.place_items_in_rooms()  # TODO
        # self.place_stairs(self.level.rooms)  # TODO

    def _get_random_room_tile(self, level, room, depth=0):
        """
        Get a random ground tile that does not already contain a object
        @param level: Level being generated.
        @param depth: This prevents crash by infinite recursion.
        @param room:
        @return:
        """
        if room.x1 + 1 < room.x2 - 1:
            x = random.randint(room.x1 + 1, room.x2 - 1)
        else:
            x = room.x1 + 1

        if room.y1 + 1 < room.y2 - 1:
            y = random.randint(room.y1 + 1, room.y2 - 1)
        else:
            y = room.y1 + 1

        tile = level.maze[x][y]

        if not tile.contains_object:
            return tile

        if depth > 50:
            logger.debug("Could not find appropriate tile to spawn items.")
            return tile

        # if we didn't find an empty tile, try again
        return self._get_random_room_tile(level, room, depth=depth + 1)

    def _place_monsters_in_rooms(self):
        """
        Go through each room (thats not the first one) and drop a monster in it. Keep
        going until there are no more monsters to place.
        """
        for room in self.level.rooms[1:]:
            if not self.level.monster_spawn_list:
                break
            tile = self._get_random_room_tile(self.level, room)
            self._place_monster(self.level, tile)

    def _place_items_in_rooms(self):
        """
        Go through each room (thats not the first one) and drop an items in it. Keep
        going until there are no more items to place.
        """
        for item in self.level.item_spawn_list:
            random_room = random.choice(self.level.rooms[1:])
            tile = self._get_random_room_tile(self.level, random_room)
            self._place_item(self.level, tile, item)

    @staticmethod
    def _place_monster(level, tile):
        # TODO This kind of spawning has a few issues, it should use a service to spawn monsters.
        monster = level.monster_spawn_list.pop(0)
        monster.location.local_x = tile.x
        monster.location.local_y = tile.y
        monster.location.level = level
        level.spawned_monsters.append(monster)
        tile.contains_object = True

    @staticmethod
    def _place_player(level, tile, player):
        """
        Place the player in the maze.
        """
        player.location.local_x = tile.x
        player.location.local_y = tile.y
        player.location.level = level
        tile.contains_object = True

    @staticmethod
    def _place_item(level, tile, item):
        # TODO This sort of assignment should use a method and set all required things like global x, area, etc
        item.location.local_x = tile.x
        item.location.local_y = tile.y
        item.level = level

    def _place_stairs(self, tile):
        # TODO Stairs should not be an item but a passable tile.
        pass

