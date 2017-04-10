from abilities.physical_abilities import PhysicalAbilities
from combat.attack import UnarmedAttackTemplate, MeleeAttackTemplate
from combat.enums import DamageType
from util import requirements


# TODO The melee damage type is repeated.. change that. (Variable AND in requirement)
# TODO Also use the requirements to fetch... requirements... like required bodypart. (Requirement!!)


punch_template = UnarmedAttackTemplate(
    name="Punch",
    description="The mighty fist is presented to the weak flesh.",
    message="{attacker} throws {attacker_his} fist at {defender}",
    requirements=[
        requirements.PhysicalAbilityRequirement(requirements.CompareType.GreaterOrEqual, 1, PhysicalAbilities.PUNCH)]
)
slash_template = MeleeAttackTemplate(
    name="Slash",
    description="The sharpened blade parts the flesh.",
    message="{attacker} slashes {attacker_weapon} at {defender}",
    required_item_melee_damage_type=DamageType.Slash,
    requirements=[requirements.ItemDamageTypeRequirement(requirements.CompareType.Equal, DamageType.Slash)]
)
smash_template = MeleeAttackTemplate(
    name="Smash",
    description="The hardened metal crushes the bone.",
    message="{attacker} smashes {attacker_weapon} at {defender}",
    required_item_melee_damage_type=DamageType.Blunt,
    requirements=[requirements.ItemDamageTypeRequirement(requirements.CompareType.Equal, DamageType.Blunt)]
)
stab_template = MeleeAttackTemplate(
    name="Stab",
    description="The point pierces the veil.",
    message="{attacker} stabs {attacker_weapon} at {defender}",
    required_item_melee_damage_type=DamageType.Pierce,
    requirements=[requirements.ItemDamageTypeRequirement(requirements.CompareType.Equal, DamageType.Pierce)]
)
base_attacks = [punch_template, slash_template, smash_template, stab_template]