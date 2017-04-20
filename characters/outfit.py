from stats.enums import StatsEnum


class Outfit(object):
    """
    This represents the outfit at spawn of a character.
    It allows us to apply multiple outfits for multiple type of characters.
    """
    def __init__(self, uid, items_worn=None, items_held=None, items_in_inventory=None):
        self.uid = uid
        self.items_worn = items_worn if items_worn else []
        self.items_held = items_held if items_held else []
        self.items_in_inventory = items_in_inventory if items_in_inventory else []

    def apply(self, game_object):
        if game_object.stats:
            new_size = game_object.stats.get_current_value(StatsEnum.Size)
            if game_object.equipment:
                for item in self.items_worn:
                    item.stats.set_total_core_value(StatsEnum.Size, new_size)
                    game_object.equipment.wear(item)

                for item in self.items_held:
                    item.stats.set_total_core_value(StatsEnum.Size, new_size)
                    game_object.equipment.wield(item)

            if game_object.inventory:
                for item in self.items_in_inventory:
                    game_object.inventory.add_item(item)
