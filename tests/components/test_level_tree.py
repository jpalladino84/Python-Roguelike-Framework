from components.level_tree import LevelTree
from components.stats import Stats, StatModifier
from components.abilities.ability import Ability
from components.abilities.power_abilities import PowerAbilities
from components.abilities.physical_abilities import PhysicalAbilities


def test_stats_modifiers():
    test_tree = LevelTree()
    test_tree.stats_modifiers = {
        1: [StatModifier(Stats.Health, 1), StatModifier(Stats.Charisma, -1)],
        2: [StatModifier(Stats.Health, 1), StatModifier(Stats.Dexterity, 1)],
        3: [StatModifier(Stats.Health, 1), StatModifier(Stats.Charisma, -1)]
    }
    modifiers = test_tree.get_stat_modifiers(3)
    assert modifiers[Stats.Health] == 3
    assert modifiers[Stats.Dexterity] == 1
    assert modifiers[Stats.Charisma] == -2


def test_ability_modifiers():
    test_tree = LevelTree()
    test_tree.abilities_modifiers = {
        1: [
            Ability(PhysicalAbilities.BITE, 1),
            Ability(PowerAbilities.Berserk, 1),
            Ability(PowerAbilities.Regeneration, 1)
        ],
        2: [
            Ability(PhysicalAbilities.BITE, -1),
            Ability(PowerAbilities.Berserk, 1)
        ]
    }
    modifiers = test_tree.get_ability_modifiers(3)
    assert modifiers[PhysicalAbilities.BITE] == 0
    assert modifiers[PowerAbilities.Berserk] == 2
    assert modifiers[PowerAbilities.Regeneration] == 1
