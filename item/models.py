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
    inventory_list = CharField(max_length=20)
    category = CharField(max_length=20)
    stat_mod = CharField(max_length=10, null=True)
    operation = CharField(max_length=10, null=True)
    value = IntegerField(null=True)
    dungeon_object = ForeignKeyField(DungeonObject, null=True)
