from peewee import SqliteDatabase, Model, IntegerField, TextField, CharField, BooleanField, ForeignKeyField

from settings import DATABASE_NAME


database = SqliteDatabase(DATABASE_NAME)


class DungeonLevel(Model):

    class Meta(object):
        database = database

    level_id = IntegerField()
    level_name = CharField(max_length=20)
    level_desc = TextField(null=True)
    max_room_size = IntegerField()
    min_room_size = IntegerField()
    max_rooms = IntegerField()
    is_final_level = BooleanField()


class Dungeon(Model):

    class Meta(object):
        database = database

    level = ForeignKeyField(DungeonLevel)
    width = IntegerField()
    height = IntegerField()
    maze = TextField()


class DungeonTile(object):
    """
    A tile of the dungeon and its properties
    """
    def __init__(self, x, y, blocked, is_explored=False, is_ground=False, contains_object=False, block_sight=None):
        self.x = x
        self.y = y
        self.is_blocked = blocked
        self.is_explored = is_explored
        self.is_ground = is_ground
        self.contains_object = contains_object

        # y default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight


class DungeonRoom(object):
    """
    A rectangle on the dungeon.
    Used to characterize a room.
    """
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return center_x, center_y

    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)


class DungeonObject(Model):
    """
    An object that is used to keep track of
    location, and whether it blocks another object from moving through it.

    DungeonObject(
        coords=(10, 20),
        blocks=(True | False)
    )
    """
    class Meta(object):
        database = database

    coords = CharField(max_length=20)
    blocks = BooleanField()
