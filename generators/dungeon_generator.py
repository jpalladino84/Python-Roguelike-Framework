import logging
import json
import random
from collections import deque

from areas.area import Area
from areas.level import Level
from areas.room import Room
from areas.tile import Tile
from characters.character import Character
from items.item import Item

logger_ = logging.getLogger("generator")
logger_.addHandler(logging.StreamHandler())

"""
We will want to have many generators, as template we could start with
World Generator, Dungeon Generator, Wilderness Generator.
"""


class DungeonGenerator(object):
    """
        Takes a level config and outputs a new areas maze.
    """

    dungeon_monsters = []
    dungeon_items = []
    num_rooms = 0
    is_final_level = False
    level = None
    maze = []
    monster_rooms = []

    def _create_room(self, room, player):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                tile = self.maze[x][y]
                tile.is_blocked = False
                tile.block_sight = False
                tile.is_ground = True

        # place the player in the center of the first room
        # TODO We should move this out
        if self.num_rooms == 0:
            x, y = room.center()
            tile = self.maze[x][y]
            self.place_player(tile, player)
        else:
            self.monster_rooms.append(room)

    def place_monsters_in_rooms(self):
        """
        Go through each room and drop a monster in it. Keep
        going until there are no more monsters to place.
        """
        for room in self.monster_rooms:
            if not self.dungeon_monsters:
                break
            tile = self.get_random_room_tile(room)
            self.place_monster(tile)

    def place_items_in_rooms(self):
        """
        Go through each room and drop an items in it. Keep
        going until there are no more items to place.
        """
        for item in self.dungeon_items:
            random_room = random.choice(self.monster_rooms)
            tile = self.get_random_room_tile(random_room)
            self.place_item(tile, item)

    def get_random_room_tile(self, room, depth=0):
        """
        Get a random ground tile that does not already contain a object
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

        tile = self.maze[x][y]

        if not tile.contains_object:
            return tile

        if depth > 50:
            logger_.debug("Could not find appropriate tile to spawn items.")
            return tile

        # if we didn't find an empty tile, try again
        return self.get_random_room_tile(room, depth=depth + 1)

    def _create_h_tunnel(self, x1, x2, y):
        # horizontal tunnel. min() and max() are used in case x1>x2
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.maze[x][y].is_blocked = False
            self.maze[x][y].block_sight = False
            self.maze[x][y].is_ground = True

    def _create_v_tunnel(self, y1, y2, x):
        # vertical tunnel
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.maze[x][y].is_blocked = False
            self.maze[x][y].block_sight = False
            self.maze[x][y].is_ground = True

    def generate(self, level, player):
        """
        Generates a new areas based the level
        @param level:
        """

        width = 80
        height = 45
        self.width = width
        self.height = height
        max_rooms = level.max_rooms
        max_room_size = level.max_room_size
        min_room_size = level.min_room_size

        self.level = level
        # TODO a Final Level does not always happen, must be configurable
        self.is_final_level = False
        # TODO The dungeon's instances are spawned and loaded here.
        self.dungeon_monsters = level.monsters
        self.dungeon_items = deque()

        # fill map with "blocked" tiles
        self.maze = [[Tile(x, y, True) for y in range(height)] for x in range(width)]

        rooms = []

        for r in range(max_rooms):
            # random width and height
            w = random.randint(min_room_size, max_room_size)
            h = random.randint(min_room_size, max_room_size)

            # random position without going out of the boundaries of the map
            x = random.randint(0, width - w - 1)
            y = random.randint(0, height - h - 1)

            # "DungeonRoom" class makes rectangles easier to work with
            new_room = Room(x, y, w, h)
            rooms.append(new_room)

            # run through the other rooms and see if they intersect with this one
            failed = False
            for other_room in rooms:
                if other_room is not new_room and new_room.intersect(other_room):
                    failed = True
                    break

            if not failed:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                self._create_room(new_room, player)

                # center coordinates of new room, will be useful later
                new_x, new_y = new_room.center()

                if self.num_rooms > 0:
                    # connect it to the previous room with a tunnel
                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[self.num_rooms-1].center()

                    # draw a coin (random number that is either 0 or 1)
                    if random.randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self._create_h_tunnel(prev_x, new_x, prev_y)
                        self._create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self._create_v_tunnel(prev_y, new_y, prev_x)
                        self._create_h_tunnel(prev_x, new_x, new_y)

                # finally, append the new room to the list
                rooms.append(new_room)
                self.num_rooms += 1

        self.place_monsters_in_rooms()
        self.place_items_in_rooms()
        self.place_stairs(rooms)

        # connect them with a tunnel
        self._create_h_tunnel(25, 55, 23)

    def place_monster(self, tile):
        # TODO This kind of spawning has a few issues, it should use a service to spawn monsters.
        monster = self.dungeon_monsters.pop(0)
        monster.location.local_x = tile.x
        monster.location.local_y = tile.y
        tile.contains_object = True

    def place_player(self, tile, player):
        """
        Place the player in the maze.
        """
        player.location.local_x = tile.x
        player.location.local_y = tile.y
        player.location.level = self.level
        tile.contains_object = True

    def place_item(self, tile, item):
        # TODO This sort of assignment should use a method and set all required things like global x, area, etc
        item.location.local_x = tile.x
        item.location.local_y = tile.y
        item.level = self.level

    def place_stairs(self, tile):
        # TODO Stairs should not be an item but a passable tile.
        pass
