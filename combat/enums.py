from enum import Enum


class TargetType(Enum):
    Single = 0
    Cone = 1
    Radius = 2
    Beam = 3
    Missile = 4


class DamageType(Enum):
    Blunt = 0
    Slash = 1
    Pierce = 2


class ThreatLevel(Enum):
    Minor = 0
    Major = 1
    Critical = 2
    Fatal = 3
