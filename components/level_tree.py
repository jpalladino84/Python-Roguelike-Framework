class LevelTree(object):
    """
    The goal of this Tree is to return advantages of a level recursively.
    """
    def __init__(self):
        self.stats_modifiers = {}
        self.abilities_modifiers = {}

    def get_stat_adjustments(self, current_level):
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

if __name__ == '__main__':
    # TEST
    from stats import Stats, StatModifier
    test_tree = LevelTree()
    test_tree.stats_modifiers = {
        1: [StatModifier(Stats.Health, 1)],
        2: [StatModifier(Stats.Health, 1), StatModifier(Stats.Dexterity, 1)],
        3: [StatModifier(Stats.Health, 1)]
    }
    print test_tree.get_stat_adjustments(3)

