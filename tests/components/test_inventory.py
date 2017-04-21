import unittest

from components.inventory import Inventory, KeyBoundInventory
from items.item import Item


class InventoryTestCase(unittest.TestCase):

    def test_inventory_add(self):
        inventory = Inventory()
        cool_item_1 = Item(uid="cool_item_1", name="Very Cool Item")
        cool_item_2 = Item(uid="cool_item_2", name="Very Cool Item Too")
        inventory.add_item(cool_item_1)
        inventory.add_item(cool_item_2)

        self.assertEqual(inventory.get_items("cool_item_1", pop=True)[0], cool_item_1)
        self.assertGreater(len(inventory.get_items("cool_item_1")), 0)
        self.assertEqual(inventory.get_items("cool_item_2")[0], cool_item_2)

    def test_inventory_keybound(self):
        inventory = KeyBoundInventory()
        cool_item_1 = Item(uid="cool_item_1", name="Very Cool Item")
        cool_item_2 = Item(uid="cool_item_2", name="Very Cool Item Too")
        cool_item_1_symbol = inventory.add_item(cool_item_1)
        cool_item_2_symbol = inventory.add_item(cool_item_2)

        self.assertEqual(inventory.pop_item_from_symbol(cool_item_1_symbol),cool_item_1)
        self.assertEqual(inventory.pop_item_from_symbol(cool_item_2_symbol), cool_item_2)

        symbols = []
        for kek in range(0, 1000):
            symbols.append(inventory.add_item(cool_item_1))
        print(symbols)
