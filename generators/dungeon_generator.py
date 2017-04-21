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

    @staticmethod
    def _create_room(level, room):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                tile = level.maze[x][y]
                tile.is_blocked = False
                tile.block_sight = False
                tile.is_ground = True

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

    def generate(self, level):
        """
        Generates a new areas based the level
        @param level: Level being generated
        @param player: Character controlled by the player
        """
        # TODO The dungeon's instances are spawned and loaded here.
        # fill map with "blocked" tiles
        level.maze = [[Tile(x, y, True) for y in range(level.height)] for x in range(level.width)]

        for r in range(level.max_rooms):
            # random width and height
            w = random.randint(level.min_room_size, level.max_room_size)
            h = random.randint(level.min_room_size, level.max_room_size)

            # random position without going out of the boundaries of the map
            x = random.randint(0, level.width - w - 1)
            y = random.randint(0, level.height - h - 1)

            # "DungeonRoom" class makes rectangles easier to work with
            new_room = Room(x, y, w, h)
            level.rooms.append(new_room)

            # run through the other rooms and see if they intersect with this one
            failed = False
            for other_room in level.rooms:
                if other_room is not new_room and new_room.intersect(other_room):
                    failed = True
                    break

            if not failed:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                self._create_room(level, new_room)

                # center coordinates of new room, will be useful later
                new_x, new_y = new_room.center()

                if level.num_rooms > 0:
                    # connect it to the previous room with a tunnel
                    # center coordinates of previous room
                    (prev_x, prev_y) = level.rooms[level.num_rooms - 1].center()

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
                level.rooms.append(new_room)
                level.num_rooms += 1

        # connect them with a tunnel
        self._create_h_tunnel(level, 25, 55, 23)


