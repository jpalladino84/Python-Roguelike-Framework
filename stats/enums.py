from enum import Enum


class StatsEnum(Enum):
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