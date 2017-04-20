import abc

from combat.enums import DamageType
from stats.enums import StatsEnum
from managers import echo
from util import check_roller
from util.dice import DiceStack, Dice
from . import enums


class AttackTemplate(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name, description, message,
                 target_type, attack_range, modifiers,
                 hit_stat_used, damage_stat_used, damage_type, requirements=None):
        self.name = name
        self.description = description
        self.message = message
        self.target_type = target_type,
        self.attack_range = attack_range
        self.modifiers = modifiers if modifiers else {}
        self.hit_stat_used = hit_stat_used
        self.damage_stat_used = damage_stat_used
        self.requirements = requirements if requirements else []
        self.damage_type = damage_type

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

    def get_damage_type(self, **kwargs):
        return self.damage_type

    def make_attack(self, attacker, defender, **kwargs):
        attack_result = self.make_hit_roll(attacker, defender, **kwargs)
        if attack_result.success:
            self.make_damage_roll(attacker, attack_result, **kwargs)

        # TODO Probably a good idea to remove this from the attack and into the manager.
        echo.EchoService.singleton.combat_context_echo(
            message=self.message + "...",
            attacker=attacker,
            defender=defender,
            **kwargs
        )
        return attack_result

    def make_hit_roll(self, attacker, defender, **kwargs):
        target_ac = defender.get_armor_class()
        success, critical, natural_roll, total_hit_roll = check_roller.d20_check_roll(
            difficulty_class=target_ac,
            modifiers=self.get_hit_bonus(attacker)
        )
        return AttackResult(success, critical, defender, target_ac, natural_roll, total_hit_roll)

    def make_damage_roll(self, attacker, attack_result, **kwargs):
        total_damage = check_roller.roll_damage(
            dice_stacks=[self.get_damage_dice(**kwargs)],
            modifiers=self.get_damage_bonus(attacker, **kwargs),
            critical=attack_result.critical
        )
        attack_result.total_damage = total_damage
        attack_result.separated_damage = [(total_damage, self.get_damage_type(**kwargs))]

        return attack_result


class UnarmedAttackTemplate(AttackTemplate):
    # TODO I admit, this looks ugly.
    def __init__(self, name, description, message, basic_damage_dice=DiceStack(1, Dice(3)), bodypart_id_needed="humanoid_hand",
                 target_type=enums.TargetType.Single, attack_range=0, modifiers=None, hit_stat_used=StatsEnum.Strength,
                 damage_stat_used=StatsEnum.Strength, damage_type=enums.DamageType.Blunt, requirements=None):

        super().__init__(name=name, description=description, message=message, target_type=target_type,
                         attack_range=attack_range, modifiers=modifiers, hit_stat_used=hit_stat_used,
                         damage_stat_used=damage_stat_used, damage_type=damage_type, requirements=requirements)

        self.basic_damage_dice = basic_damage_dice
        self.bodypart_id_needed = bodypart_id_needed

    def get_damage_dice(self, *args, **kwargs):
        if 'attacker' in kwargs:
            return DiceStack(1, Dice(kwargs['attacker'].stats.size - 1))
        return self.basic_damage_dice

    def get_damage_bonus(self, attacker, **kwargs):
        return (self.modifiers.get('damage_modifier', 0) +
                attacker.get_stat_modifier(self.damage_stat_used))


class MeleeAttackTemplate(AttackTemplate):
    def __init__(self, name, description, message, required_item_melee_damage_type,
                 target_type=enums.TargetType.Single, attack_range=0, modifiers=None, hit_stat_used=StatsEnum.Strength,
                 damage_stat_used=StatsEnum.Strength, requirements=None):

        super().__init__(name=name, description=description, message=message, target_type=target_type,
                         attack_range=attack_range, modifiers=modifiers, hit_stat_used=hit_stat_used,
                         damage_stat_used=damage_stat_used, damage_type=None, requirements=requirements)

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
        return attacker_weapon.weapon.damage_dice

    def get_used_weapon(self, attacker):
        for wielded_item in attacker.equipment.get_wielded_items():
            weapon = wielded_item.get_component('weapon')
            if weapon.melee_damage_type == self.required_item_melee_damage_type:
                return wielded_item

    def get_damage_type(self, **kwargs):
        item = kwargs.get("attacker_weapon")
        if item.weapon:
            return item.weapon.melee_damage_type
        else:
            # TODO This indicates an improvised weapon. We'll need to get a better way to handle this.
            return DamageType.Blunt


class RangedAttackTemplate(AttackTemplate):
    pass


class AttackResult(object):
    """
    A class to keep a combat attack result organized across functions.
    """
    __slots__ = ['success', 'critical', 'target_object',
                 'natural_roll', 'total_hit_roll', 'total_damage',
                 'separated_damage', 'target_ac', 'body_part_hit']

    def __init__(self, success, critical, target_object, target_ac,
                 natural_roll=None, total_hit_roll=None, total_damage=None, separated_damage=None):

        self.success = success
        self.critical = critical
        self.natural_roll = natural_roll
        self.total_hit_roll = total_hit_roll
        self.total_damage = total_damage
        self.separated_damage = separated_damage
        self.target_object = target_object
        self.target_ac = target_ac
        self.body_part_hit = None

    def __str__(self):
        return "Rolled {} vs AC:{}".format(self.total_hit_roll, self.target_ac)
