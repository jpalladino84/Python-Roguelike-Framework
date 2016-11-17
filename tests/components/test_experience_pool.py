from components.experience_pool import ExperiencePool


def test_experience_pools_split():
    race_pool = ExperiencePool()
    class_pool = ExperiencePool()
    subclass_pool = ExperiencePool()

    race_pool.add_child_pool(class_pool)
    class_pool.add_child_pool(subclass_pool)

    race_pool.add_experience(500)
    assert race_pool.experience == 250
    assert class_pool.experience == 125
    assert subclass_pool.experience == 125
