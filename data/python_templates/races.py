from abilities.ability import Ability
from abilities.power_abilities import PowerAbilities
from characters.race import Race
from components.level_tree import LevelTree
from components.stats import StatModifier, Stats


def build_orc_race():
    # An orc won't get uglier over time but it could gain abilities.
    orc_level_tree = LevelTree()
    orc_level_tree.stats_modifiers = {
        1: [
            StatModifier(Stats.Strength, 2),
            StatModifier(Stats.Constitution, 2),
            StatModifier(Stats.Charisma, -2),
            StatModifier(Stats.Intelligence, -2)
        ]
    }
    orc_level_tree.abilities_modifiers = {
        1: [Ability(PowerAbilities.Berserk, 1)]
    }
    orc_race = Race("orc", "Orc", orc_level_tree, "humanoid")

    return orc_race


def build_troll_race():
    troll_level_tree = LevelTree()
    troll_level_tree.stats_modifiers = {
        1: [
            StatModifier(Stats.Strength, 4),
            StatModifier(Stats.Constitution, 4),
            StatModifier(Stats.Charisma, -4),
            StatModifier(Stats.Intelligence, -4)
        ]
    }
    troll_level_tree.abilities_modifiers = {
        1: [Ability(PowerAbilities.Regeneration, 1)]
    }
    troll_race = Race("troll", "Troll", troll_level_tree, "humanoid")

    return troll_race


def build_human_race():
    human_level_tree = LevelTree()
    human_race = Race("human", "Human", human_level_tree, "humanoid")

    return human_race

human_race = build_human_race()
orc_race = build_orc_race()
troll_race = build_troll_race()

races = [
    human_race,
    orc_race,
    troll_race
]
