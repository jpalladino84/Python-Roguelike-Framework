from . import enums
from managers import echo
from components.stats import Stats
from components import requirements
from components.abilities.physical_abilities import PhysicalAbilities
from items.item import DamageType


class AttackTemplate(object):
    def __init__(self, name, description="", message, attack_type,
                 attack_sub_type, target_type, attack_range,
                 modifiers, hit_stat_used, damage_stat_used, requisites=None):
        self.name = name
        self.description = description
        self.message = message
        self.attack_type = attack_type
        self.attack_sub_type = attack_sub_type
        self.target_type = target_type,
        self.attack_range = attack_range
        self.modifiers = modifiers if modifiers else []
        self.hit_stat_used = hit_stat_used
        self.damage_stat_used = damage_stat_used
        self.requisites = requisites if requisites else []


class AttackInstance(object):
    def __init__(self, template, attacker, defender, hit_roll, damage_roll):
        self.template = template
        self.attacker = attacker
        self.defender = defender
        self.hit_roll = hit_roll
        self.damage_roll = damage_roll


# TODO Attacks will need prerequisites so you can't slash with a hammer.

# TODO Move this out of here to a proper place
punch_template = AttackTemplate(
    name="Punch",
    description="The mighty fist is presented to the weak flesh.",
    message="%A throws %Ahis fist into %D's %BP!",
    attack_type=enums.AttackType.Melee,
    attack_sub_type=enums.AttackSubType.Unarmed,
    target_type=enums.TargetType.Single,
    modifiers=None,
    attack_range=0,
    hit_stat_used=Stats.Strength,
    damage_stat_used=Stats.Strength,
    requisites=[requirements.PhysicalAbilityRequirement(requirements.CompareType.GreaterOrEqual, 1, PhysicalAbilities.PUNCH)]
)
slash_template = AttackTemplate(
    name="Slash",
    description="The sharpened blade parts the flesh.",
    message="%A slashes %WP across %D's %BP!",
    attack_type=enums.AttackType.Melee,
    attack_sub_type=enums.AttackSubType.Weapon,
    attack_range=0,
    target_type=enums.TargetType.Single,
    modifiers=None,
    hit_stat_used=Stats.Strength,
    damage_stat_used=Stats.Strength,
    requisites=[requirements.ItemDamageTypeRequirement(requirements.CompareType.Equal, DamageType.Slash)]
)
smash_template = AttackTemplate(
    name="Smash",
    description="The hardened metal crushes the bone.",
    message="%A smashes %WP on %D's %BP!",
    attack_type=enums.AttackType.Melee,
    attack_sub_type=enums.AttackSubType.Weapon,
    attack_range=0,
    target_type=enums.TargetType.Single,
    modifiers=None,
    hit_stat_used=Stats.Strength,
    damage_stat_used=Stats.Strength,
    requisites=[requirements.ItemDamageTypeRequirement(requirements.CompareType.Equal, DamageType.Blunt)]
)
stab_template = AttackTemplate(
    name="Stab",
    description="The point pierces the veil.",
    message="%A stabs %WP through %D's %BP!",
    attack_type=enums.AttackType.Melee,
    attack_sub_type=enums.AttackSubType.Weapon,
    attack_range=0,
    target_type=enums.TargetType.Single,
    modifiers=None,
    hit_stat_used=Stats.Strength,
    damage_stat_used=Stats.Strength,
    requisites=[requirements.ItemDamageTypeRequirement(requirements.CompareType.Equal, DamageType.Pierce)]
)
base_attacks = [punch_template, slash_template, smash_template, stab_template]