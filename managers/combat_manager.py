import random

# TODO We are going the D&D 5E SRD route.
# TODO It still means we can have several attack flavors and defense flavors
# TODO But we should streamline the actual attacks.


def choose_attack(attacker):
    attacks = attacker.get_attacks()

    # TODO These attacks should have a priority by effectiveness
    # TODO They should also apply their prereqs

    return random.choice(attacks)


def make_defense(attack, defender, roll):
    # TODO Here we'll need the total attack hit roll.
    # TODO We will use this to determine which type of defense we should apply.
    # TODO This is merely cosmetic.
    pass


def execute_combat_round(attacker, defender):
    """
    This is meant to be the "round" when you walk into someone.
    """
    # Prepare attack
    attack_template = choose_attack(attacker)
    attack_template.make_attack(attack_template, attacker, defender)

# TODO Implement Limb Damaging statuses.
# TODO Implement prioritized defenses based on hitroll with flavor.
# TODO Implement all base attack types.
