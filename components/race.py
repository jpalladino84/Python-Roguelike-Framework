from components.component import Component
from components.messages import QueryStatModifierMessage


# TODO We need to fix the Class Instance Whatever here
class Race(object):
    NAME = 'character_race'
    """
    Racial characteristics and bonuses
    """
    def __init__(self, uid, name, level_tree, body_template_uid, experience_penalty=0):
        self.uid = uid
        self.name = name
        self.level_tree = level_tree
        self.body_template_uid = body_template_uid
        self.experience_penalty = experience_penalty


class MetaRace(Race):
    """
    Pretty much the same as a race but is more like a modifier itself.
    """
    def __init__(self, uid, name, level_tree, body_modifier_template_uid):
        super().__init__(uid, name, level_tree, None)
        self.body_modifier_template_uid = body_modifier_template_uid


class RaceInstance(Component):
    def __init__(self, template, experience_pool):
        super().__init__()
        self.template = template
        self.experience_pool = experience_pool

    @property
    def name(self):
        return self.template.name

    @property
    def level_tree(self):
        return self.template.level_tree

    @property
    def experience_penalty(self):
        return self.template.level_tree

    def get_stat_modifier(self, stat):
        if self.template.level_tree:
            modifiers = self.template.level_tree.get_stat_modifiers(self.experience_pool.get_pool_level())
            if stat in modifiers:
                return modifiers[stat]
        return 0

    def handle_message(self, message):
        if isinstance(message, QueryStatModifierMessage):
            return self.handle_stat_modifier_query(message)

    def handle_stat_modifier_query(self, message):
        if self.template.level_tree:
            modifiers = self.template.level_tree.get_stat_modifiers(self.experience_pool.get_pool_level())
            if message.stat in modifiers:
                response = message.create_response(self)
                response.stat_modifier_value = modifiers[message.stat]

                return response
