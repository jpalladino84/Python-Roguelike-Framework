from components.component import Component
from combat.enums import DamageType
from util.dice import DiceStack, Dice


class Weapon(Component):
    def __init__(self, weapon_category, weapon_type, ammunition_uid, size, finesse=False,
                 loading=False, normal_range=0, long_range=0, reach=False, thrown=False, two_handed=False,
                 melee_damage_type=DamageType.Blunt, ranged_damage_type=None, damage_dice=DiceStack(1, Dice(1))):

        self.weapon_category = weapon_category
        self.weapon_type = weapon_type
        self.ammunition_uid = ammunition_uid
        self.size = size
        self.finesse = finesse
        self.loading = loading
        self.normal_range = normal_range
        self.long_range = long_range
        self.reach = reach
        self.thrown = thrown
        self.two_handed = two_handed
        self.melee_damage_type = melee_damage_type
        self.ranged_damage_type = ranged_damage_type
        self.damage_dice = damage_dice
