class LevelTree(object):
    NAME = "level_tree"
    """
    The goal of this Tree is to return advantages of a level recursively.
    """
    def __init__(self):
        super().__init__()
        self.stats_modifiers = {}
        self.abilities_modifiers = {}

    def get_stat_modifiers(self, current_level):
        final_modifiers = {}
        ordered_modifiers = sorted(self.stats_modifiers.keys())
        for level in ordered_modifiers:
            if int(level) > int(current_level):
                continue

            for stat_modifier in self.stats_modifiers[level]:
                if stat_modifier in final_modifiers:
                    final_modifiers[stat_modifier.uid] += stat_modifier.get_leveled_value(current_level, level)
                else:
                    final_modifiers[stat_modifier.uid] = stat_modifier.get_leveled_value(current_level, level)

        return final_modifiers

    def get_ability_modifiers(self, current_level):
        final_modifiers = {}
        for level in sorted(self.abilities_modifiers.keys()):
            if level > current_level:
                continue
            for ability_modifier in self.abilities_modifiers[level]:
                if ability_modifier.uid in final_modifiers:
                    final_modifiers[ability_modifier.uid] += ability_modifier.get_leveled_value(current_level, level)
                else:
                    final_modifiers[ability_modifier.uid] = ability_modifier.get_leveled_value(current_level, level)

        return final_modifiers

    def add_stat_modifier(self, level, stat_modifier):
        if level not in self.stats_modifiers:
            self.stats_modifiers[level] = []
        self.stats_modifiers[level].append(stat_modifier)

    def add_ability_modifier(self, level, ability_modifier):
        if level not in self.abilities_modifiers:
            self.abilities_modifiers[level] = []
        self.abilities_modifiers[level].append(ability_modifier.power)





