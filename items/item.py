import copy


class Item(object):
    """
    What is an item?
    It made out of a material, it has a type, it can be used.
    It has stats, it can be destroyed, displayed, held.
    It can have a rarity, a level, value.
    It can be sharpened, altered, destroyed and repaired.
    Painted, customized, engraved.
    A good loot system can go a long way in terms of prolonging gameplay.
    """
    def __init__(self, uid, name="", description="", location=None, display=None, weight=1, health=1):
        self.uid = uid
        self.name = name
        self.description = description
        self.location = location
        self.display = display
        self.weight = weight
        self.health = health

    def __eq__(self, other):
        return (
            self.uid == other.uid
            and self.health == other.health
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(
            (
                self.uid,
                self.health
            )
        )


class ItemStack(object):
    """
    Used to combine every identical instances of a specific type in a single stack
    """
    def __init__(self, item):
        self.amount = 1
        self.item = item

    def add_to_stack(self):
        self.amount += 1

    def pop_from_stack(self):
        if self.amount:
            self.amount -= 1
            return copy.copy(self.item)

    def __hash__(self):
        return hash(self.item)
