from combat.enums import DamageType
from components import material
from components.display import Display
from components.stats import ItemStats, Size
from items.item import ItemTemplate, WornLayer
from util.colors import Colors


def build_short_sword():
    short_sword = ItemTemplate(
        uid="short_sword",
        name="Short Sword",
        description="A short sword.",
        display=Display(Colors.DARK_GRAY, Colors.BLACK_COLOR, "!"),
        material_uid=material.Iron.uid,
        base_stats=ItemStats(health=1, size=Size.Medium, damage_dice_amount=1, min_damage=1, max_damage=6),
        melee_damage_type=DamageType.Pierce
    )

    return short_sword


def build_helmet():
    helmet = ItemTemplate(
        uid="helmet",
        name="Helmet",
        description="A helmet.",
        display=Display(Colors.DARK_GRAY, Colors.BLACK_COLOR, "!"),
        material_uid=material.Iron.uid,
        base_stats=ItemStats(health=10, size=Size.Medium),
        wearable_bodyparts_uid=["humanoid_head"],
        worn_layer=WornLayer.Outer
    )

    return helmet

short_sword = build_short_sword()
helmet = build_helmet()

items = [
    short_sword,
    helmet
]
