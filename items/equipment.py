from enum import Enum


class EquipmentUsage(Enum):
    """
    How is the equipment used.
    Bound items fuse with the bodypart and may only be dispelled off.
    """
    Worn = 0
    Held = 1
    Bound = 2
