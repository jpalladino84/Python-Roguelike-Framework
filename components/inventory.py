class Inventory(object):
    """
    The inventory object containing Items via InventorySlots
    """
    def __init__(self):
        self._items = dict()
        self._unassigned_symbols = [chr(i) for i in range(127)]

    def add_item(self, item):
        self._items[self.__return_next_assigned_symbol()] = item

    def remove_item(self, symbol):
        self._unassigned_symbols.append(symbol)
        del self._items[symbol]

    def get_item(self, symbol):
        return self._items[symbol]

    def get_all_items(self):
        return self._items

    def __return_next_assigned_symbol(self):
        return self._unassigned_symbols.pop(0)

