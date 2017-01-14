from enum import Enum


class Equipment(object):
    """
    This is given to whatever can be worn.
    It could hold additional effects that are only given when worn or held.
    """
    def __init__(self, compatible_bodyparts_uid=None, usage=EquipmentUsage.Worn):
        self.compatible_bodyparts_uid = compatible_bodyparts_uid
        self.usage = usage


class EquipmentUsage(Enum):
    """
    How is the equipment used.
    Bound items fuse with the bodypart and may only be dispelled off.
    """
    Worn = 0
    Held = 1
    Bound = 2
