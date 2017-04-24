from components.component import Component
from components.messages import QueryType


class CharacterClass(Component):
    NAME = 'character_class'

    # TODO ExperiencePool should itself be a component and be stripped off here.
    # TODO This component should instead MESSAGE the experience pool to register one.
    def __init__(self, uid, name, level_tree, hit_die):
        super().__init__()
        self.uid = uid
        self.name = name
        self.level_tree = level_tree
        self.get_level = lambda: 0
        self.hit_die = hit_die

    def copy(self):
        return CharacterClass(
            uid=self.uid,
            name=self.name,
            level_tree=self.level_tree,
            hit_die=self.hit_die
        )

    def on_register(self, host):
        super().on_register(host)
        host.register_query_responder(self, QueryType.StatModifier, self.respond_stat_modifier_query)
        results = host.transmit_query(self, QueryType.ExperiencePool, name=self.name)
        self.get_level = results[0]

    def respond_stat_modifier_query(self, stat):
        if self.level_tree:
            modifiers = self.level_tree.get_stat_modifiers(self.get_level())
            if stat in modifiers:
                return modifiers[stat]
