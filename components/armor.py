from components.component import Component


class Armor(Component):
    NAME = "armor"
    """
    Component to make an object wearable.
    """
    def __init__(self, armor_category, worn_layer, wearable_body_parts_uid, base_armor_class=0,
                 required_strength=0, dexterity_disadvantage=0, maximum_dexterity_bonus=None):
        super().__init__()
        self.base_armor_class = base_armor_class
        self.required_strength = required_strength
        self.dexterity_disadvantage = dexterity_disadvantage
        self.maximum_dexterity_bonus = maximum_dexterity_bonus
        self.worn_layer = worn_layer
        self.wearable_body_parts_uid = wearable_body_parts_uid
        self.armor_category = armor_category

    def copy(self):
        return Armor(
            armor_category=self.armor_category,
            base_armor_class=self.base_armor_class,
            dexterity_disadvantage=self.dexterity_disadvantage,
            required_strength=self.required_strength,
            maximum_dexterity_bonus=self.maximum_dexterity_bonus,
            wearable_body_parts_uid=self.wearable_body_parts_uid,
            worn_layer=self.worn_layer,
        )
