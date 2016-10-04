"""
The goal of grouping models is to use them only for saving and loading... Persistence!
"""
from peewee import SqliteDatabase, Model, FixedCharField, IntegerField, TextField, CharField, BooleanField, ForeignKeyField
from math import floor
from settings import DATABASE_NAME


database = SqliteDatabase(DATABASE_NAME)


class Character(Model):

    class Meta(object):
        database = database

    level = ForeignKeyField(DungeonLevel, null=True)
    name = CharField(max_length=20)
    ascii_char = FixedCharField(max_length=2)
    fgcolor = CharField(max_length=15)
    bgcolor = CharField(max_length=15)
    character_state = CharField(max_length=10)
    character_class = ForeignKeyField(CharacterClass, null=True)
    dungeon_object = ForeignKeyField(DungeonObject, null=True)
    inventory_id = IntegerField(null=True)


class CharacterClass(Model):

    class Meta(object):
        database = database

    class_name = CharField(max_length=30)
    max_hp = IntegerField()
    hp = IntegerField()
    defense = IntegerField()
    attack = IntegerField()
    speed = IntegerField()
    inventory_list = CharField(max_length=30, null=True)


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

        return int(floor(center_x)), int(floor(center_y))

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
    blocks = BooleanField(default=False)


class Item(Model):
    """
    Describes an object that can be carried by the player.
    """
    class Meta(object):
        database = database

    level = ForeignKeyField(DungeonLevel, null=True)
    name = CharField(max_length=20)
    description = TextField()
    ascii_char = FixedCharField(max_length=1)
    fgcolor = CharField(max_length=15)
    bgcolor = CharField(max_length=15)
    category = CharField(max_length=20)
    stat_mod = CharField(max_length=10, null=True)
    operation = CharField(max_length=10, null=True)
    value = IntegerField(null=True)
    dungeon_object = ForeignKeyField(DungeonObject, null=True)


class InventorySlot(Model):
    """
    Describes a slot containing an item and referring to an inventory.
    """

    class Meta(object):
        database = database

    inventory_id = IntegerField(index=True)
    item_id = ForeignKeyField(Item, null=True)

    def __init__(self, inventory_id=None, item_id=None):
        super().__init__()
        if inventory_id is None:
            self.inventory_id = InventorySlot.raw("SELECT COUNT(inventory_id) FROM Inventory").execute()
        else:
            self.inventory_id = inventory_id
