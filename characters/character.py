import math
from components.location import Location
from components.equipment import Equipment
from components.stats import Stats


class Character(object):
    def __init__(self, uid, name, character_class, character_race, stats, display,
                 inventory, body, main_experience_pool, location=None, equipment=None):
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
        self.equipment = equipment if equipment else Equipment(self)

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

    def get_stat_modifier(self, stat):
        current_total = self.stats.get_stat(stat) + self.character_race.get_stat_modifier(stat)
        return math.floor((current_total - 10) / 2)

    def get_attack_modifier(self):
        # TODO Figure out better ways to calculate this
        return self.get_stat_modifier(Stats.Strength)

    def get_defense_modifier(self):
        # TODO Figure out better ways to calculate this
        return self.get_stat_modifier(Stats.Dexterity)

    def get_health_modifier(self):
        # TODO Figure out better ways to calculate this
        return self.get_stat_modifier(Stats.Health)

    def get_speed_modifier(self):
        # TODO Figure out better ways to calculate this
        return self.get_stat_modifier(Stats.Dexterity)

    def get_armor_class(self):
        base_ac = self._get_base_armor_class()
        max_dex_modifier = self._get_maximum_dex_bonus()
        dex_modifier = self.get_stat_modifier(Stats.Dexterity)
        if dex_modifier > max_dex_modifier:
            dex_modifier = max_dex_modifier
        armor_modifier = self._get_equipment_modifiers(Stats.ArmorClass)
        effect_modifier = self._get_effects_modifier(Stats.ArmorClass)
        level_tree_modifiers = self._get_level_tree_modifiers(Stats.ArmorClass)

        return base_ac + dex_modifier + armor_modifier + effect_modifier + level_tree_modifiers

    def _get_base_armor_class(self):
        # TODO This can be affected by a few things.
        return 10

    def _get_maximum_dex_bonus(self):
        # TODO This is affected by armor
        # 20 Is just a magic number, dex bonus should never go past that anyway.
        return 20

    def _get_equipment_modifiers(self, stat):
        # TODO Check all equipment and return its bonus AC.
        # TODO This should be abstracted to any stats!
        return 0

    def _get_effects_modifier(self, stat):
        # TODO Check all effects.. (spells poisons, whatever)
        # TODO This should be abstracted to any stats!
        return 0

    def _get_level_tree_modifiers(self, stat):
        # TODO This should grab all the bonuses for a stat from any level tree
        return 0

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
