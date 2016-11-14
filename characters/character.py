class Character(object):
    def __init__(self, uid, name, character_class, character_race, stats, display, location, inventory, body, main_experience_pool):
        self.uid = uid
        self.name = name
        self.character_class = character_class
        self.character_race = character_race
        self.stats = stats
        self.display = display
        self.location = location
        self.inventory = inventory
        self.body = body
        self.main_experience_pool = main_experience_pool

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


class CharacterTemplate(object):
    def __init__(self, uid, name, class_uid, race_uid, base_stats, display, body_uid, cumulative_level):
        self.uid = uid
        self.name = name
        self.class_uid = class_uid
        self.race_uid = race_uid
        self.base_stats = base_stats
        self.display = display
        self.body_uid = body_uid
        self.cumulative_level = cumulative_level
