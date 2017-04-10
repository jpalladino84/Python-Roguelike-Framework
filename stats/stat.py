import math


class Stat(object):
    def __init__(self, uid, current, maximum):
        self.uid = uid
        self.current = current
        self.maximum = maximum

    def __str__(self):
        return str(self.current)

    def __int__(self):
        return int(self.current)

    def modify_current(self, value):
        self.current += value

    def modify_max(self, value):
        self.maximum += value


class StatModifier(object):
    def __init__(self, uid, value, level_progression=0):
        self.uid = uid
        self.value = value
        self.level_progression = level_progression

    def __int__(self):
        return

    def get_leveled_value(self, level, initial_level):
        if self.level_progression > 0:
            multiplier = (level - initial_level) / self.level_progression
            return math.ceil(self.value * multiplier)
        else:
            return self.value


