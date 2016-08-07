"""
Character Classes
"""
from peewee import SqliteDatabase, Model, ForeignKeyField, FixedCharField, CharField

from settings import DATABASE_NAME
from dungeon.models import DungeonObject, DungeonLevel
from character.components import CharacterClass

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

# class Player(Character):
#     """
#     Player is a dungeon object.
#
#     The player has a state for which the game_manager uses
#     to keep track of whether the player is alive or dead.
#     """
#     class Meta(object):
#         database = database
#
#     player_state = CharField(max_length=10)
#
#
# class Monster(Character):
#     """
#     Monsters are just dungeon objects with an AI component
#     """
#     class Meta(object):
#         db_table = 'character'
#
#     monster_state = CharField(max_length=10)
