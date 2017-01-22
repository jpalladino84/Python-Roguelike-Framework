class AttackTemplate(object):
    def __init__(self, name, description, message, attack_type,
                 attack_sub_type, target_type, modifiers, stat_used):
        self.name = name
        self.description = description
        self.message = message
        self.attack_type = attack_type
        self.attack_sub_type = attack_sub_type
        self.target_type = target_type
        self.modifiers = modifiers
        self.stat_used = stat_used


class AttackInstance(object):
    def __init__(self, template, attacker, defender, hit_roll, damage_roll):
        self.template = template
        self.attacker = attacker
        self.defender = defender
        self.hit_roll = hit_roll
        self.damage_roll = damage_roll
