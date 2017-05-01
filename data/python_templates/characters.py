from characters.character import Character
from components.display import Display
from components.stats import make_character_stats
from components.outfitter import Outfitter
from data.python_templates.classes import thief_class, warrior_class
from data.python_templates.races import human_race, orc_race, troll_race
from data.python_templates.body import humanoid_body
from util.colors import Colors


weak_orc = Character(
    uid="weak_orc",
    name="Weak Orc",
    character_class=warrior_class,
    character_race=orc_race,
    stats=make_character_stats(health=10),
    display=Display(Colors.ORC_GREEN, Colors.BLACK_COLOR, "O"),
    body=humanoid_body.copy(),
)
strong_orc = Character(
    uid="strong_orc",
    name="Strong Orc",
    character_class=warrior_class,
    character_race=orc_race,
    stats=make_character_stats(health=16, strength=12, constitution=12),
    display=Display(Colors.ORC_GREEN, Colors.BLACK_COLOR, "O"),
    body=humanoid_body.copy(),
)
weak_troll = Character(
    uid="weak_troll",
    name="Weak Troll",
    character_class=warrior_class,
    character_race=troll_race,
    stats=make_character_stats(health=24, strength=14, constitution=14),
    display=Display(Colors.TROLL_GREEN, Colors.BLACK_COLOR, "O"),
    body=humanoid_body.copy(),
)
human_warrior = Character(
    uid="human_warrior",
    name="Human Warrior",
    character_class=warrior_class,
    character_race=human_race,
    stats=make_character_stats(health=10, strength=12, constitution=12, dexterity=10),
    display=Display(Colors.WHITE_COLOR, Colors.BLACK_COLOR, "O"),
    body=humanoid_body.copy(),
)
human_warrior.register_component(Outfitter('starter_warrior'))
human_thief = Character(
    uid="human_thief",
    name="Human Thief",
    character_class=thief_class,
    character_race=human_race,
    stats=make_character_stats(health=6, constitution=10, dexterity=16),
    display=Display(Colors.WHITE_COLOR, Colors.BLACK_COLOR, "O"),
    body=humanoid_body.copy(),
)
human_thief.register_component(Outfitter('starter_thief'))


character_templates = {
    weak_orc.uid: weak_orc,
    strong_orc.uid: strong_orc,
    weak_troll.uid: weak_troll,
    human_warrior.uid: human_warrior,
    human_thief.uid: human_thief
}
