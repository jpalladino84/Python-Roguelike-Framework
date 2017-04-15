import data.python_templates.material
from combat.enums import DamageType
from components.armor import Armor
from components.weapon import Weapon
from components.display import Display
from components.stats import Stats
from stats.enums import Size
from items.item import Item
from items import enums as item_enums
from util.colors import Colors
from util.dice import Dice, DiceStack


def build_short_sword():
    _short_sword = Item(
        uid="short_sword",
        name="Short Sword",
        description="A short sword.",
        display=Display(Colors.DARK_GRAY, Colors.BLACK_COLOR, "!"),
    )
    _short_sword.register_component(data.python_templates.material.Iron.copy())
    _short_sword.register_component(Stats(health=1, size=Size.Medium))
    _short_sword.register_component(
        Weapon(weapon_category=item_enums.WeaponCategory.Martial, weapon_type=item_enums.WeaponType.Melee,
               size=Size.Small, melee_damage_type=DamageType.Pierce, damage_dice=DiceStack(1, Dice(6)))
    )

    return _short_sword


def build_long_sword():
    _long_sword = Item(
        uid="long_sword",
        name="Longsword",
        description="A longsword.",
        display=Display(Colors.DARK_GRAY, Colors.BLACK_COLOR, "!"),
    )
    _long_sword.register_component(data.python_templates.material.Iron.copy())
    _long_sword.register_component(Stats(health=1, size=Size.Medium))
    _long_sword.register_component(
        Weapon(weapon_category=item_enums.WeaponCategory.Martial, weapon_type=item_enums.WeaponType.Melee,
               size=Size.Medium, melee_damage_type=DamageType.Slash, damage_dice=DiceStack(1, Dice(8)))
    )

    return _long_sword


def build_helmet():
    _helmet = Item(
        uid="helmet",
        name="Helmet",
        description="A helmet.",
        display=Display(Colors.DARK_GRAY, Colors.BLACK_COLOR, "!"),
    )
    _helmet.register_component(data.python_templates.material.Iron.copy())
    _helmet.register_component(Stats(health=10, size=Size.Medium, weight=2))
    _helmet.register_component(
        Armor(
            base_armor_class=2,
            armor_category=item_enums.ArmorCategory.Medium,
            wearable_body_parts_uid=["humanoid_head"],
            worn_layer=item_enums.WornLayer.Outer
        )
    )

    return _helmet


def build_breastplate():
    _breastplate = Item(
        uid="breastplate",
        name="Breastplate",
        description="An iron breastplate..",
        display=Display(Colors.DARK_GRAY, Colors.BLACK_COLOR, "!"),
    )
    _breastplate.register_component(data.python_templates.material.Iron.copy())
    _breastplate.register_component(Stats(health=10, size=Size.Medium, weight=4))
    _breastplate.register_component(
        Armor(
            base_armor_class=4,
            armor_category=item_enums.ArmorCategory.Medium,
            wearable_body_parts_uid=["humanoid_torso"],
            worn_layer=item_enums.WornLayer.Outer,
            maximum_dexterity_bonus=2
        )
    )

    return _breastplate


def build_bracer():
    _bracers = Item(
        uid="bracer",
        name="Bracer",
        description="An iron bracer",
        display=Display(Colors.DARK_GRAY, Colors.BLACK_COLOR, "!"),
    )
    _bracers.register_component(data.python_templates.material.Iron.copy())
    _bracers.register_component(Stats(health=10, size=Size.Medium, weight=0.5))
    _bracers.register_component(
        Armor(
            base_armor_class=0.5,
            armor_category=item_enums.ArmorCategory.Medium,
            wearable_body_parts_uid=["humanoid_arm"],
            worn_layer=item_enums.WornLayer.Outer,
            maximum_dexterity_bonus=2
        )
    )

    return _bracers


def build_gauntlet():
    _gauntlet = Item(
        uid="gauntlet",
        name="Gauntlet",
        description="An iron gauntlet",
        display=Display(Colors.DARK_GRAY, Colors.BLACK_COLOR, "!"),
    )
    _gauntlet.register_component(data.python_templates.material.Iron.copy())
    _gauntlet.register_component(Stats(health=10, size=Size.Medium, weight=0.5))
    _gauntlet.register_component(
        Armor(
            base_armor_class=0.5,
            armor_category=item_enums.ArmorCategory.Medium,
            wearable_body_parts_uid=["humanoid_hand"],
            worn_layer=item_enums.WornLayer.Outer,
            maximum_dexterity_bonus=2
        )
    )

    return _gauntlet


def build_greave():
    _greave = Item(
        uid="greave",
        name="Greave",
        description="An iron greave",
        display=Display(Colors.DARK_GRAY, Colors.BLACK_COLOR, "!"),
    )
    _greave.register_component(data.python_templates.material.Iron.copy())
    _greave.register_component(Stats(health=10, size=Size.Medium, weight=0.5))
    _greave.register_component(
        Armor(
            base_armor_class=0.5,
            armor_category=item_enums.ArmorCategory.Medium,
            wearable_body_parts_uid=["humanoid_leg"],
            worn_layer=item_enums.WornLayer.Outer,
            maximum_dexterity_bonus=2
        )
    )

    return _greave


def build_boot():
    _boot = Item(
        uid="boot",
        name="Boot",
        description="An iron boot",
        display=Display(Colors.DARK_GRAY, Colors.BLACK_COLOR, "!"),
    )
    _boot.register_component(data.python_templates.material.Iron.copy())
    _boot.register_component(Stats(health=10, size=Size.Medium, weight=0.5))
    _boot.register_component(
        Armor(
            base_armor_class=0.5,
            armor_category=item_enums.ArmorCategory.Medium,
            wearable_body_parts_uid=["humanoid_foot"],
            worn_layer=item_enums.WornLayer.Outer,
            maximum_dexterity_bonus=2
        )
    )

    return _boot


short_sword = build_short_sword()
longsword = build_long_sword()

boot = build_boot()
bracer = build_bracer()
breastplate = build_breastplate()
gauntlet = build_gauntlet()
greave = build_greave()
helmet = build_helmet()

item_templates = {
    short_sword.uid: short_sword,
    longsword.uid: longsword,
    boot.uid: boot,
    bracer.uid: bracer,
    breastplate.uid: breastplate,
    gauntlet.uid: gauntlet,
    greave.uid: greave,
    helmet.uid: helmet,
}
