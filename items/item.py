import copy

from combat.enums import DamageType
from components.game_object import GameObject


class Item(GameObject):
    NAME = "item"
    """
    What is an item?
    It made out of a material, it has a type, it can be used.
    It has stats, it can be destroyed, displayed, held.
    It can have a rarity, a level, value.
    It can be sharpened, altered, destroyed and repaired.
    Painted, customized, engraved.
    A good loot system can go a long way in terms of extending play time.
    """
    def __init__(self, uid, name="", description="", location=None, display=None):
        super().__init__()
        self.uid = uid
        self._name = name
        self._description = description
        self.location = location
        self.display = display

        # TODO Items should have weapon stats AND armor stats of D&D
        # TODO They should be affected by material, so you can have a base item of iron breastplate of +2 AC
        # TODO that could be reforged to steel for a total of +4 AC that could then be enchanted for a +6
        # TODO Having these materials affects may not be very D&D but lets talk about it again
        # TODO Once you craft a breastplate out of bones.

    @property
    def description(self):
        """
        This property will be able to return altered descriptions for customized items.
        :return: String of current description.
        """
        return self._description

    @property
    def name(self):
        """
        This property will be able to return engraved names for customized items.
        :return: String of current name.
        """
        return self._name

    def copy(self):
        new_item = Item(self.uid, self._name, self._description, self.location, self.display)
        return super().copy_to(new_item)

    def __eq__(self, other):
        return (
            self.uid == other.uid,
            self.name == other.name,
            self.description == other.description,
            self.material == other.material,
            self.stats == other.stats
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(
            (
                self.uid,
                self.name,
                self.description,
                self.material,
                self.stats
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

    def tuple(self):
        return self.item, self.amount

    def __hash__(self):
        return hash(self.item)

    @property
    def description(self):
        """
        This property will be able to return altered descriptions for customized items.
        :return: String of current description.
        """
        return self.item.description

    @property
    def name(self):
        """
        This property will be able to return engraved names for customized items.
        :return: String of current name.
        """
        return self.item.name
