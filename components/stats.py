import six

from components.component import Component
from components.messages import QueryType
from stats.enums import StatsEnum
from stats.stat import Stat


class Stats(Component):
    NAME = 'stats'
    """
    This is the component that implements core stats but can also retrieves other components stats.
    """
    def __init__(self, **kwargs):
        super().__init__()
        self._core_stats = {}
        for key, value in six.iteritems(kwargs):
            self.add_core_stat(StatsEnum[key.capitalize()], value, value)

    def add_core_stat(self, stat, current_value, maximum_value):
        if stat in StatsEnum:
            self._core_stats[stat] = Stat(stat, current_value, maximum_value)

    def modify_core_current_value(self, stat, modifier):
        if stat in self._core_stats:
            self._core_stats[stat].current += modifier

    def set_core_current_value(self, stat, current_value):
        if stat in self._core_stats:
            self._core_stats[stat].current = current_value

    def set_core_maximum_value(self, stat, maximum_value):
        if stat in self._core_stats:
            self._core_stats[stat].maximum = maximum_value

    def set_total_core_value(self, stat, value):
        self.set_core_current_value(stat, value)
        self.set_core_maximum_value(stat, value)

    def remove(self, stat):
        if stat in self._core_stats:
            del self._core_stats[stat]

    def get_current_value(self, stat):
        if stat in StatsEnum:
            stat_value = 0
            if stat in self._core_stats:
                stat_value += self._core_stats[stat].current

            responses = self.host.transmit_query(self, QueryType.StatModifier, stat=stat)
            for response in responses:
                if response:
                    stat_value += response.stat_modifier_value

            return stat_value

    def copy(self):
        copy_instance = Stats()
        copy_instance._core_stats = self._core_stats.copy()

        return copy_instance


def make_character_stats(health=0, strength=8, dexterity=8, constitution=8,
                         intelligence=8, charisma=8, wisdom=8, size=5, **kwargs):
    """Helper function to add common core character stats."""
    stats = Stats()
    stats.add_core_stat(StatsEnum.Health, health, health)
    stats.add_core_stat(StatsEnum.Strength, strength, strength)
    stats.add_core_stat(StatsEnum.Dexterity, dexterity, dexterity)
    stats.add_core_stat(StatsEnum.Constitution, constitution, constitution)
    stats.add_core_stat(StatsEnum.Intelligence, intelligence, intelligence)
    stats.add_core_stat(StatsEnum.Charisma, charisma, charisma)
    stats.add_core_stat(StatsEnum.Weight, wisdom, wisdom)
    stats.add_core_stat(StatsEnum.Size, size, size)

    return stats
