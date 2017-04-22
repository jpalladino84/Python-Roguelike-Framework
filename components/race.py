from components.component import Component
from components.messages import QueryType

# TODO We need to fix the Class Instance Whatever here


class Race(Component):
    NAME = 'character_race'
    """
    Racial characteristics and bonuses
    """
    def __init__(self, uid, name, level_tree, body_template_uid):
        super().__init__()
        self.uid = uid
        self.name = name
        # TODO Some races won't be leveled, should acknowledge a level_tree of one
        # TODO and avoid registering a pool
        self.level_tree = level_tree
        self.body_template_uid = body_template_uid
        self.get_level = lambda: 0

    def copy(self):
        return Race(
            uid=self.uid,
            name=self.name,
            level_tree=self.level_tree,
            body_template_uid=self.body_template_uid
        )

    def on_register(self, host):
        super().on_register(host)
        host.register_query_responder(self, QueryType.StatModifier, self.respond_stat_modifier_query)
        if self.level_tree:
            results = host.transmit_query(self, QueryType.ExperiencePool, name=self.name)
            self.get_level = results[0]

    def respond_stat_modifier_query(self, message):
        if self.level_tree:
            modifiers = self.level_tree.get_stat_modifiers(self.get_level())
            if message.stat in modifiers:
                response = message.create_response(self)
                response.stat_modifier_value = modifiers[message.stat]

                return response


class MetaRace(Race):
    """
    Pretty much the same as a race but is more like a modifier itself.
    """
    def __init__(self, uid, name, level_tree, body_modifier_template_uid):
        super().__init__(uid, name, level_tree, None)
        self.body_modifier_template_uid = body_modifier_template_uid

