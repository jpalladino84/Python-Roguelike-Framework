class Character(object):
    def __init__(self, uid, name, character_class, character_race, stats, display, location, inventory, body):
        self.uid = uid
        self.name = name
        self.character_class = character_class
        self.character_race = character_race
        self.stats = stats
        self.display = display
        self.location = location
        self.inventory = inventory
        self.body = body

    def is_dead(self):
        """
        This verifies if the character is really dead, whether living or undead.
        :return: bool
        """
        # TODO Make this
        pass

    def get_attack(self):
        # TODO Figure out better ways to calculate this
        return self.stats.strength

    def get_defense(self):
        # TODO Figure out better ways to calculate this
        return self.stats.dexterity

    def get_health(self):
        # TODO Figure out better ways to calculate this
        return self.stats.health

    def get_speed(self):
        # TODO Figure out better ways to calculate this
        return self.stats.dexterity
