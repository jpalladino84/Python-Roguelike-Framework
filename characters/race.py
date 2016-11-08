from components.level_tree import LevelTree
from components.stats import Stats, StatModifier
from components.body import get_humanoid_body_sample


class Race(object):
    """
    Racial characteristics and bonuses
    """
    def __init__(self, uid, name, level_tree, body_template):
        self.uid = uid
        self.name = name
        self.level_tree = level_tree
        self.body_template = body_template


class MetaRace(Race):
    """
    Pretty much the same as a race but is more like a modifier itself.
    """
    def __init__(self, uid, name, level_tree, body_modifier_template):
        super().__init__(uid, name, level_tree, None)
        self.body_modifier_template = body_modifier_template

# TODO Move this OUT


def get_race_samples():
    # An orc won't get uglier over time but it could gain abilities.
    humanoid_body = get_humanoid_body_sample()
    orc_level_tree = LevelTree()
    orc_level_tree.stats_modifiers = {
        1: [
            StatModifier(Stats.Strength, 2),
            StatModifier(Stats.Constitution, 2),
            StatModifier(Stats.Charisma, -2),
            StatModifier(Stats.Intelligence, -2)
        ]
    }
    orc_race = Race("orc", "Orc", orc_level_tree, humanoid_body)
    troll_level_tree = LevelTree()
    troll_level_tree.stats_modifiers = {
        1: [
            StatModifier(Stats.Strength, 4),
            StatModifier(Stats.Constitution, 4),
            StatModifier(Stats.Charisma, -4),
            StatModifier(Stats.Intelligence, -4)
        ]
    }
    troll_race = Race("troll", "Troll", troll_level_tree, humanoid_body)
    human_level_tree = LevelTree()
    human_race = Race("human", "Human", human_level_tree, humanoid_body)

    return [orc_race, troll_race, human_race]
