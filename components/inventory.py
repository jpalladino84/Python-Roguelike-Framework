from components.component import Component
from items.item import ItemStack


class Inventory(Component):
    """
    The inventory object containing Items via ItemSlots.
    While getting an item from an item seems useless it's to be combined with another type of inventory.
    See Keybound below which is meant for a player.
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
            popped_item = self._item_stacks[item].pop_from_stack()
            if self._item_stacks[item].amount <= 0:
                del self._item_stacks[item]
            return popped_item

    def get_items(self, uid, count=0, pop=False):
        """
        :param uid: uid of item to get.
        :param count: How many to retrieve.
        :param pop: bool to know if we remove it or not.
        :return: List of items found.
        """
        found_items = []
        item_stacks = [item_stack for item_stack in self._item_stacks.values() if item_stack.item.uid == uid]
        for item_stack in item_stacks:
            if count and len(found_items) >= count:
                break

            if pop:
                found_items.append(self.pop_item(item_stack.item))
            else:
                found_items.append(item_stack.item)

        return found_items

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
            self._assigned_symbols[self._page][next_symbol] = item
            return next_symbol

        super(KeyBoundInventory, self).add_item(item)
        return self.get_symbol_from_item(item)

    def get_symbol_from_uid(self, item_uid):
        return next(
            (symbol for page, symbols in self._assigned_symbols.items()
             for symbol, item in symbols.items() if item.uid == item_uid))

    def get_symbol_from_item(self, item):
        for page in self._assigned_symbols.keys():
            for key, value in self._assigned_symbols[page].items():
                if value == item:
                    return key

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
