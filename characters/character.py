from components.location import Location


class Character(object):
    def __init__(self, uid, name, character_class, character_race, stats, display,
                 inventory, body, main_experience_pool, location=None):
        self.uid = uid
        self._name = name
        self.character_class = character_class
        self.character_race = character_race
        self.stats = stats
        self.display = display
        if not location:
            self.location = Location()
        else:
            self.location = location
        self.inventory = inventory
        self.body = body
        self.main_experience_pool = main_experience_pool
        self.is_player = False

    @property
    def name(self):
        if self.is_player:
            return "(You)" + self._name
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def is_dead(self):
        """
        This verifies if the character is really dead, whether living or undead.
        :return: bool
        """
        # TODO Make this
        return int(self.stats.health) <= 0

    def get_attack_total(self):
        # TODO Figure out better ways to calculate this
        return self.stats.strength.current + self.character_race.get_stat_modifier(self.stats.strength)

    def get_defense_total(self):
        # TODO Figure out better ways to calculate this
        return self.stats.dexterity.current + self.character_race.get_stat_modifier(self.stats.dexterity)

    def get_health_total(self):
        # TODO Figure out better ways to calculate this
        return self.stats.health.current + self.character_race.get_stat_modifier(self.stats.health)

    def get_speed_total(self):
        # TODO Figure out better ways to calculate this
        return self.stats.dexterity.current + self.character_race.get_stat_modifier(self.stats.dexterity)

    @property
    def current_level(self):
        return self.location.level


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
