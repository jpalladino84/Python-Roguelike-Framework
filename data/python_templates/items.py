import data.python_templates.material
from combat.enums import DamageType
from components.armor import Armor
from components.weapon import Weapon
from components.display import Display
from components.stats import ItemStats, Size
from items.item import ItemTemplate
from items import enums as item_enums
from util.colors import Colors
from util.dice import Dice, DiceStack


def build_short_sword():
    _short_sword = ItemTemplate(
        uid="short_sword",
        name="Short Sword",
        description="A short sword.",
        display=Display(Colors.DARK_GRAY, Colors.BLACK_COLOR, "!"),
        material_uid=data.python_templates.material.Iron.uid,
        base_stats=ItemStats(health=1, size=Size.Medium, damage_dice_amount=1, min_damage=1, max_damage=6),
        melee_damage_type=DamageType.Pierce
    )
    _short_sword.register_component(
        Weapon(weapon_category=item_enums.WeaponCategory.Martial, weapon_type=item_enums.WeaponType.Melee,
               size=Size.Small, melee_damage_type=DamageType.Pierce, damage_dice=DiceStack(1, Dice(6)))
    )

    return _short_sword


def build_helmet():
    _helmet = ItemTemplate(
        uid="helmet",
        name="Helmet",
        description="A helmet.",
        display=Display(Colors.DARK_GRAY, Colors.BLACK_COLOR, "!"),
        material_uid=data.python_templates.material.Iron.uid,
        base_stats=ItemStats(health=10, size=Size.Medium),

    )
    _helmet.register_component(
        Armor(
            base_armor_class=1,
            armor_category=item_enums.ArmorCategory.Medium,
            wearable_body_parts_uid=["humanoid_head"],
            worn_layer=item_enums.WornLayer.Outer
        )
    )

    return _helmet

short_sword = build_short_sword()
helmet = build_helmet()

item_templates = {
    short_sword.uid: short_sword,
    helmet.uid: helmet,
}
