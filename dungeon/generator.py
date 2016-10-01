import logging
import json
import random
from collections import deque

from dungeon.models import Dungeon, DungeonTile, DungeonRoom, DungeonObject, DungeonLevel
from character.models import Character
from item.models import Item

logger_ = logging.getLogger("generator")
logger_.addHandler(logging.StreamHandler())


class DungeonGenerator(object):
    """
    Takes a level config and outputs a new dungeon maze.
    """
    dungeon_monsters = []
    dungeon_items = []
    num_rooms = 0
    is_final_level = False
    level = None
    maze = []
    monster_rooms = []

    def _create_room(self, room):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                tile = self.maze[x][y]
                tile.is_blocked = False
                tile.block_sight = False
                tile.is_ground = True

        # place the player in the center of the first room
        if self.num_rooms == 0:
            x, y = room.center()
            tile = self.maze[x][y]
            self.place_player(tile)
        else:
            self.monster_rooms.append(room)

    def place_monsters_in_rooms(self):
        """
        Go through each room and drop a monster in it. Keep
        going until there are no more monsters to place.
        """
        while len(self.dungeon_monsters):
            for room in self.monster_rooms:
                tile = self.get_random_room_tile(room)
                self.place_monster(tile)

    def place_items_in_rooms(self):
        """
        Go through each room and drop an item in it. Keep
        going until there are no more items to place.
        """
        for item in self.dungeon_items:
            random_room = random.choice(self.monster_rooms)
            tile = self.get_random_room_tile(random_room)
            self.place_item(tile, item)

    def get_random_room_tile(self, room, depth=0):
        """
        Get a random ground tile that does not already contain a object

        @param room:
        @return:
        """
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)
        tile = self.maze[x][y]

        if not tile.contains_object:
            return tile

        if depth > 50:
            logger_.debug("Could not find appropriate tile to spawn item.")
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

    def generate(self, level):
        """
        Generates a new dungeon based the level
        @param level:
        """
        width = 80
        height = 45
        max_rooms = level.max_rooms
        max_room_size = level.max_room_size
        min_room_size = level.min_room_size

        self.level = level
        self.is_final_level = level.is_final_level
        self.dungeon_monsters = deque([m for m in
                                       Character
                                      .select()
                                      .join(DungeonLevel)
                                      .where(
                                           (DungeonLevel.level_id == level.level_id) &
                                           (Character.name != 'player'))
                                       ])

        self.dungeon_items = deque([item for item in Item
                                   .select()
                                   .join(DungeonLevel)
                                   .where((DungeonLevel.level_id == level.level_id))])

        # self.max_num_items = level.max_num_items
        # fill map with "blocked" tiles
        self.maze = [[DungeonTile(x, y, True) for y in range(height)] for x in range(width)]

        rooms = []

        for r in range(max_rooms):
            # random width and height
            w = random.randint(min_room_size, max_room_size)
            h = random.randint(min_room_size, max_room_size)
            # random position without going out of the boundaries of the map
            x = random.randint(0, width - w - 1)
            y = random.randint(0, height - h - 1)

            # "DungeonRoom" class makes rectangles easier to work with
            new_room = DungeonRoom(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
            failed = False
            for other_room in rooms:
                if new_room.intersect(other_room):
                    failed = True
                    break

            if not failed:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                self._create_room(new_room)

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
        # if not level.final_level:
        #     self.place_stairs(rooms)

        # connect them with a tunnel
        self._create_h_tunnel(25, 55, 23)

        serialized_maze = json.dumps([
            [
                {
                    'x': tile.x,
                    'y': tile.y,
                    'is_blocked': tile.is_blocked,
                    'is_explored': tile.is_explored,
                    'is_ground': tile.is_ground,
                    'contains_object': tile.contains_object,
                    'block_sight': tile.block_sight
                } for tile in row
            ] for row in self.maze
        ])

        new_dungeon = Dungeon(level=level, width=width, height=height, maze=serialized_maze)
        new_dungeon.save()

    def place_monster(self, tile):

        try:
            monster = self.dungeon_monsters.popleft()
            new_dungeon_object = DungeonObject(
                coords=json.dumps((tile.x, tile.y)),
                blocks=True
            )
            new_dungeon_object.save()
            monster.dungeon_object = new_dungeon_object
            monster.save()
            tile.contains_object = True
        except IndexError:
            pass

    def place_player(self, tile):
        """
        Place the player in the maze.
        """
        dungeon_object = DungeonObject(
            coords=json.dumps((tile.x, tile.y)),
            blocks=True
        )

        player = Character.get(Character.name == 'player')
        player.level = self.level
        player.dungeon_object = dungeon_object

        dungeon_object.save()
        player.save()

        tile.contains_object = True

    def place_item(self, tile, item):
        item.dungeon_object = DungeonObject(coords=json.dumps((tile.x, tile.y)))
        item.level = self.level
        item.dungeon_object.save()
        item.save()

# def place_stairs(self, tile):
#     TODO: fix this to use new item system
#     room = random.choice(rooms[1::])
#
#     (x, y) = room.center()
#
#     if not util.is_blocked(x, y, self):
#         stairs = DungeonObject(x, y, '>', 'Stairs')
#
#         self.stairs = stairs
#         self.objects.append(stairs)
#         util.send_to_back(stairs, self.objects)
#     else:
#         # if the spot was blocked find another spot to place the item
#         self.place_stairs(rooms)
