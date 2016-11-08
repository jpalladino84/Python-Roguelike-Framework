class LevelTree(object):
    """
    The goal of this Tree is to return advantages of a level recursively.
    """
    def __init__(self):
        self.stats_modifiers = {}
        self.abilities_modifiers = {}

    def get_stat_modifiers(self, current_level):
        final_modifiers = {}
        for level in sorted(self.stats_modifiers.iterkeys()):
            if level > current_level:
                continue
            for stat_modifier in self.stats_modifiers[level]:
                if stat_modifier.uid in final_modifiers:
                    final_modifiers[stat_modifier.uid] += stat_modifier.value
                else:
                    final_modifiers[stat_modifier.uid] = stat_modifier.value

        return final_modifiers

    def add_stat_modifier(self, level, stat_modifier):
        if stat_modifier.uid in self.stats_modifiers[level]:
            self.stats_modifiers[level][stat_modifier.uid] += int(stat_modifier)
        else:
            self.stats_modifiers[level][stat_modifier.uid] = int(stat_modifier)
