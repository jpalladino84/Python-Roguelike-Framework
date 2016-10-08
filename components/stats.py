class Stat(object):
    def __init__(self, current, max):
        self.current = current
        self.max = max

    def modify_current(self, value):
        self.current += value

    def modify_max(self, value):
        self.max += value


class CharacterStats(object):
    def __init__(self):
        self.health = Stat(1, 1)
        self.mana = Stat(1, 1)
        self.strength = Stat(1, 1)
        self.dexterity = Stat(1, 1)
        self.constitution = Stat(1, 1)
        self.intelligence = Stat(1, 1)
        self.charisma = Stat(1, 1)
        self.wisdom = Stat(1, 1)
