import math

from characters.enums import Sex, EncumberanceLevel
from data.python_templates.attacks import base_attacks
from data.python_templates.defenses import base_defenses
from components.experience_pool import ExperiencePool
from components.equipment import Equipment
from components.location import Location
from components.inventory import Inventory
from stats.enums import StatsEnum
from components.game_object import GameObject


class Character(GameObject):
    def __init__(self, uid, name, character_class, character_race, stats, display, body,
                 inventory=None, main_experience_pool=None, location=None, equipment=None, sex=None):
        super().__init__()
        self.uid = uid
        self._name = name
        if not main_experience_pool:
            self.register_component(ExperiencePool())
        else:
            self.register_component(main_experience_pool)

        if character_class:
            self.register_component(character_class)

        if character_race:
            self.register_component(character_race)

        if stats:
            self.register_component(stats)

        if equipment:
            self.register_component(equipment)
        else:
            self.register_component(Equipment())

        self.display = display
        if not location:
            self.location = Location()
        else:
            self.location = location

        if inventory:
            self.register_component(inventory)
        else:
            self.register_component(Inventory())

        if body:
            self.register_component(body)
        self.is_player = False
        self.sex = sex if sex else Sex.Male

    def copy(self):
        # TODO Eventually pretty much everything in here will be components
        # TODO Which means we will only have to loop on components and call copy()
        new_instance = Character(
            uid=self.uid,
            name=self.name,
            character_class=None,
            character_race=None,
            stats=None,
            display=self.display.copy(),
            body=self.body.copy(),
            location=None,
            sex=self.sex
        )
        return super().copy_to(new_instance)

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
        return self.stats.get_current_value(StatsEnum.Health) <= 0

    def get_stat_modifier(self, stat):
        current_total = self.stats.get_current_value(stat)
        return math.floor((current_total - 10) / 2)

    def get_attack_modifier(self):
        # TODO Figure out better ways to calculate this
        return self.get_stat_modifier(StatsEnum.Strength)

    def get_health_modifier(self):
        # TODO Figure out better ways to calculate this
        return self.get_stat_modifier(StatsEnum.Health)

    def get_speed_modifier(self):
        # TODO Figure out better ways to calculate this
        return self.get_stat_modifier(StatsEnum.Dexterity)

    def get_armor_class(self):
        base_ac = self._get_base_armor_class()
        effective_dex_modifier = self.get_effective_dex_modifier()

        armor_modifier = self.get_armor_modifiers()
        effect_modifier = self._get_effects_modifier(StatsEnum.ArmorClass)
        level_tree_modifiers = self._get_level_tree_modifiers(StatsEnum.ArmorClass)

        return base_ac + effective_dex_modifier + armor_modifier + effect_modifier + level_tree_modifiers

    def get_effective_dex_modifier(self):
        max_dex_modifier = self._get_maximum_dex_bonus()
        effective_dex_modifier = self.get_stat_modifier(StatsEnum.Dexterity)
        if effective_dex_modifier > max_dex_modifier:
            effective_dex_modifier = max_dex_modifier

        return effective_dex_modifier

    def _get_base_armor_class(self):
        # TODO This can be affected by a few things.
        return 10

    def _get_maximum_dex_bonus(self):
        # This deviates from normal D&D rules but the benefit
        # of handling multiple armor pieces is worth it.
        # This should still be close enough to the rules.
        total_weight = self.equipment.get_load_of_worn_items()
        load_level = self.get_encumberance_level(total_weight)
        if load_level == EncumberanceLevel.LIGHT:
            return 100
        elif load_level == EncumberanceLevel.MEDIUM:
            return 2
        else:
            return 0

    def get_encumberance_level(self, weight):
        light = 13
        medium = 40

        if weight <= light:
            return EncumberanceLevel.LIGHT
        elif weight <= medium:
            return EncumberanceLevel.MEDIUM
        else:
            return EncumberanceLevel.HEAVY

    def get_armor_modifiers(self):
        total_armor_ac = 0
        worn_items = self.equipment.get_worn_items()
        for item in worn_items:
            armor = item.armor
            total_armor_ac += armor.get_real_armor_class()

        return int(total_armor_ac)

    def get_shield_modifiers(self):
        # TODO Check worn shields and return the bonus AC.
        # TODO This could be abstracted? To any stats?
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

    def get_attacks(self):
        # We'll need to distinguish innate racial attacks and learned attacks.
        # This BaseAttack is just in the meantime.
        return [attack for attack in base_attacks if attack.evaluate_requirements(self)]

    def get_defenses(self):
        return base_defenses

