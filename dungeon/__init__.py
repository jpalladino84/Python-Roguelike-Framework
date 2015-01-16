"""

"""
import random
import common
from common import Tile, Rect, Object, Item
from characters import Fighter, BasicMonster


# Takes a level to configue dungeon settings
class Dungeon_Generator:

    def __init__(self, level):
        self.width = 80  # Defines the dungeon width
        self.height = 45  # Defines the dungeon height
        self.objects = []
        self.level_id = level.id
        self.max_room_size = level.max_room_size
        self.min_room_size = level.min_room_size
        self.max_rooms = level.max_rooms
        self.max_room_monsters = level.max_room_monsters
        self.num_items = level.num_items
        self.cone = None
        self.player = level.player
        self.stairs = None
        self.map = []
        self._make_map()

        self.objects.append(self.player)

    def _create_room(self, room):

        #go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.map[x][y].blocked = False
                self.map[x][y].block_sight = False
                self.map[x][y].ground = True

    def _create_h_tunnel(self, x1, x2, y):
        #horizontal tunnel. min() and max() are used in case x1>x2
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.map[x][y].blocked = False
            self.map[x][y].block_sight = False
            self.map[x][y].ground = True

    def _create_v_tunnel(self, y1, y2, x):
        #vertical tunnel
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.map[x][y].blocked = False
            self.map[x][y].block_sight = False
            self.map[x][y].ground = True

    def _make_map(self):

        #fill map with "blocked" tiles
        self.map = [[Tile(True)
                    for y in range(self.height)] for x in range(self.width)]

        rooms = []
        num_rooms = 0

        for r in range(self.max_rooms):
            #random width and height
            w = random.randint(self.min_room_size, self.max_room_size)
            h = random.randint(self.min_room_size, self.max_room_size)
            #random position without going out of the boundaries of the map
            x = random.randint(0, self.width - w - 1)
            y = random.randint(0, self.height - h - 1)

            #"Rect" class makes rectangles easier to work with
            new_room = Rect(x, y, w, h)

            #run through the other rooms and see if they intersect with this one
            failed = False
            for other_room in rooms:
                if new_room.intersect(other_room):
                    failed = True
                    break

            if not failed:
                #this means there are no intersections, so this room is valid

                #"paint" it to the map's tiles
                self._create_room(new_room)

                #add some contents to this room, such as monsters
                self.place_objects(new_room)

                #center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    self.player.x = new_x
                    self.player.y = new_y
                else:
                    #all rooms after the first:
                    #connect it to the previous room with a tunnel

                    #center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms-1].center()

                    #draw a coin (random number that is either 0 or 1)
                    if random.randint(0, 1) == 1:
                        #first move horizontally, then vertically
                        self._create_h_tunnel(prev_x, new_x, prev_y)
                        self._create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        #first move vertically, then horizontally
                        self._create_v_tunnel(prev_y, new_y, prev_x)
                        self._create_h_tunnel(prev_x, new_x, new_y)

                #finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

        self.place_item(rooms)

        if self.level_id != 5:
            self.place_stairs(rooms)

        #connect them with a tunnel
        self._create_h_tunnel(25, 55, 23)

    def monster_death(self, monster):
        #transform it into a nasty corpse! it doesn't block, can't be
        #attacked and doesn't move
        monster.char = '%'
        monster.fgcolor = (255, 50, 50)
        monster.blocks = False
        monster.fighter = None
        monster.ai = None
        monster.name = 'remains of ' + monster.name
        common.send_to_back(monster, self.objects)

    def place_objects(self, room):

<<<<<<< HEAD
=======
        if self.player is None:
            # create player and place him in the room
            # this is the first room, where the player starts at
            fighter_component = Fighter(hp=30, defense=2, power=5, speed = 3, death_function=self.player_death)
            self.player = Player(0, 0, '@', 'Hero', True, fighter=fighter_component)

            self.objects.append(self.player)

>>>>>>> Add primitive unit speed.
        #choose random number of monsters
        num_monsters = random.randint(0, self.max_room_monsters)

        for i in range(num_monsters):
            #choose random spot for this monster
            x = random.randint(room.x1+1, room.x2-1)
            y = random.randint(room.y1+1, room.y2-1)

            #only place it if the tile is not blocked
            if not common.is_blocked(x, y, self):
                if random.randint(0, 100) < 80:  # 80% chance of getting an orc
                    #create an orc
                    fighter_component = Fighter(hp=10, defense=0, power=3, speed = 2, death_function=self.monster_death)
                    ai_component = BasicMonster()
                    monster = Object(x, y, 'o', 'orc', fgcolor=(150, 250, 230), blocks=True,
                                     fighter=fighter_component, ai=ai_component)
                else:
                    #create a troll
                    fighter_component = Fighter(hp=16, defense=1, power=4, speed = 1, death_function=self.monster_death)
                    ai_component = BasicMonster()

                    monster = Object(x, y, 'T', 'troll', fgcolor=(100, 180, 150), blocks=True,
                                     fighter=fighter_component, ai=ai_component)

                self.objects.append(monster)

    def place_item(self, rooms):
        for i in range(self.num_items):

            room = random.choice(rooms)  # get a random room

            x = random.randint(room.x1+1, room.x2-1)
            y = random.randint(room.y1+1, room.y2-1)

            if not common.is_blocked(x, y, self):
                item_component = Item()

                if self.level_id == 5:
                    item = Object(x, y, '!', 'Cone of Dunshire', item=item_component)
                    self.cone = item
                else:
                    item = Object(x, y, '!', 'health potion', item=item_component)

                self.objects.append(item)
                common.send_to_back(item, self.objects)
            else:
                # if the spot was blocked find another spot to place the item
                self.place_item(self, rooms)

    def place_stairs(self, rooms):
        room = random.choice(rooms[1::])

        (x, y) = room.center()

        if not common.is_blocked(x, y, self):
            stairs = Object(x, y, '>', 'Stairs')

            self.stairs = stairs
            self.objects.append(stairs)
            common.send_to_back(stairs, self.objects)
