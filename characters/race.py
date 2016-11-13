class Race(object):
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


