from components.inventory import Inventory, KeyBoundInventory
from items.item import Item
from datetime import datetime


def test_inventory_add():
    inventory = Inventory()
    cool_item_1 = Item(uid="cool_item_1", name="Very Cool Item")
    cool_item_2 = Item(uid="cool_item_2", name="Very Cool Item Too")
    inventory.add_item(cool_item_1)
    inventory.add_item(cool_item_2)

    assert inventory.get_items("cool_item_1", pop=True)[0] == cool_item_1
    assert len(inventory.get_items("cool_item_1")) == 0
    assert inventory.get_items("cool_item_2")[0] == cool_item_2
    assert inventory.get_items("cool_item_2")[0] == cool_item_2


def test_inventory_keybound():
    inventory = KeyBoundInventory()
    cool_item_1 = Item(uid="cool_item_1", name="Very Cool Item")
    cool_item_2 = Item(uid="cool_item_2", name="Very Cool Item Too")
    cool_item_1_symbol = inventory.add_item(cool_item_1)
    cool_item_2_symbol = inventory.add_item(cool_item_2)

    assert inventory.pop_item_from_symbol(cool_item_1_symbol) == cool_item_1
    assert inventory.pop_item_from_symbol(cool_item_2_symbol) == cool_item_2

    symbols = []
    for kek in range(0, 1000):
        symbols.append(inventory.add_item(cool_item_1))
    print(symbols)


def test_performance_inventories():
    inventory = Inventory()
    keybound_inventory = KeyBoundInventory()

    start_iteration_1 = datetime.now()
    for _ in range(0, 1000):
        inventory.add_item(Item(uid="cool_item_1", name="Very Cool Item"))
    end_iteration_1 = datetime.now()

    start_iteration_2 = datetime.now()
    for _ in range(0, 1000):
        inventory.get_items(uid="cool_item_1")
    end_iteration_2 = datetime.now()

    bound_symbols = []
    start_iteration_3 = datetime.now()
    for _ in range(0, 1000):
        bound_symbols.append(keybound_inventory.add_item(Item(uid="cool_item_1", name="Very Cool Item")))
    end_iteration_3 = datetime.now()

    start_iteration_4 = datetime.now()
    for symbol in bound_symbols:
        pass
        #keybound_inventory.pop_item_from_symbol(symbol)
    end_iteration_4 = datetime.now()

    print("Iteration 1 time:" + str(end_iteration_1 - start_iteration_1))
    print("Iteration 2 time:" + str(end_iteration_2 - start_iteration_2))
    print("Iteration 3 time:" + str(end_iteration_3 - start_iteration_3))
    print("Iteration 4 time:" + str(end_iteration_4 - start_iteration_4))