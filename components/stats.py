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


class Stats(Enum):
    Health = 'health'
    Mana = 'mana'
    Strength = 'strength'
    Dexterity = 'dexterity'
    Constitution = 'constitution'
    Intelligence = 'intelligence'
    Charisma = 'charisma'
    Wisdom = 'wisdom'


