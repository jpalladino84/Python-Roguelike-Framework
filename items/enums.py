from enum import Enum


class ArmorCategory(Enum):
    Light = 0
    Medium = 1
    Heavy = 2


class WeaponCategory(Enum):
    Simple = 0
    Martial = 1


class WeaponType(Enum):
    Melee = 0
    Ranged = 1


class WornLayer(Enum):
    Inner = 0
    Outer = 1
    Extra = 2