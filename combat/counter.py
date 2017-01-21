class CounterTemplate(object):
    def __init__(self, name, description, message, defend_attack_type, defend_attack_sub_type,
                 attack_type, attack_sub_type, target_type, modifiers, stat_used):
        self.name = name
        self.description = description
        self.message = message
        self.defend_attack_type = defend_attack_type
        self.defend_attack_sub_type = defend_attack_sub_type
        self.attack_type = attack_type
        self.attack_sub_type = attack_sub_type
        self.target_type = target_type
        self.modifiers = modifiers
        self.stat_used = stat_used


class CounterInstance(object):
    def __init__(self, template, attacker, defender):
        self.template = template
        self.attacker = attacker
        self.defender = defender
