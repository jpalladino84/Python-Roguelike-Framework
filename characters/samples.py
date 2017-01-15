from .race import Race
from components.level_tree import LevelTree
from components.stats import Stats, StatModifier, CharacterStats
from components.abilities.power_abilities import PowerAbilities
from components.abilities.ability import Ability
from components.display import Display
from components.colors import Colors
from .classes import CharacterClass
from .character import CharacterTemplate
from ..items.item import ItemTemplate, DamageType
from components.stats import ItemStats, Size
from components import material


def get_race_samples():
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
    human_level_tree = LevelTree()
    human_race = Race("human", "Human", human_level_tree, "humanoid")

    return [orc_race, troll_race, human_race]


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


def get_sample_monsters():
    sample_races = get_race_samples()
    sample_classes = get_sample_classes()
    weak_orc = CharacterTemplate(
        uid="weak_orc", name="Weak Orc",
        class_uid=sample_classes[0].uid,
        race_uid=sample_races[0].uid,
        base_stats=CharacterStats(health=10),
        display=Display(Colors.ORC_GREEN, Colors.BLACK_COLOR, "O"),
        body_uid="humanoid",
        cumulative_level=0
    )
    strong_orc = CharacterTemplate(
        uid="strong_orc", name="Strong Orc",
        class_uid=sample_classes[0].uid,
        race_uid=sample_races[0].uid,
        base_stats=CharacterStats(health=16, strength=12, constitution=12),
        display=Display(Colors.ORC_GREEN, Colors.BLACK_COLOR, "O"),
        body_uid="humanoid",
        cumulative_level=2
    )
    weak_troll = CharacterTemplate(
        uid="weak_troll", name="Weak Troll",
        class_uid=sample_classes[0].uid,
        race_uid=sample_races[1].uid,
        base_stats=CharacterStats(health=24, strength=14, constitution=14),
        display=Display(Colors.TROLL_GREEN, Colors.BLACK_COLOR, "O"),
        body_uid="humanoid",
        cumulative_level=4
    )
    human_warrior = CharacterTemplate(
        uid="human_warrior", name="human_warrior",
        class_uid=sample_classes[0].uid,
        race_uid=sample_races[2].uid,
        base_stats=CharacterStats(health=10, strength=12, constitution=12, dexterity=10),
        display=Display(Colors.WHITE_COLOR, Colors.BLACK_COLOR, "O"),
        body_uid="humanoid",
        cumulative_level=0
    )
    human_thief = CharacterTemplate(
        uid="human_thief", name="human_thief",
        class_uid=sample_classes[1].uid,
        race_uid=sample_races[2].uid,
        base_stats=CharacterStats(health=6, constitution=10, dexterity=16),
        display=Display(Colors.WHITE_COLOR, Colors.BLACK_COLOR, "O"),
        body_uid="humanoid",
        cumulative_level=0
    )

    return [weak_orc, strong_orc, weak_troll, human_warrior, human_thief]


def get_sample_items():
    steel_sword = ItemTemplate(
        uid="short_sword",
        name="Short Sword",
        description="A short sword.",
        display=Display(Colors.DARK_GRAY, Colors.BLACK_COLOR, "!"),
        material_uid=material.Iron.uid,
        base_stats=ItemStats(health=1, size=Size.Medium, min_damage=1, max_damage=6),
        melee_damage_type=DamageType.Slash
    )
    helmet = ItemTemplate(
        uid="helmet",
        name="Helmet",
        description="A helmet.",
        display=Display(Colors.DARK_GRAY, Colors.BLACK_COLOR, "!"),
        material_uid=material.Iron.uid,
        base_stats=ItemStats(health=10, size=Size.Medium),
        wearable_bodyparts_uid=["humanoid_head"]
    )
    return [steel_sword, helmet]
