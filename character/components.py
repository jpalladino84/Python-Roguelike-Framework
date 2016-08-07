from peewee import SqliteDatabase, Model, IntegerField, CharField

from settings import DATABASE_NAME

database = SqliteDatabase(DATABASE_NAME)


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
