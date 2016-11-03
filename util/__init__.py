"""
Utility functions
"""
from peewee import SqliteDatabase

from areas.models import DungeonLevel, DungeonObject, Dungeon
from settings import DATABASE_NAME


def create_tables():
    database = SqliteDatabase(DATABASE_NAME)
    database.connect()
    database.create_table([Dungeon, DungeonLevel, DungeonObject])


def send_to_back(obj, objects):
    # make this object be drawn first, so all others appear above it if
    # they're in the same tile.

    objects.remove(obj)
    objects.insert(0, obj)
