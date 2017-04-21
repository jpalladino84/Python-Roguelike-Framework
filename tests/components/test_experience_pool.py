import unittest

from components.experience_pool import ExperiencePool


class ExperiencePool(unittest.TestCase):

    def test_experience_pools_split(self):
        race_pool = ExperiencePool()
        class_pool = ExperiencePool()
        subclass_pool = ExperiencePool()

        race_pool.add_child_pool(class_pool)
        class_pool.add_child_pool(subclass_pool)

        race_pool.add_experience(500)
        self.assertEqual(race_pool.experience, 250)
        self.assertEqual(class_pool.experience, 125)
        self.assertEqual(subclass_pool.experience, 125)
