from peewee import SqliteDatabase, Model, IntegerField, ForeignKeyField
from settings import DATABASE_NAME


database = SqliteDatabase(DATABASE_NAME)


class Inventory(object):
    """
    The inventory object containing Items via InventorySlots
    """
    def __init__(self):
        self.inventory_id = None
        self.items = {}

    def add_item(self, item):
        if not self.__check_if_item_in_inventory(item):
            self.items[item.get_id()] = item

    def __check_if_item_in_inventory(self, item):
        if item.get_id() not in self.items:
            return False
        else:
            return True
