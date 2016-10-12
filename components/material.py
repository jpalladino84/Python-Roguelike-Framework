class Material(object):
    """
    This defines a material that is used in other compositions like items/tiles.
    """
    def __init__(self, name, hardness, sharpness, potency, weight, value):
        self.name = name
        self.hardness = hardness
        self.sharpness = sharpness
        self.potency = potency
        self.weight = weight
        self.value = value



# This is here until it can be moved to a json where it belongs
Bone = Material('Bone', 1, 1, 1, 1, 0.1)
Skin = Material('Skin', 0.1, 0, 1, 0.1, 0.1)
Flesh = Material('Flesh', 0.2, 0, 1, 0.2, 0.1)
Wood = Material('Wood', 1, 0.5, 1, 0.5, 1)
Stone = Material('Stone', 2, 1, 0.5, 2, 0.5)
Iron = Material('Iron', 2, 2, 1, 2, 1)

