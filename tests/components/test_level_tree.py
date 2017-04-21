import unittest

from abilities.ability import Ability
from abilities.power_abilities import PowerAbilities

from abilities.physical_abilities import PhysicalAbilities
from components.level_tree import LevelTree
from stats.enums import StatsEnum
from stats.stat import StatModifier


class LevelTreeTestCase(unittest.TestCase):

    def test_stats_modifiers(self):
        test_tree = LevelTree()
        test_tree.stats_modifiers = {
            1: [StatModifier(StatsEnum.Health, 1, level_progression=1),
                StatModifier(StatsEnum.Charisma, -1, level_progression=2)],
            2: [StatModifier(StatsEnum.Dexterity, 1)]
        }
        modifiers = test_tree.get_stat_modifiers(8)
        self.assertEqual(modifiers[StatsEnum.Health], 7)
        self.assertEqual(modifiers[StatsEnum.Dexterity], 1)
        self.assertEqual(modifiers[StatsEnum.Charisma], 3)

    def test_ability_modifiers(self):
        test_tree = LevelTree()
        test_tree.abilities_modifiers = {
            1: [
                Ability(PhysicalAbilities.BITE, 1),
                Ability(PowerAbilities.Berserk, 1, level_progression=1),
                Ability(PowerAbilities.Regeneration, 1, level_progression=10)
            ]
        }
        modifiers = test_tree.get_ability_modifiers(12)
        self.assertEqual(modifiers[PhysicalAbilities.BITE], 1)
        self.assertEqual(modifiers[PhysicalAbilities.Berserk], 11)
        self.assertEqual(modifiers[PhysicalAbilities.Regeneration], 2)
