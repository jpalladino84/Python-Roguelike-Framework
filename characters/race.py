class Race(object):
    """
    Racial characteristics and bonuses
    """
    def __init__(self, uid, name):
        self.name = None


        # TODO THIS SHOULD DEFINE RACIAL BONUSES WITH A TREE OF GROWTH


class MetaRace(object):
    def __init__(self):
        self.name = None
        # TODO THIS SHOULD DEFINE ADDITIONAL BONUSES THAT ARE ADDED TO A BASE RACE
        # THE NAME OF THIS METACLASS WILL BE ADDED TO THE BASE RACE, EX Vampire Human


# TODO Move this OUT
orc = Race("orc", "Orc")
sample_races = []