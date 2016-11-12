from components.level_tree import LevelTree
from components.stats import Stats, StatModifier
from components.abilities.physical_abilities import PhysicalAbilities
from components.abilities.power_abilities import PowerAbilities
from components.abilities.ability import Ability


class CharacterClass(object):
    def __init__(self, uid, name, level_tree, experience_penalty=0):
        self.uid = uid
        self.name = name
        self.level_tree = level_tree
        self.experience_penalty = experience_penalty


def get_sample_classes():
    warrior_level_tree = LevelTree()
    warrior_level_tree.add_stat_modifier(0, StatModifier(Stats.Health, 10, level_progression=1))
    warrior_level_tree.add_ability_modifier(2, Ability(PowerAbilities.PowerAttack, 1, level_progression=2))
    warrior_level_tree.add_ability_modifier(4, Ability(PowerAbilities.Parry, 1, level_progression=4))
    warrior = CharacterClass('warrior', 'Warrior', warrior_level_tree)

    thief_level_tree = LevelTree()
    thief_level_tree.add_stat_modifier(0, StatModifier(Stats.Health, 6, level_progression=1))
    thief_level_tree.add_ability_modifier(2, Ability(PowerAbilities.Sneak, 1, level_progression=2))
    thief_level_tree.add_ability_modifier(4, Ability(PowerAbilities.Backstab, 1, level_progression=4))
    thief = CharacterClass('thief', 'Thief', thief_level_tree)

    return [warrior, thief]
