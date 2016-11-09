from components.level_tree import LevelTree
from components.stats import Stats, StatModifier
from components.body import get_humanoid_body_sample
from components.abilities.physical_abilities import PhysicalAbilities
from components.abilities.power_abilities import PowerAbilities
from components.abilities.ability import Ability


class Race(object):
    """
    Racial characteristics and bonuses
    """
    def __init__(self, uid, name, level_tree, body_template_uid, experience_penalty=0):
        self.uid = uid
        self.name = name
        self.level_tree = level_tree
        self.body_template_uid = body_template_uid
        self.experience_penalty = experience_penalty


class MetaRace(Race):
    """
    Pretty much the same as a race but is more like a modifier itself.
    """
    def __init__(self, uid, name, level_tree, body_modifier_template_uid):
        super().__init__(uid, name, level_tree, None)
        self.body_modifier_template_uid = body_modifier_template_uid

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
    orc_level_tree.abilities_modifiers = {
        1: [Ability(PowerAbilities.Berserk, 1)]
    }
    orc_race = Race("orc", "Orc", orc_level_tree, humanoid_body.uid)
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
    troll_race = Race("troll", "Troll", troll_level_tree, humanoid_body.uid)
    human_level_tree = LevelTree()
    human_race = Race("human", "Human", human_level_tree, humanoid_body.uid)

    return [orc_race, troll_race, human_race]
