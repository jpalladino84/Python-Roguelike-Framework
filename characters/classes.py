from components.component import Component
from components.component_messages import QueryStatModifierMessage


class CharacterClass(object):
    def __init__(self, uid, name, level_tree, experience_penalty=0):
        self.uid = uid
        self.name = name
        self.level_tree = level_tree
        self.experience_penalty = experience_penalty


class CharacterClassInstance(Component):
    NAME = 'character_class'

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
