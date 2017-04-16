from characters.outfit import Outfit
from data.python_templates import items


def build_starter_warrior():
    return Outfit(
        "starter_warrior",
        items_worn=[
            items.helmet,
            items.breastplate,
            items.bracer,
            items.bracer,
            items.gauntlet,
            items.gauntlet,
            items.greave,
            items.greave,
            items.boot,
            items.boot,
        ],
        items_held=[
            items.longsword
        ]
    )

starter_warrior = build_starter_warrior()
outfits = [starter_warrior]
