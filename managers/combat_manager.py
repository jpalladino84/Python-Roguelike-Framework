import random

from combat import enums as combat_enums
from combat.attack import MeleeAttackTemplate
from stats.enums import StatsEnum
from managers import echo
from util.colors import Colors


# TODO We are going the D&D 5E SRD route.
# TODO It still means we can have several attack flavors and defense flavors
# TODO But we should streamline the actual attacks.


def choose_attack(attacker):
    attacks = attacker.get_attacks()

    # TODO These attacks should have a priority by effectiveness
    # TODO They should also apply their prereqs
    if attacks:
        melee_attacks = [attack for attack in attacks if isinstance(attack, MeleeAttackTemplate)]
        if melee_attacks:
            return random.choice(melee_attacks)
        return random.choice(attacks)


def choose_defense(attacker, defender, hit_roll):
    defenses = [defense for defense in defender.get_defenses()
                if defense.evaluate(attacker, hit_roll)]

    return random.choice(defenses)


def execute_combat_round(attacker, defender):
    """
    This is meant to be the "round" when you walk into someone.
    """
    # Prepare attack
    attack_template = choose_attack(attacker)
    if not attack_template:
        return
    attack_result = attack_template.make_attack(attacker, defender)

    if attack_result.success:
        threat_level = get_threat_level(attack_result.total_damage, defender.stats.get_current_value(StatsEnum.Health))
        attack_result.body_part_hit = defender.body.get_random_body_part_for_threat_level(threat_level)
        # TODO We might want to display info about actual rolls but that should be handled in the Echo manager/service
        # TODO I am still unsure on where its best to apply actual damage.
        # TODO Leaving it in the defender object could have them behave differently
        # TODO but at the same time having it centralized in one location will keep the other classes smaller.
        # TODO Maybe this should be extracted to a component?
        take_damage(defender, attack_result)
    else:
        choose_defense(attacker, defender, attack_result.total_hit_roll).make_defense(attacker, defender)
    echo.EchoService.singleton.console.printStr(str(attack_result) + "\n")


def take_damage(actor, attack_result):
    # TODO Here we take each damage dealt, apply resistance
    # TODO Determine threat level for total damage
    if attack_result.total_damage <= 0:
        return
    damage_string = "... "
    wound_strings = []

    for damage, damage_type in attack_result.separated_damage:
        if damage > 0:
            wound_strings.append(describe_wounds(damage_type))
            actor.stats.modify_core_current_value(StatsEnum.Health, -damage)

    damage_string += ",".join(wound_strings)
    damage_string += " {} {} for {} damage!".format(
        echo.his_her_it(actor), attack_result.body_part_hit.name, attack_result.total_damage)
    echo.EchoService.singleton.console.printStr(damage_string + "\n")

    # TODO THIS MUST BE EXTRACTED
    # check for death. if there's a death function, call it
    if actor.stats.get_current_value(StatsEnum.Health) <= 0:
        if actor.is_player:
            player_death(actor, echo.EchoService.singleton.console)
        else:
            monster_death(actor, echo.EchoService.singleton.console)

        x, y = actor.location.get_local_coords()
        actor.current_level.maze[x][y].contains_object = False


def player_death(player, console):
    # TODO This should not be here
    # the game ended!
    console.printStr('You have died... Game Over\n\n')

    # for added effect, transform the player into a corpse!
    player.display.ascii_character = '%'
    player.display.foreground_color = Colors.BLOOD_RED


def monster_death(monster, console):
    # TODO This should not be here
    # transform it into a nasty corpse! it doesn't block, can't be
    # attacked and doesn't move
    console.printStr('{} has died.\n\n'.format(monster.name))
    monster.display.ascii_character = '%'
    monster.display.foreground_color = Colors.BLOOD_RED
    monster.blocks = False
    monster.name = 'remains of ' + monster.name


def get_threat_level(total_damage, health):
    minor = (float(health) / 5)
    major = (float(health) / 2.5)
    critical = (float(health) / 1.5)

    if total_damage <= minor:
        return combat_enums.ThreatLevel.Minor
    elif minor < total_damage <= major:
        return combat_enums.ThreatLevel.Major
    elif major < total_damage <= health:
        return combat_enums.ThreatLevel.Critical
    elif total_damage >= health:
        return combat_enums.ThreatLevel.Fatal


def describe_wounds(damage_type):
    if damage_type == combat_enums.DamageType.Blunt:
        return "bruising"
    elif damage_type == combat_enums.DamageType.Slash:
        return "cutting"
    elif damage_type == combat_enums.DamageType.Pierce:
        return "piercing"

# TODO Implement Limb Damaging statuses.

