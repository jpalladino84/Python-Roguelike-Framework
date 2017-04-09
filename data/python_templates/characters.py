from characters.character import CharacterTemplate
from components.display import Display
from components.stats import CharacterStats
from data.python_templates.classes import thief_class, warrior_class
from data.python_templates.races import human_race, orc_race, troll_race
from util.colors import Colors


weak_orc = CharacterTemplate(
        uid="weak_orc", name="Weak Orc",
        class_uid=warrior_class.uid,
        race_uid=orc_race.uid,
        base_stats=CharacterStats(health=10),
        display=Display(Colors.ORC_GREEN, Colors.BLACK_COLOR, "O"),
        body_uid="humanoid",
        cumulative_level=0
    )

strong_orc = CharacterTemplate(
        uid="strong_orc", name="Strong Orc",
        class_uid=warrior_class.uid,
        race_uid=orc_race.uid,
        base_stats=CharacterStats(health=16, strength=12, constitution=12),
        display=Display(Colors.ORC_GREEN, Colors.BLACK_COLOR, "O"),
        body_uid="humanoid",
        cumulative_level=2
    )

weak_troll = CharacterTemplate(
        uid="weak_troll", name="Weak Troll",
        class_uid=warrior_class.uid,
        race_uid=troll_race.uid,
        base_stats=CharacterStats(health=24, strength=14, constitution=14),
        display=Display(Colors.TROLL_GREEN, Colors.BLACK_COLOR, "O"),
        body_uid="humanoid",
        cumulative_level=4
    )

human_warrior = CharacterTemplate(
        uid="human_warrior", name="Human Warrior",
        class_uid=warrior_class.uid,
        race_uid=human_race.uid,
        base_stats=CharacterStats(health=10, strength=12, constitution=12, dexterity=10),
        display=Display(Colors.WHITE_COLOR, Colors.BLACK_COLOR, "O"),
        body_uid="humanoid",
        cumulative_level=0
    )

human_thief = CharacterTemplate(
        uid="human_thief", name="Human Thief",
        class_uid=human_race.uid,
        race_uid=thief_class.uid,
        base_stats=CharacterStats(health=6, constitution=10, dexterity=16),
        display=Display(Colors.WHITE_COLOR, Colors.BLACK_COLOR, "O"),
        body_uid="humanoid",
        cumulative_level=0
    )


character_templates = {
    weak_orc.uid: weak_orc,
    strong_orc.uid: strong_orc,
    weak_troll.uid: weak_troll,
    human_warrior.uid: human_warrior,
    human_thief.uid: human_thief
}
