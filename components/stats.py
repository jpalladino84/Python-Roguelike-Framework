from enum import Enum
import math


class Stat(object):
    def __init__(self, uid, current, maximum):
        self.uid = uid
        self.current = current
        self.maximum = maximum

    def __str__(self):
        return str(self.current)

    def __int__(self):
        return int(self.current)

    def modify_current(self, value):
        self.current += value

    def modify_max(self, value):
        self.maximum += value


class StatModifier(object):
    def __init__(self, uid, value, level_progression=0):
        self.uid = uid
        self.value = value
        self.level_progression = level_progression

    def __int__(self):
        return

    def get_leveled_value(self, level, initial_level):
        if self.level_progression > 0:
            multiplier = (level - initial_level) / self.level_progression
            return math.ceil(self.value * multiplier)
        else:
            return self.value


# TODO I'm not sure we want classes for stats, maybe just use this to assign proper stats to an object instead?
class CharacterStats(object):
    def __init__(self, health=1, mana=1, strength=8, dexterity=8, constitution=8, intelligence=8, charisma=8, wisdom=8, **kwargs):
        self.health = Stat(Stats.Health, health, health)
        self.mana = Stat(Stats.Mana, mana, mana)
        self.strength = Stat(Stats.Strength, strength, strength)
        self.dexterity = Stat(Stats.Dexterity, dexterity, dexterity)
        self.constitution = Stat(Stats.Constitution, constitution, constitution)
        self.intelligence = Stat(Stats.Intelligence, intelligence, intelligence)
        self.charisma = Stat(Stats.Charisma, charisma, charisma)
        self.wisdom = Stat(Stats.Wisdom, wisdom, wisdom)


class ItemStats(object):
    def __init__(self, health=0, mana=0, sharpness=0, hardness=0, weight=0, size=0, potency=0):
        self.health = Stat(Stats.Health, health, health)
        self.mana = Stat(Stats.Mana, mana, mana)
        self.sharpness = Stat(Stats.Sharpness, sharpness, sharpness)
        self.hardness = Stat(Stats.Hardness, hardness, hardness)
        self.weight = Stat(Stats.Weight, weight, weight)
        self.size = Stat(Stats.Size, size, size)
        self.potency = Stat(Stats.Potency, potency, potency)

    def __eq__(self, other):
        return (
            self.health == other.health
            and self.mana == other.mana
            and self.sharpness == other.sharpness
            and self.hardness == other.hardness
            and self.weight == other.weight
            and self.size == other.size
            and self.potency == other.potency
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(
            (
                self.health,
                self.mana,
                self.sharpness,
                self.hardness,
                self.weight,
                self.size,
                self.potency,
            )
        )


class Stats(Enum):
    Health = 'health'
    Mana = 'mana'
    Strength = 'strength'
    Dexterity = 'dexterity'
    Constitution = 'constitution'
    Intelligence = 'intelligence'
    Charisma = 'charisma'
    Wisdom = 'wisdom'
    Sharpness = 'sharpness'
    Hardness = 'hardness'
    Weight = 'weight'
    Size = 'size'
    Potency = 'potency'


