from components.level_tree import LevelTree
from components.stats import Stats, StatModifier


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
