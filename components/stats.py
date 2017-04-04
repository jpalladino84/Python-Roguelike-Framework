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
    def __init__(self, health=1, mana=1, strength=8, dexterity=8, constitution=8,
                 intelligence=8, charisma=8, wisdom=8, size=5, **kwargs):
        self.health = Stat(Stats.Health, int(health), int(health))
        self.mana = Stat(Stats.Mana, int(mana), int(mana))
        self.strength = Stat(Stats.Strength, int(strength), int(strength))
        self.dexterity = Stat(Stats.Dexterity, int(dexterity), int(dexterity))
        self.constitution = Stat(Stats.Constitution, int(constitution), int(constitution))
        self.intelligence = Stat(Stats.Intelligence, int(intelligence), int(intelligence))
        self.charisma = Stat(Stats.Charisma, int(charisma), int(charisma))
        self.wisdom = Stat(Stats.Wisdom, int(wisdom), int(wisdom))
        self.size = size

    def get_stat(self, stat):
        if isinstance(stat, Stat):
            return self.__dict__[stat.uid]

        if isinstance(stat, Stats):
            return self.__dict__[stat.value]

        return self.__dict__[stat]


class ItemStats(object):
    def __init__(self, health=0, mana=0, sharpness=0, hardness=0,
                 weight=0, size=0, potency=0, damage_dice_amount=1, min_damage=0, max_damage=0):
        self.health = Stat(Stats.Health, health, health)
        self.mana = Stat(Stats.Mana, mana, mana)
        self.sharpness = Stat(Stats.Sharpness, sharpness, sharpness)
        self.hardness = Stat(Stats.Hardness, hardness, hardness)
        self.weight = Stat(Stats.Weight, weight, weight)
        self.size = Stat(Stats.Size, size, size)
        self.potency = Stat(Stats.Potency, potency, potency)
        self.damage_dice_amount = damage_dice_amount
        self.min_damage = Stat(Stats.MinDamage, min_damage, min_damage)
        self.max_damage = Stat(Stats.MaxDamage, max_damage, max_damage)

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
    MaxDamage = 'max_damage'
    MinDamage = 'min_damage'
    ArmorClass = 'armor_class'


class Size:
    Fine = 0
    Diminutive = 1
    Tiny = 2
    Small = 3
    Medium = 4
    Large = 5
    Huge = 6
    Gargantuan = 7
    Colossal = 8



