from components.component import Component


class Armor(Component):
    """
    Component to make an object wearable.
    """
    def __init__(self, base_armor_class, required_strength,
                 armor_category, dexterity_disadvantage, maximum_dexterity_bonus,
                 worn_layer, wearable_body_parts_uid):

        self.base_armor_class = base_armor_class
        self.required_strength = required_strength
        self.dexterity_disadvantage = dexterity_disadvantage
        self.maximum_dexterity_bonus = maximum_dexterity_bonus
        self.worn_layer = worn_layer
        self.wearable_body_parts_uid = wearable_body_parts_uid
        self.armor_category = armor_category
