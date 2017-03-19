from enum import Enum
from abc import abstractmethod

# Anything should be able to have a requirement and validate it.


class CompareType(Enum):
    LessThan = 0
    LessOrEqual = 1
    Equal = 2
    GreaterOrEqual = 3
    Greater = 4


class RequirementType(Enum):
    StatRequirement = 0
    ItemRequirement = 1
    LevelRequirement = 2
    PhysicalAbilityRequirement = 3
    ItemDamageTypeRequirement = 4


class Requirement(object):
    def __init__(self, requirement_type, compare_type, key, value):
        self.requirement_type = requirement_type
        self.compare_type = compare_type
        self.key = key
        self.value = value

    @abstractmethod
    def evaluate(self, game_object):
        pass

    @staticmethod
    def compare(compare_type, value, other_value):
        if compare_type == CompareType.LessThan:
            if other_value < value:
                return True
        elif compare_type == CompareType.LessOrEqual:
            if other_value <= value:
                return True
        elif compare_type == CompareType.Equal:
            if other_value == value:
                return True
        elif compare_type == CompareType.GreaterOrEqual:
            if other_value >= value:
                return True
        elif compare_type == CompareType.Greater:
            if other_value > value:
                return True

        return False


class StatRequirement(Requirement):
    def __init__(self, compare_type, value, stat):
        super(StatRequirement, self).__init__(RequirementType.StatRequirement, compare_type, key=stat, value=value)

    def evaluate(self, game_object):
        if hasattr(game_object, 'stats'):
            return self.compare(self.compare_type, self.value, getattr(game_object.stats, self.key))
        return False


class PhysicalAbilityRequirement(Requirement):
    def __init__(self, compare_type, value, ability_enum):
        super(PhysicalAbilityRequirement, self).__init__(RequirementType.StatRequirement, compare_type, key=ability_enum, value=value)

    def evaluate(self, game_object):
        if hasattr(game_object, 'body'):
            abilities = game_object.body.get_physical_abilities()
            return self.compare(self.compare_type, self.value, abilities.get(self.key, 0))
        return False


class ItemDamageTypeRequirement(Requirement):
    def __init__(self, compare_type, damage_type_enum):
        super(ItemDamageTypeRequirement, self).__init__(RequirementType.StatRequirement, compare_type, key=damage_type_enum, value=damage_type_enum)

    def evaluate(self, game_object):
        if hasattr(game_object, 'equipment'):
            weapons = game_object.equipment.get_wielded_items()
            for weapon in weapons:
                if self.compare(self.compare_type, self.value, weapon.melee_damage_type):
                    return True
        return False
