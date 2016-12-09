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
    # noinspection SpellCheckingInspection
    CHARACTER_SET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789°!\"#$%?&*()_+^:'.|{}[]@"
    """
    This inventory keeps ascii bindings to added items.
    Used for the player.
    """
    def __init__(self):
        super(KeyBoundInventory, self).__init__()
        self._page = 0
        self._max_page = 0
        self._unassigned_symbols = {0: list(KeyBoundInventory.CHARACTER_SET)}
        self._assigned_symbols = {0: {}}

    def add_item(self, item):
        if item not in self._item_stacks:
            super(KeyBoundInventory, self).add_item(item)
            next_symbol = self.__return_next_assigned_symbol()
            self._assigned_symbols[self._page][next_symbol] = item.uid
            return next_symbol

        super(KeyBoundInventory, self).add_item(item)
        return self.get_symbol_from_uid(item.uid)

    def get_symbol_from_uid(self, item_uid):
        return next(
            (symbol for page, symbols in self._assigned_symbols.items()
             for symbol, uid in symbols.items() if uid == item_uid))

    def pop_item_from_symbol(self, symbol):
        self._unassigned_symbols[self._page].append(symbol)
        return self.pop_item(self._assigned_symbols[self._page].pop(symbol))

    def get_assigned_symbols(self, page):
        return {symbol: name for symbol, name in self._assigned_symbols[page].items()}

    def __return_next_assigned_symbol(self):
        if not self._unassigned_symbols[self._page]:
            page = self.__find_available_page_or_create()
            return self._unassigned_symbols[page].pop(0)
        return self._unassigned_symbols[self._page].pop(0)

    def __find_available_page_or_create(self):
        for page, available_symbols in self._unassigned_symbols.items():
            if available_symbols:
                return page
        self._max_page += 1
        self._unassigned_symbols[self._max_page] = list(self.CHARACTER_SET)
        return self._max_page
