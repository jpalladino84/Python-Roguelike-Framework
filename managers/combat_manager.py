import random

# TODO We are going the D&D 5E SRD route.
# TODO It still means we can have several attack flavors and defense flavors
# TODO But we should streamline the actual attacks.


def choose_attack(attacker):
    attacks = attacker.get_attacks()

    # TODO These attacks should have a priority by effectiveness
    # TODO They should also apply their prereqs

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
    success, critical, hit_roll, total_damage = attack_template.make_attack(attack_template, attacker, defender)
    if not success:
        choose_defense(attacker, defender, hit_roll).make_defense()


# TODO Implement Limb Damaging statuses.
# TODO Implement prioritized defenses based on hitroll with flavor.
# TODO Implement all base attack types.
