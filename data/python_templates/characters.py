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
    stats=make_character_stats(health=4, strength=8),
    display=Display(Colors.ORC_GREEN, Colors.BLACK_COLOR, "O"),
    body=humanoid_body.copy(),
)
weak_orc.xp_value = 25

strong_orc = Character(
    uid="strong_orc",
    name="Strong Orc",
    character_class=warrior_class,
    character_race=orc_race,
    stats=make_character_stats(health=7, strength=10, constitution=10),
    display=Display(Colors.ORC_GREEN, Colors.BLACK_COLOR, "O"),
    body=humanoid_body.copy(),
)
strong_orc.xp_value = 50

weak_troll = Character(
    uid="weak_troll",
    name="Weak Troll",
    character_class=warrior_class,
    character_race=troll_race,
    stats=make_character_stats(health=12, strength=12, constitution=10),
    display=Display(Colors.TROLL_GREEN, Colors.BLACK_COLOR, "O"),
    body=humanoid_body.copy(),
)
weak_troll.xp_value = 100

skeleton_warrior = Character(
    uid="skeleton_warrior",
    name="Skeleton Warrior",
    character_class=warrior_class,
    character_race=human_race,
    stats=make_character_stats(health=6, strength=10, constitution=10, dexterity=10),
    display=Display(Colors.WHITE_COLOR, Colors.BLACK_COLOR, "s"),
    body=humanoid_body.copy(),
)
skeleton_warrior.register_component(Outfitter('starter_warrior'))
skeleton_warrior.xp_value = 50

goblin_thief = Character(
    uid="goblin_thief",
    name="Goblin Thief",
    character_class=thief_class,
    character_race=human_race,
    stats=make_character_stats(health=4, constitution=8, dexterity=12),
    display=Display(Colors.ORC_GREEN, Colors.BLACK_COLOR, "g"),
    body=humanoid_body.copy(),
)
goblin_thief.register_component(Outfitter('starter_thief'))
goblin_thief.xp_value = 25


character_templates = {
    weak_orc.uid: weak_orc,
    strong_orc.uid: strong_orc,
    weak_troll.uid: weak_troll,
    skeleton_warrior.uid: skeleton_warrior,
    goblin_thief.uid: goblin_thief
}
