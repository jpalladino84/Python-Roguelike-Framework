import logging
import random

from areas.room import Room
from areas.tile import Tile

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
    def __init__(self, factory_service):
        self.factory_service = factory_service

    def _create_room(self, level, room, player):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                tile = level.maze[x][y]
                tile.is_blocked = False
                tile.block_sight = False
                tile.is_ground = True

        # place the player in the center of the first room
        # TODO We should move this out
        if level.num_rooms == 0:
            x, y = room.center()
            tile = level.maze[x][y]
            self.place_player(level, tile, player)
        else:
            level.monster_rooms.append(room)

    def place_monsters_in_rooms(self, level):
        """
        Go through each room and drop a monster in it. Keep
        going until there are no more monsters to place.
        """
        for room in level.monster_rooms:
            if not level.monster_spawn_list:
                break
            tile = self.get_random_room_tile(level, room)
            self.place_monster(level, tile)

    def place_items_in_rooms(self, level):
        """
        Go through each room and drop an items in it. Keep
        going until there are no more items to place.
        """
        for item in level.item_spawn_list:
            # TODO Why monster rooms?
            random_room = random.choice(level.monster_rooms)
            tile = self.get_random_room_tile(random_room, level)
            self.place_item(level, tile, item)

    def get_random_room_tile(self, level, room, depth=0):
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
            logger_.debug("Could not find appropriate tile to spawn items.")
            return tile

        # if we didn't find an empty tile, try again
        return self.get_random_room_tile(level, room, depth=depth + 1)

    @staticmethod
    def _create_h_tunnel(level, x1, x2, y):
        # horizontal tunnel. min() and max() are used in case x1>x2
        for x in range(min(x1, x2), max(x1, x2) + 1):
            level.maze[x][y].is_blocked = False
            level.maze[x][y].block_sight = False
            level.maze[x][y].is_ground = True

    @staticmethod
    def _create_v_tunnel(level, y1, y2, x):
        # vertical tunnel
        for y in range(min(y1, y2), max(y1, y2) + 1):
            level.maze[x][y].is_blocked = False
            level.maze[x][y].block_sight = False
            level.maze[x][y].is_ground = True

    def generate(self, level, player):
        """
        Generates a new areas based the level
        @param level: Level being generated
        @param player: Character controlled by the player
        """
        # TODO The dungeon's instances are spawned and loaded here.
        # fill map with "blocked" tiles
        level.maze = [[Tile(x, y, True) for y in range(level.height)] for x in range(level.width)]
        rooms = []

        for r in range(level.max_rooms):
            # random width and height
            w = random.randint(level.min_room_size, level.max_room_size)
            h = random.randint(level.min_room_size, level.max_room_size)

            # random position without going out of the boundaries of the map
            x = random.randint(0, level.width - w - 1)
            y = random.randint(0, level.height - h - 1)

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
                self._create_room(level, new_room, player)

                # center coordinates of new room, will be useful later
                new_x, new_y = new_room.center()

                if level.num_rooms > 0:
                    # connect it to the previous room with a tunnel
                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[level.num_rooms - 1].center()

                    # draw a coin (random number that is either 0 or 1)
                    if random.randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self._create_h_tunnel(level, prev_x, new_x, prev_y)
                        self._create_v_tunnel(level, prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self._create_v_tunnel(level, prev_y, new_y, prev_x)
                        self._create_h_tunnel(level, prev_x, new_x, new_y)

                # finally, append the new room to the list
                rooms.append(new_room)
                level.num_rooms += 1

        self.place_monsters_in_rooms(level)
        self.place_items_in_rooms(level)
        self.place_stairs(rooms)

        # connect them with a tunnel
        self._create_h_tunnel(level, 25, 55, 23)

    @staticmethod
    def place_monster(level, tile):
        # TODO This kind of spawning has a few issues, it should use a service to spawn monsters.
        monster = level.monster_spawn_list.pop(0)
        monster.location.local_x = tile.x
        monster.location.local_y = tile.y
        monster.location.level = level
        level.spawned_monsters.append(monster)
        tile.contains_object = True

    @staticmethod
    def place_player(level, tile, player):
        """
        Place the player in the maze.
        """
        player.location.local_x = tile.x
        player.location.local_y = tile.y
        player.location.level = level
        tile.contains_object = True

    @staticmethod
    def place_item(level, tile, item):
        # TODO This sort of assignment should use a method and set all required things like global x, area, etc
        item.location.local_x = tile.x
        item.location.local_y = tile.y
        item.level = level

    def place_stairs(self, tile):
        # TODO Stairs should not be an item but a passable tile.
        pass
