import math


class Ability(object):
    def __init__(self, uid, power, level_progression=0):
        self.uid = uid
        self.power = power
        self.level_progression = level_progression

    def get_leveled_value(self, level, initial_level):
        if self.level_progression > 0:
            multiplier = (level - initial_level) / self.level_progression
            return math.ceil(self.power * multiplier)
        else:
            return self.power
