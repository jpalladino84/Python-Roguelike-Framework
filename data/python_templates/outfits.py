from characters.outfit import Outfit
from data.python_templates import items
from data.python_templates import material


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
            items.short_sword
        ]
    )


def build_starter_thief():
    leather_bracer_variant = items.bracer.copy()
    leather_bracer_variant.material = material.Leather.copy()
    leather_gauntlet_variant = items.gauntlet.copy()
    leather_gauntlet_variant.material = material.Leather.copy()
    leather_boot_variant = items.boot.copy()
    leather_boot_variant.material = material.Leather.copy()
    return Outfit(
        "starter_thief",
        items_worn=[
            items.leather_hood,
            items.leather_cuirass,
            leather_bracer_variant,
            leather_bracer_variant,
            leather_gauntlet_variant,
            leather_gauntlet_variant.copy(),
            items.leather_pants,
            leather_boot_variant,
            leather_boot_variant.copy(),
        ],
        items_held=[
            items.short_sword
        ]
    )

starter_warrior = build_starter_warrior()
starter_thief = build_starter_thief()
outfits = [starter_warrior, starter_thief]
