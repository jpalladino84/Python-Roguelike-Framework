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


def build_helmet():
    _helmet = Item(
        uid="helmet",
        name="Helmet",
        description="A helmet.",
        display=Display(Colors.DARK_GRAY, Colors.BLACK_COLOR, "!"),
    )
    _helmet.register_component(data.python_templates.material.Iron.copy())
    _helmet.register_component(Stats(health=10, size=Size.Medium))
    _helmet.register_component(
        Armor(
            base_armor_class=1,
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
    _breastplate.register_component(Stats(health=10, size=Size.Medium))
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


short_sword = build_short_sword()
helmet = build_helmet()
breastplate = build_breastplate()

item_templates = {
    short_sword.uid: short_sword,
    helmet.uid: helmet,
    breastplate.uid: breastplate
}
