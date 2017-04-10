from combat.defense import DodgeTemplate, ParryTemplate, BlockTemplate, ArmorAbsorbTemplate, MissTemplate

dodge = DodgeTemplate(
    name="Dodge",
    description="Standard move out of the way.",
    message="but {defender} dodges it.",
)
parry = ParryTemplate(
    name="Parry",
    description="Standard parry weapon with weapon.",
    message="but {defender} parries it with {defender_his} {defender_weapon} !"
)
block = BlockTemplate(
    name="Block",
    description="Standard block something with something.",
    message="but {defender} blocks it with {defender_his} {defender_weapon}"
)
armor_absorb = ArmorAbsorbTemplate(
    name="Armor Absorb",
    description="Standard armor saves your ass.",
    message="but the hit is absorbed by {defender_bodypart_armor}"
)
miss = MissTemplate(
    name="Miss",
    description="Action falls short of the will.",
    message="but {attacker_he} misses {defender}"
)
base_defenses = [
    dodge, parry, block, armor_absorb, miss
]