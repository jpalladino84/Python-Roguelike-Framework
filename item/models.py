from peewee import SqliteDatabase, Model, CharField, IntegerField, TextField, ForeignKeyField, FixedCharField

from settings import DATABASE_NAME
from dungeon.models import DungeonObject, DungeonLevel

database = SqliteDatabase(DATABASE_NAME)


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

