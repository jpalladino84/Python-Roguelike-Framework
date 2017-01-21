from enum import Enum


class AttackType(Enum):
    Melee = 0
    Ranged = 1
    Magic = 2


class AttackSubType(Enum):
    Unarmed = 0
    Weapon = 1
    Missile = 2


class DefenseType(Enum):
    Block = 0
    Dodge = 1
    Deflect = 2


class TargetType(Enum):
    Single = 0
    Cone = 1
    Radius = 2
    Beam = 3
    Missile = 4
