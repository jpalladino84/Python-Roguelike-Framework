from characters.outfit import Outfit
from data.python_templates import items


def starter_warrior():
    outfit = Outfit(
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
