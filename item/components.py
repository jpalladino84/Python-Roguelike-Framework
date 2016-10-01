from peewee import SqliteDatabase, Model, IntegerField, CharField, ForeignKeyField
from models import Item
from settings import DATABASE_NAME

database = SqliteDatabase(DATABASE_NAME)


class Inventory(Model):

    class Meta(object):
        database = database

    inventory_id = IntegerField(index=True)
    item_id = ForeignKeyField(Item)


