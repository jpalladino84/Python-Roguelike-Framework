from components.inventory import Inventory, KeyBoundInventory
from items.item import Item


def test_inventory_add():
    inventory = Inventory()
    cool_item_1 = Item(uid="cool_item_1", name="Very Cool Item", health=9000)
    cool_item_2 = Item(uid="cool_item_2", name="Very Cool Item Too", health=9000)
    inventory.add_item(cool_item_1)
    inventory.add_item(cool_item_2)

    assert inventory.pop_item("cool_item_1") == cool_item_1
    assert inventory.pop_item("cool_item_1") is None
    assert inventory.pop_item("cool_item_2") == cool_item_2


def test_inventory_keybound():
    inventory = KeyBoundInventory()
    cool_item_1 = Item(uid="cool_item_1", name="Very Cool Item", health=9000)
    cool_item_2 = Item(uid="cool_item_2", name="Very Cool Item Too", health=9000)
    cool_item_1_symbol = inventory.add_item(cool_item_1)
    cool_item_2_symbol = inventory.add_item(cool_item_2)

    assert inventory.pop_item_from_symbol(cool_item_1_symbol) == cool_item_1
    assert inventory.pop_item_from_symbol(cool_item_2_symbol) == cool_item_2

    symbols = []
    for kek in range(0, 1000):
        symbols.append(inventory.add_item(cool_item_1))
    print(symbols)
