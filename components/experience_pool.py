from .component import Component
from .messages import QueryType

advancement_table = {
    1: 0,
    2: 300,
    3: 900,
    4: 2700,
    5: 6500,
    6: 14000,
    7: 23000,
    8: 34000,
    9: 48000,
    10: 64000,
    11: 85000,
    12: 100000,
    13: 120000,
    14: 140000,
    15: 165000,
    16: 195000,
    17: 225000,
    18: 265000,
    19: 305000,
    20: 355000
}


class ExperiencePool(Component):
    NAME = "experience_pool"
    """
    This pool will hold total EXP and levels for each registered pool.
    """
    STARTING_LEVEL = 1
    SOFT_MAX_LEVEL = 20

    def __init__(self):
        super().__init__()
        self.total_level = 1
        self.unspent_levels = 0
        self.experience = 0
        self.child_pools = {}
        self.on_level_up = None  # callable(new_level), set by host

    def copy(self):
        new_copy = ExperiencePool()
        new_copy.total_level = self.total_level
        new_copy.unspent_levels = self.unspent_levels
        new_copy.experience = self.experience
        new_copy.child_pools = self.child_pools.copy()
        return new_copy

    def on_register(self, host):
        super().on_register(host)
        self.host.register_query_responder(self, QueryType.ExperiencePool, self.respond_experience_pool)

    def respond_experience_pool(self, name):
        if name not in self.child_pools:
            self.child_pools[name] = 1  # child pools start at level 1

        return lambda: self.child_pools[name]

    def assign_level(self, pool_name):
        if self.unspent_levels > 0 and pool_name in self.child_pools:
            self.child_pools[pool_name] += 1
            self.unspent_levels -= 1

    def get_xp_for_next_level(self):
        next_level = self.total_level + 1
        if next_level > self.SOFT_MAX_LEVEL:
            return advancement_table[self.SOFT_MAX_LEVEL] + (next_level - self.SOFT_MAX_LEVEL) * 50000
        return advancement_table[next_level]

    def add_experience(self, experience_amount):
        self.experience += experience_amount
        levels_gained = 0
        while self.experience >= self.get_xp_for_next_level():
            self.total_level += 1
            self.unspent_levels += 1
            levels_gained += 1
            for name in self.child_pools:
                self.child_pools[name] += 1
            if self.on_level_up:
                self.on_level_up(self.total_level)
        return levels_gained

    def remove_experience(self, experience_amount):
        level_exp_threshold = advancement_table.get(self.total_level, 0)
        new_value = self.experience - experience_amount
        if new_value < level_exp_threshold:
            new_value = level_exp_threshold
        self.experience = new_value
