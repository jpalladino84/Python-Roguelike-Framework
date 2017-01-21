class DefenseTemplate(object):
    def __init__(self, name, description, message, defend_attack_type,
                 defend_attack_sub_type, modifiers, stat_used):
        self.name = name
        self.description = description
        self.message = message
        self.defend_attack_type = defend_attack_type
        self.defend_attack_sub_type = defend_attack_sub_type
        self.stat_used = stat_used
        self.modifiers = modifiers


class DefenseInstance(object):
    def __init__(self, template, attacker, defender):
        self.template = template
        self.attacker = attacker
        self.defender = defender
