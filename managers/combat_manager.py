import random
from combat.attack import AttackInstance
from combat.defense import DefenseInstance
from combat.counter import CounterInstance


def choose_attack(attacker):
    # TODO These attacks should have a priority by effectiveness
    attacks = attacker.get_attacks()
    return random.choice(attacks)


def prepare_attack(attack, attacker, defender):
    # This will prepare an instance and make necessary rolls for the attack
    hit_roll = (
        random.randint(1, 20)
        + attack.modifiers.get('hit_modifier', 0)
        + attacker.get_stat_modifier(attack.hit_stat_used)
    )
    damage_roll = random.randint(
        attack.modifiers.get('minimum_damage', 0),
        attack.modifiers.get('maximum_damage', 0)
    ) + attacker.get_stat_modifier(attack.damage_stat_used)

    return AttackInstance(attack, attacker, defender, hit_roll, damage_roll)


def choose_defense(attack, defender):
    applicable_defenses = [defense for defense in defender.get_defenses()
                           if defense.defend_attack_type == attack.attack_type
                           and defense.defend_attack_sub_type == attack.attack_sub_type]

    # TODO Defenses should be prioritized by effectiveness
    return random.choice(applicable_defenses)


def prepare_defense(defense, attacker, defender):
    # From the chosen defense prepare the rolls for the current defender
    defense_roll = (
        random.randint(1, 20)
        + defense.modifiers.get('defense_modifier', 0)
        + defender.get_stat_modifier(defense.stat_used)
    )
    return DefenseInstance(defense, attacker, defender, defense_roll)


def choose_counter(attack, defender):
    applicable_counters = [counter for counter in defender.get_counters()
                           if counter.defend_attack_type == attack.attack_type
                           and counter.defend_attack_sub_type == attack.attack_sub_type]

    # TODO Counters should be prioritized by effectiveness
    return random.choice(applicable_counters)


def prepare_counter(counter, attacker, defender):
    hit_roll = (
        random.randint(1, 20)
        + counter.modifiers.get('hit_modifier', 0)
        + defender.get_stat_modifier(counter.hit_stat_used)
    )
    damage_roll = random.randint(
        counter.modifiers.get('minimum_damage', 0),
        counter.modifiers.get('maximum_damage', 0)
    ) + defender.get_stat_modifier(counter.damage_stat_used)

    return CounterInstance(counter, attacker, defender, hit_roll, damage_roll)


def execute_combat_round(attacker, defender):
    """
    This is meant to be the "round" when you walk into someone.
    """
    # Prepare attack
    attack_template = choose_attack(attacker)
    attack_instance = prepare_attack(attack_template, attacker, defender)
    defense_template = choose_defense(attacker, defender)
    defense_instance = prepare_defense(defense_template, attacker, defender)
    if attack_instance.hit_roll > defense_instance.defense_roll:
        # HIT!
        pass
    else:
        # Defense Sucess
        if defense_instance.defense_roll > attack_instance.hit_roll * 2:
            # COUNTER!
            counter_template = choose_attack(defender)
            counter_instance = prepare_attack(attack_template, defender, attacker)
            defense_template = choose_defense(counter_template, attacker)
            defense_instance = prepare_defense(defense_template, defender, attacker)
            if counter_instance.hit_roll > defense_instance.defense_roll:
                # HIT!
                pass
    # For every defender prepare their defense, if critical execute counter
    # Apply attack results to every defender that failed their defense
    # Apply counters to attacker if any
    pass


# TODO This combat manager will need to handle multiple scenarios.
# Anything could target anything, basically.
# If we want to have good messages tying together we will need to use many enums.
# Types could be Melee, Ranged, Magic
# Subtypes would vary but they should include types like, Melee - Sword, Melee - Unarmed, Ranged - Arrow, Magic - Bolt
# We should also have a list of attacks and defenses for each type and they should be limited to a particular
# skill level.

# The target must also be taken into account, being able to block, dodge, counter.
# Can't counter a Ranged attack with Melee defense, for example.

# Different maneuvers would use different stats, a dodge could use dex, block use str and magic defense could be wisdom.

# One attack should only be vulnerable to a single counter.
# We could also have finishers to execute in gory details, a small chance to happen when the target is low hp,
# but could also be triggered manually by attacking an unconscious creature.

# In all this, we should also support channeled attacks, ki beams anyone?
# This channeling would be a sort of sustained attack.

# Any limb attacked should be able to be crippled and all cripples will vary depending on damage type.
# Like that, severed limbs would bleed out, crushed and burnt limbs would inflict massive pain.
