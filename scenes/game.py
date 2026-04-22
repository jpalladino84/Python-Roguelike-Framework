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
from data.python_templates.items import build_health_potion

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class GameConsoles(Enum):
    ActionLog = 0
    Status = 1
    Controls = 2


class GameScene(BaseScene):
    """
    This handles everything relating to the UI in the game window.
    """
    ID = "Game"

    def __init__(self, console_manager, scene_manager, game_context):
        super().__init__(console_manager, scene_manager, game_context)
        # TODO Eventually we will want to map more than just movement keys
        self.loaded_levels = {}  # depth (int) -> Level
        self.current_depth = 1
        self.movement_keys = settings.KEY_MAPPINGS
        self.consoles = {
            GameConsoles.ActionLog: self.console_manager.create_new_console(80, 15),
            GameConsoles.Status: self.console_manager.create_new_console(20, 15),
            GameConsoles.Controls: self.console_manager.create_new_console(20, 45),
        }
        self.action_manager = ActionManager(self.consoles[GameConsoles.ActionLog])
        self.echo_service = EchoService(self.consoles[GameConsoles.ActionLog], game_context)
        self.inventory_open = False

        game_context.echo_service = self.echo_service
        self._draw_controls_panel()
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
            self.consoles[GameConsoles.Status].drawStr(0, 6, 'Press any key...')
        if self.inventory_open:
            self.render_inventory(player)

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
                # Transition to game over on any key when dead
                if player.is_dead():
                    self.game_context.depth_reached = self.current_depth
                    self.transition_to("GameOverScene")
                    return

                # Toggle inventory
                if key_event.keychar == "i" or (self.inventory_open and key_event.key == "ESCAPE"):
                    self.inventory_open = not self.inventory_open
                    continue

                # Inventory input — consume item by letter key
                if self.inventory_open:
                    items = list(player.inventory.get_all_items())
                    for idx, item_stack in enumerate(items):
                        if idx >= 26:
                            break
                        if key_event.keychar.lower() == chr(ord('a') + idx):
                            consumable = item_stack.item.get_component('consumable')
                            if consumable:
                                msg = consumable.use(player)
                                player.inventory.pop_item(item_stack.item)
                                self.echo_service.console.printStr(msg + "\n")
                            self.inventory_open = False
                            break
                    continue

                if not player.is_dead():
                    if key_event.key == 'KP5' or key_event.key == '.':
                        moved = True

                    if key_event.keychar.upper() in self.movement_keys:
                        key_x, key_y = self.movement_keys[key_event.keychar.upper()]
                        self.action_manager.move_or_attack(player, key_x, key_y)
                        moved = True
                        tile = player.location.level.maze[player.location.local_x][player.location.local_y]
                        if tile.stair_down:
                            self.descend(player)
                        elif tile.stair_up:
                            self.ascend(player)

                    if key_event.keychar == "g":
                        px, py = player.location.local_x, player.location.local_y
                        for item in list(current_level.spawned_items):
                            if item.location.local_x == px and item.location.local_y == py:
                                player.inventory.add_item(item)
                                current_level.spawned_items[:] = [i for i in current_level.spawned_items if i is not item]
                                self.echo_service.console.printStr(
                                    "You pick up {}.\n".format(item.name))
                                moved = True
                                break

                    if moved:
                        for monster in player.location.level.spawned_monsters:
                            self.action_manager.monster_take_turn(monster, player)
                        moved = False

    def new_game(self):
        level = self._build_level(depth=1)
        self.loaded_levels[1] = level
        self.current_depth = 1
        self.init_dungeon(level)

    def _build_level(self, depth):
        level = Level()
        level.name = "Level {}".format(depth)
        level.depth = depth
        level.min_room_size = 4
        level.max_room_size = 10
        level.max_rooms = 10
        level.width = 80
        level.height = 45
        return level

    def init_dungeon(self, level):
        # TODO The player must be built and retrieved here.
        dungeon_generator = DungeonGenerator(self.game_context.factory_service)
        player = self.game_context.player
        player.is_player = True
        dungeon_generator.generate(level)
        self.place_dungeon_objects(level, player)

    def descend(self, player):
        next_depth = self.current_depth + 1
        if next_depth not in self.loaded_levels:
            level = self._build_level(depth=next_depth)
            self.loaded_levels[next_depth] = level
            self.init_dungeon(level)  # Forerunner places player at first room (= up-stairs)
        else:
            level = self.loaded_levels[next_depth]
            x, y = level.stair_up_pos
            player.location.local_x = x
            player.location.local_y = y
            player.location.level = level
        self.current_depth = next_depth
        self.consoles[GameConsoles.ActionLog].drawStr(0, 0, "You descend deeper into the dungeon.")

    def ascend(self, player):
        if self.current_depth <= 1:
            return
        prev_depth = self.current_depth - 1
        level = self.loaded_levels[prev_depth]
        x, y = level.stair_down_pos
        player.location.local_x = x
        player.location.local_y = y
        player.location.level = level
        self.current_depth = prev_depth
        self.consoles[GameConsoles.ActionLog].drawStr(0, 0, "You ascend toward the surface.")

    def place_dungeon_objects(self, level, player):
        character_factory = self.game_context.character_factory
        level.monster_spawn_list = self._build_monster_list(character_factory, level.depth)
        level.item_spawn_list = [build_health_potion() for _ in range(4)]

        forerunner = Forerunner(level, player)
        forerunner.run()

    @staticmethod
    def _build_monster_list(character_factory, depth):
        if depth <= 2:
            pool = ["weak_orc", "goblin_thief"]
            count = 2
        elif depth <= 4:
            pool = ["weak_orc", "strong_orc", "skeleton_warrior", "goblin_thief"]
            count = 3
        else:
            pool = ["weak_orc", "strong_orc", "weak_troll", "skeleton_warrior", "goblin_thief"]
            count = min(4 + (depth - 5), 6)

        monsters = [character_factory.build(uid) for uid in random.choices(pool, k=count)]
        for monster in monsters:
            GameScene._scale_monster(monster, depth)
        return monsters

    @staticmethod
    def _scale_monster(monster, depth):
        if depth <= 1:
            return
        # Scale HP: +20% per floor beyond 1
        max_hp = monster.stats.get_maximum_value(StatsEnum.Health)
        new_hp = max(1, round(max_hp * (1.0 + (depth - 1) * 0.2)))
        monster.stats.set_core_current_value(StatsEnum.Health, new_hp)
        monster.stats.set_core_maximum_value(StatsEnum.Health, new_hp)
        # Scale strength: +1 per floor so enemies eventually break through armor
        monster.stats.modify_core_current_value(StatsEnum.Strength, depth - 1)
        # Scale XP reward
        monster.xp_value = round(monster.xp_value * (1.0 + (depth - 1) * 0.25))

    def render_gui(self, player):
        status_console = self.consoles[GameConsoles.Status]
        status_console.clear()
        pool = player.experience_pool
        current_hp = int(player.stats.get_current_value(StatsEnum.Health))
        max_hp = int(player.stats.get_maximum_value(StatsEnum.Health))
        strength = int(player.stats.get_current_value(StatsEnum.Strength))
        dexterity = int(player.stats.get_current_value(StatsEnum.Dexterity))
        status_console.drawStr(0, 0, "Depth: {}".format(self.current_depth))
        status_console.drawStr(0, 2, "Level: {}".format(pool.total_level))
        status_console.drawStr(0, 4, "XP:{}/{}".format(pool.experience, pool.get_xp_for_next_level()))
        status_console.drawStr(0, 6, "HP: {}/{}".format(current_hp, max_hp))
        status_console.drawStr(0, 8, "Str: {}  Def: {}".format(strength, player.get_armor_class()))
        status_console.drawStr(0, 10, "Dex: {}".format(dexterity))

        self.console_manager.render_console(self.consoles[GameConsoles.ActionLog], 0, 45)
        self.console_manager.render_console(status_console, 80, 45)
        self.console_manager.render_console(self.consoles[GameConsoles.Controls], 80, 0)

    def _draw_controls_panel(self):
        c = self.consoles[GameConsoles.Controls]
        lines = [
            "-- Controls --------",
            "",
            "Move",
            " Arrow keys",
            " Numpad 1-9",
            "",
            "Wait",
            " . or Numpad 5",
            "",
            "Pick up item",
            " g",
            "",
            "Inventory",
            " i",
            "",
            "Use item",
            " i, then a-z",
            "",
            "Close inventory",
            " i or ESC",
            "",
            "Stairs",
            " Walk onto > or <",
            "--------------------",
        ]
        for row, text in enumerate(lines):
            c.drawStr(0, row, text)

    def render_map(self, current_level, viewer_fov):
        for x, y in viewer_fov:
            if not x >= len(current_level.maze) and not y >= len(current_level.maze[x]):
                tile = current_level.maze[x][y]
                if tile.is_blocked:
                    self.main_console.drawChar(x, y, '#', fgcolor=COLORS['light_wall'])
                    tile.is_explored = True
                if tile.is_ground:
                    if tile.stair_down:
                        self.main_console.drawChar(x, y, '>', fgcolor=COLORS['stair'])
                    elif tile.stair_up:
                        self.main_console.drawChar(x, y, '<', fgcolor=COLORS['stair'])
                    else:
                        self.main_console.drawChar(x, y, '.', fgcolor=COLORS['light_ground'])
                    tile.is_explored = True

    def render_items(self, player, level):
        for item in level.spawned_items:
            x, y = item.location.local_x, item.location.local_y
            if (x, y) in player.fov:
                self.main_console.drawChar(x, y, **item.display.get_draw_info())

    def render_inventory(self, player):
        x, y = 5, 2
        items = list(player.inventory.get_all_items())
        self.main_console.drawStr(x, y,     "================================")
        self.main_console.drawStr(x, y + 1, " INVENTORY  (letter=use, i=close)")
        self.main_console.drawStr(x, y + 2, "================================")
        if items:
            for i, item_stack in enumerate(items):
                if i >= 26:
                    break
                letter = chr(ord('a') + i)
                self.main_console.drawStr(x, y + 3 + i,
                    " {}) {} x{}".format(letter, item_stack.item.name, item_stack.amount))
        else:
            self.main_console.drawStr(x, y + 3, " Your inventory is empty.")
        row = y + 3 + max(len(items), 1) + 1
        self.main_console.drawStr(x, row, "================================")

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
                        if tile.stair_down:
                            self.main_console.drawChar(x, y, '>', fgcolor=COLORS['dark_stair'])
                        elif tile.stair_up:
                            self.main_console.drawChar(x, y, '<', fgcolor=COLORS['dark_stair'])
                        else:
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
        self._place_items_in_rooms()
        self._place_stairs()

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
        if len(self.level.rooms) < 2:
            return
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
        from components.location import Location
        if item.location is None:
            item.location = Location()
        item.location.local_x = tile.x
        item.location.local_y = tile.y
        item.location.level = level
        level.spawned_items.append(item)

    def _place_stairs(self):
        # Down stairs go in the last room
        last_room = self.level.rooms[-1]
        dx, dy = last_room.center()
        down_tile = self.level.maze[dx][dy]
        down_tile.stair_down = True
        self.level.stair_down_pos = (dx, dy)

        # Up stairs go in the first room (only on levels below the surface)
        if self.level.depth > 1:
            first_room = self.level.rooms[0]
            ux, uy = first_room.center()
            up_tile = self.level.maze[ux][uy]
            up_tile.stair_up = True
            self.level.stair_up_pos = (ux, uy)

