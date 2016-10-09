"""
Character Classes
"""
from peewee import SqliteDatabase, Model, ForeignKeyField, FixedCharField, CharField

from settings import DATABASE_NAME
from dungeon.models import DungeonObject, DungeonLevel
from character.components import CharacterClass
from item.components import Inventory

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
    inventory = Inventory()
