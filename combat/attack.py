from . import enums
import abc
from managers import echo

from components.stats import Stats
from components import requirements
from components.abilities.physical_abilities import PhysicalAbilities
from util.dice import DiceStack, Dice
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
        self.modifiers = modifiers if modifiers else {}
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
        return DiceStack(1, Dice(1))

    def make_attack(self, attacker, defender, **kwargs):
        success, critical, roll = self.make_hit_roll(attacker, defender, **kwargs)
        total_damage = 0 if not success else self.make_damage_roll(attacker, critical, **kwargs)
        body_part_hit = defender.body.get_random_body_part_by_relative_size()
        echo.echo_service.combat_context_echo(
            message=self.message, attacker=attacker, defender=defender, defender_bodypart=body_part_hit, **kwargs)

        return success, critical, roll, total_damage

    def make_hit_roll(self, attacker, defender, **kwargs):
        success, critical, roll = check_roller.d20_check_roll(
            difficulty_class=defender.get_armor_class(),
            modifiers=self.get_hit_bonus(attacker)
        )
        return success, critical, roll

    def make_damage_roll(self, attacker, critical=False, **kwargs):
        total_damage = check_roller.roll_damage(
            dice_stacks=[self.get_damage_dice(**kwargs)],
            modifiers=self.get_damage_bonus(attacker, **kwargs),
            critical=critical
        )
        return total_damage


class UnarmedAttackTemplate(AttackTemplate):
    # TODO I admit, this looks ugly.
    def __init__(self, name, description, message, basic_damage_dice=DiceStack(1, Dice(3)), bodypart_id_needed="humanoid_hand",
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
        attacker_weapon = self.get_used_weapon(attacker)
        return super().make_attack(attacker, defender, attacker_weapon=attacker_weapon)

    def get_hit_bonus(self, attacker, **kwargs):
        # TODO Weapon could have bonuses to hit
        return super().get_hit_bonus(attacker, **kwargs)

    def get_damage_bonus(self, attacker, **kwargs):
        # TODO Weapon could have bonuses to damage
        return super().get_damage_bonus(attacker, **kwargs)

    def get_damage_dice(self, **kwargs):
        attacker_weapon = kwargs.get("attacker_weapon")
        return DiceStack(int(attacker_weapon.stats.damage_dice_amount), Dice(int(attacker_weapon.stats.max_damage)))

    def get_used_weapon(self, attacker):
        return next((weapon for weapon in attacker.equipment.get_wielded_items()
                     if weapon.melee_damage_type == self.required_item_melee_damage_type))


class RangedAttackTemplate(AttackTemplate):
    pass


# TODO Move this out of here to a proper place
punch_template = UnarmedAttackTemplate(
    name="Punch",
    description="The mighty fist is presented to the weak flesh.",
    message="{attacker} throws {attacker_his} fist into {defender}'s {defender_bodypart}!",
    requirements=[requirements.PhysicalAbilityRequirement(requirements.CompareType.GreaterOrEqual, 1, PhysicalAbilities.PUNCH)]
)
# TODO The melee damage type is repeated.. change that.
# TODO Also use the requirements to fetch... requirements... like required bodypart.
slash_template = MeleeAttackTemplate(
    name="Slash",
    description="The sharpened blade parts the flesh.",
    message="{attacker} slashes {attacker_weapon} across {defender}'s {defender_bodypart}!",
    required_item_melee_damage_type=DamageType.Slash,
    requirements=[requirements.ItemDamageTypeRequirement(requirements.CompareType.Equal, DamageType.Slash)]
)
smash_template = MeleeAttackTemplate(
    name="Smash",
    description="The hardened metal crushes the bone.",
    message="{attacker} smashes {attacker_weapon} on {defender}'s {defender_bodypart}!",
    required_item_melee_damage_type=DamageType.Blunt,
    requirements=[requirements.ItemDamageTypeRequirement(requirements.CompareType.Equal, DamageType.Blunt)]
)
stab_template = MeleeAttackTemplate(
    name="Stab",
    description="The point pierces the veil.",
    message="{attacker} stabs {attacker_weapon} through {defender}'s {defender_weapon}!",
    required_item_melee_damage_type=DamageType.Pierce,
    requirements=[requirements.ItemDamageTypeRequirement(requirements.CompareType.Equal, DamageType.Pierce)]
)
base_attacks = [punch_template, slash_template, smash_template, stab_template]
