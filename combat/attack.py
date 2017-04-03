from . import enums
import abc
from managers import echo

from components.stats import Stats
from components import requirements
from components.abilities.physical_abilities import PhysicalAbilities
from util.dice import DiceStack
from util import check_roller
from items.item import DamageType

# TODO We'll separate data from this module


class AttackTemplate(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name, description, message,
                 target_type, attack_range, modifiers,
                 hit_stat_used, damage_stat_used, requirements=None):
        self.name = name
        self.description = description
        self.message = message
        self.target_type = target_type,
        self.attack_range = attack_range
        self.modifiers = modifiers if modifiers else []
        self.hit_stat_used = hit_stat_used
        self.damage_stat_used = damage_stat_used
        self.requirements = requirements if requirements else []

    def evaluate_requirements(self, game_object):
        for requirement in self.requirements:
            if not requirement.evaluate(game_object):
                return False
        return True

    def get_hit_bonus(self, attacker, **kwargs):
        return self.modifiers.get('hit_modifier', 0) + attacker.get_stat_modifier(self.hit_stat_used)

    def get_damage_bonus(self, attacker, **kwargs):
        return self.modifiers.get('damage_modifier', 0) + attacker.get_stat_modifier(self.damage_stat_used)

    def get_damage_dice(self, **kwargs):
        return DiceStack(1, 1)

    def make_attack(self, attacker, defender, **kwargs):
        # This will prepare an instance and make necessary rolls for the attack
        # TODO This needs to grab modifiers depending on the attack types and equipment
        success, critical, roll = self.make_hit_roll(attacker, defender)
        if success:
            total_damage = self.make_damage_roll(attacker, critical)
            # TODO We describe and apply damage here to the attacker
        else:
            # TODO We describe defense here.
            pass

    def make_hit_roll(self, attacker, defender, **kwargs):
        success, critical, roll = check_roller.d20_check_roll(
            difficulty_class=defender.get_armor_class(),
            modifiers=self.get_hit_bonus(attacker)
        )
        return success, critical, roll

    def make_damage_roll(self, attacker, critical=False, **kwargs):
        total_damage = check_roller.roll_damage(
            dice_stacks=self.get_damage_dice(),
            modifiers=self.get_damage_bonus(attacker),
            critical=critical
        )

        return total_damage


class UnarmedAttackTemplate(AttackTemplate):
    # TODO I admit, this looks ugly.
    def __init__(self, name, description, message, basic_damage_dice=DiceStack(1, 3), bodypart_id_needed="humanoid_hand",
                 target_type=enums.TargetType.Single, attack_range=0, modifiers=None, hit_stat_used=Stats.Strength,
                 damage_stat_used=Stats.Strength, requirements=None):

        super().__init__(name=name, description=description, message=message, target_type=target_type,
                         attack_range=attack_range, modifiers=modifiers, hit_stat_used=hit_stat_used,
                         damage_stat_used=damage_stat_used, requirements=requirements)

        self.basic_damage_dice = basic_damage_dice
        self.bodypart_id_needed = bodypart_id_needed

    def get_damage_dice(self, *args, **kwargs):
        return self.basic_damage_dice

    def get_damage_bonus(self, attacker, **kwargs):
        return (self.modifiers.get('damage_modifier', 0) +
                attacker.get_stat_modifier(self.damage_stat_used) +
                attacker.stats.size - 1)


class MeleeAttackTemplate(AttackTemplate):
    def __init__(self, name, description, message, required_item_melee_damage_type,
                 target_type=enums.TargetType.Single, attack_range=0, modifiers=None, hit_stat_used=Stats.Strength,
                 damage_stat_used=Stats.Strength, requirements=None):

        super().__init__(name=name, description=description, message=message, target_type=target_type,
                         attack_range=attack_range, modifiers=modifiers, hit_stat_used=hit_stat_used,
                         damage_stat_used=damage_stat_used, requirements=requirements)

        self.required_item_melee_damage_type = required_item_melee_damage_type

    def make_attack(self, attacker, defender, **kwargs):
        # This will prepare an instance and make necessary rolls for the attack
        # TODO This needs to grab modifiers depending on the attack types and equipment
        weapon_used = self.get_used_weapon(attacker)
        success, critical, roll = self.make_hit_roll(attacker, defender, weapon_used=weapon_used)
        if success:
            total_damage = self.make_damage_roll(attacker, critical, weapon_used=weapon_used)
            # TODO We describe and apply damage here to the attacker
        else:
            # TODO We describe defense here.
            pass

    def get_hit_bonus(self, attacker, **kwargs):
        # TODO Weapon could have bonuses to hit
        return super().get_hit_bonus(attacker, **kwargs)

    def get_damage_bonus(self, attacker, **kwargs):
        # TODO Weapon could have bonuses to damage
        return super().get_damage_bonus(attacker, **kwargs)

    def get_damage_dice(self, **kwargs):
        weapon_used = kwargs.get("weapon_used")
        return DiceStack(weapon_used.damage_dice_amount, weapon_used.max_damage)

    def get_used_weapon(self, attacker):
        return next((weapon for weapon in attacker.get_wielded_items()
                     if weapon.melee_damage_type == self.required_item_melee_damage_type))


class RangedAttackTemplate(AttackTemplate):
    pass


# TODO Move this out of here to a proper place
punch_template = UnarmedAttackTemplate(
    name="Punch",
    description="The mighty fist is presented to the weak flesh.",
    message="%A throws %Ahis fist into %D's %BP!",
    requirements=[requirements.PhysicalAbilityRequirement(requirements.CompareType.GreaterOrEqual, 1, PhysicalAbilities.PUNCH)]
)
# TODO The melee damage type is repeated.. change that.
# TODO Also use the requirements to fetch... requirements... like required bodypart.
slash_template = MeleeAttackTemplate(
    name="Slash",
    description="The sharpened blade parts the flesh.",
    message="%A slashes %WP across %D's %BP!",
    required_item_melee_damage_type=DamageType.Slash,
    requirements=[requirements.ItemDamageTypeRequirement(requirements.CompareType.Equal, DamageType.Slash)]
)
smash_template = MeleeAttackTemplate(
    name="Smash",
    description="The hardened metal crushes the bone.",
    message="%A smashes %WP on %D's %BP!",
    required_item_melee_damage_type=DamageType.Blunt,
    requirements=[requirements.ItemDamageTypeRequirement(requirements.CompareType.Equal, DamageType.Blunt)]
)
stab_template = MeleeAttackTemplate(
    name="Stab",
    description="The point pierces the veil.",
    message="%A stabs %WP through %D's %BP!",
    required_item_melee_damage_type=DamageType.Pierce,
    requirements=[requirements.ItemDamageTypeRequirement(requirements.CompareType.Equal, DamageType.Pierce)]
)
base_attacks = [punch_template, slash_template, smash_template, stab_template]
