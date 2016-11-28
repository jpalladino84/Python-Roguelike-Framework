from items.item import ItemStack

# TODO Does it make sense to pop an item from an item instance?
# TODO Finish moving symbol handling to a keybound inventory.


class Inventory(object):
    """
    The inventory object containing Items via InventorySlots
    """
    def __init__(self):
        self._item_stacks = dict()

    def add_item(self, item):
        if item in self._item_stacks:
            self._item_stacks[item].add_to_stack()
        else:
            self._item_stacks[item] = ItemStack(item)

    def pop_item(self, item):
        if item in self._item_stacks:
            return self._item_stacks[item].pop_from_stack()


class KeyBoundInventory(Inventory):
    """
    This inventory keeps ascii bindings to added items.
    """
    def __init__(self):
        super(KeyBoundInventory, self).__init__()
        self._unassigned_symbols = [chr(i) for i in range(127)]
        self._assigned_symbols = {}

    def add_item(self, item):
        if item not in self._item_stacks:
            self._assigned_symbols[item] = self.__return_next_assigned_symbol()
        super(KeyBoundInventory, self).add_item(item)


    def pop_item(self, item):
        self._unassigned_symbols.append(symbol)
        del self._item_stacks[symbol]

    def get_item(self, symbol):
        return self._item_stacks[symbol]

    def get_all_items(self):
        return self._item_stacks

    def __return_next_assigned_symbol(self):
        return self._unassigned_symbols.pop(0)