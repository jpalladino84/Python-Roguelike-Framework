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
    def __init__(self):
        self.name = ""
        self.description = ""
        self.location = None
        self.display = None
        self.weight = 1
        self.health = 1
