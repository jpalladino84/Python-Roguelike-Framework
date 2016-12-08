from items.item import ItemStack


class Inventory(object):
    """
    The inventory object containing Items via InventorySlots
    """
    def __init__(self):
        self._item_stacks = dict()

    def add_item(self, item):
        if item.uid in self._item_stacks:
            self._item_stacks[item.uid].add_to_stack()
        else:
            self._item_stacks[item.uid] = ItemStack(item)

    def pop_item(self, item_uid):
        if item_uid in self._item_stacks:
            return self._item_stacks[item_uid].pop_from_stack()

    def get_all_items(self):
        return self._item_stacks.values()


class KeyBoundInventory(Inventory):
    """
    This inventory keeps ascii bindings to added items.
    Used for the player.
    """
    def __init__(self):
        super(KeyBoundInventory, self).__init__()
        self._unassigned_symbols = [chr(i) for i in range(127)]
        self._assigned_symbols = {}

    def add_item(self, item):
        if item not in self._item_stacks:
            self._assigned_symbols[self.__return_next_assigned_symbol()] = item.uid
        super(KeyBoundInventory, self).add_item(item)

    def pop_item_from_symbol(self, symbol):
        self._unassigned_symbols.append(symbol)
        return self.pop_item(self._assigned_symbols.pop(symbol))

    def get_assigned_symbols(self):
        return {symbol: name for symbol, name in self._assigned_symbols.items()}

    def __return_next_assigned_symbol(self):
        return self._unassigned_symbols.pop(0)
