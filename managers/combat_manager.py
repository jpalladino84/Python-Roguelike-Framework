import random
from components.colors import Colors
from combat.attack import MeleeAttackTemplate
from managers import echo

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
    success, critical, hit_roll, total_damage = attack_template.make_attack(attacker, defender)
    echo.echo_service.console.printStr("Hit Roll:{} vs AC:{}\n".format(hit_roll, defender.get_armor_class()))
    if success:
        # TODO We might want to display info about actual rolls but that should be handled in the Echo manager/service
        # TODO I am still unsure on where its best to apply actual damage.
        # TODO Leaving it in the defender object could have them behave differently
        # TODO but at the same time having it centralized in one location will keep the other classes smaller.
        # TODO Maybe this should be extracted to a component?
        take_damage(defender, total_damage, echo.echo_service.console)
    else:
        choose_defense(attacker, defender, hit_roll).make_defense(attacker, defender)


def take_damage(actor, damage, console):
    # TODO This should not be here
    # apply damage if possible
    if damage > 0:
        console.printStr('{} takes {} damage.\n\n'.format(actor.name, damage))
        actor.stats.health.modify_current(-damage)

    # check for death. if there's a death function, call it
    if actor.stats.health.current <= 0:
        if actor.is_player:
            player_death(actor, console)
        else:
            monster_death(actor, console)

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
# TODO Implement Limb Damaging statuses.
# TODO Implement all base attack types.
