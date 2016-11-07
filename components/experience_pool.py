from math import floor


class ExperiencePool(object):
    """
    This pool will hold experience and a list of other pools it can trickle to.
    Example: A Character has a pool that holds all the experience he gains.
    He has a race Orc, a class Warrior and a subclass Berserker.
    When he gains 500 xp, 250 goes to orc, 250 goes to warrior and 125 goes to berserker.
    Once he reaches max level of Orc then the full amount goes to warrior, which gives half of what it has to berserker.
    """
    def __init__(self):
        self.experience = 0
        self.child_pools = []

    def add_child_pool(self, child_pool):
        self.child_pools.append(child_pool)

    def remove_child_pool(self, child_pool):
        self.child_pools.remove(child_pool)

    def add_experience(self, experience_amount):
        divided_experience = experience_amount / len(self.child_pools) if self.child_pools else experience_amount
        self.experience += divided_experience
        for child_pool in self.child_pools:
            child_pool.add_experience(divided_experience)

    def remove_experience(self, experience_amount):
        divided_experience = experience_amount / len(self.child_pools) if self.child_pools else experience_amount
        self.experience -= divided_experience
        for child_pool in self.child_pools:
            child_pool.remove_experience(divided_experience)

    def get_total_levels(self):
        levels = self.get_pool_level()
        for child_pool in self.child_pools:
            levels += child_pool.get_pool_level()
        return levels

    def get_pool_level(self):
        return floor(self.experience / 5000)
