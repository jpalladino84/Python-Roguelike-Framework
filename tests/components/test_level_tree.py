from abilities.ability import Ability
from abilities.power_abilities import PowerAbilities

from abilities.physical_abilities import PhysicalAbilities
from components.level_tree import LevelTree
from components.stats import Stats, StatModifier


def test_stats_modifiers():
    test_tree = LevelTree()
    test_tree.stats_modifiers = {
        1: [StatModifier(Stats.Health, 1, level_progression=1),
            StatModifier(Stats.Charisma, -1, level_progression=2)],
        2: [StatModifier(Stats.Dexterity, 1)]
    }
    modifiers = test_tree.get_stat_modifiers(8)
    assert modifiers[Stats.Health] == 7
    assert modifiers[Stats.Dexterity] == 1
    assert modifiers[Stats.Charisma] == -3


def test_ability_modifiers():
    test_tree = LevelTree()
    test_tree.abilities_modifiers = {
        1: [
            Ability(PhysicalAbilities.BITE, 1),
            Ability(PowerAbilities.Berserk, 1, level_progression=1),
            Ability(PowerAbilities.Regeneration, 1, level_progression=10)
        ]
    }
    modifiers = test_tree.get_ability_modifiers(12)
    assert modifiers[PhysicalAbilities.BITE] == 1
    assert modifiers[PowerAbilities.Berserk] == 11
    assert modifiers[PowerAbilities.Regeneration] == 2
