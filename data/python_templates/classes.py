from abilities.ability import Ability
from abilities.power_abilities import PowerAbilities
from components.character_class import CharacterClass
from components.level_tree import LevelTree
from stats.enums import StatsEnum
from stats.stat import StatModifier


def build_warrior_class():
    warrior_level_tree = LevelTree()
    warrior_level_tree.add_stat_modifier(0, StatModifier(StatsEnum.Health, 10, level_progression=1))
    warrior_level_tree.add_ability_modifier(2, Ability(PowerAbilities.PowerAttack, 1, level_progression=2))
    warrior_level_tree.add_ability_modifier(4, Ability(PowerAbilities.Parry, 1, level_progression=4))

    return CharacterClass('warrior', 'Warrior', warrior_level_tree)


def build_thief_class():
    thief_level_tree = LevelTree()
    thief_level_tree.add_stat_modifier(0, StatModifier(StatsEnum.Health, 6, level_progression=1))
    thief_level_tree.add_ability_modifier(2, Ability(PowerAbilities.Sneak, 1, level_progression=2))
    thief_level_tree.add_ability_modifier(4, Ability(PowerAbilities.Backstab, 1, level_progression=4))

    return CharacterClass('thief', 'Thief', thief_level_tree)


warrior_class = build_warrior_class()
thief_class = build_thief_class()

character_class_templates = {
    warrior_class.uid: warrior_class,
    thief_class.uid: thief_class
}
