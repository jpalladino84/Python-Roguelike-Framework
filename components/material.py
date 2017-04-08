from .component import Component


class Material(Component):
    """
    This defines a material that is used in other compositions like items/tiles.
    """
    def __init__(self, uid, name="", hardness=0.0, sharpness=0.0, potency=0.0, weight=0.0, value=0.0):
        self.uid = uid
        self.name = name
        self.hardness = hardness
        self.sharpness = sharpness
        self.potency = potency
        self.weight = weight
        self.value = value

    def __str__(self):
        return "Material({})".format(self.name)


# This is here until it can be moved to a json where it belongs
Bone = Material('bone', 'Bone', 1, 1, 1, 1, 0.1)
Skin = Material('skin', 'Skin', 0.1, 0, 1, 0.1, 0.1)
Flesh = Material('flesh', 'Flesh', 0.2, 0, 1, 0.2, 0.1)
Wood = Material('wood', 'Wood', 1, 0.5, 1, 0.5, 1)
Stone = Material('stone', 'Stone', 2, 1, 0.5, 2, 0.5)
Iron = Material('iron', 'Iron', 2, 2, 1, 2, 1)


materials = [
    Bone,
    Skin,
    Flesh,
    Wood,
    Stone,
    Iron
]
