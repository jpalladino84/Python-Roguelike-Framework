from .component import Component


class Material(Component):
    NAME = "material"
    """
    This defines a material that is used in other compositions like items/tiles.
    """
    def __init__(self, uid, name="", hardness=0.0, sharpness=0.0, potency=0.0, weight=0.0, value=0.0):
        super().__init__()
        self.uid = uid
        self.name = name
        self.hardness = hardness
        self.sharpness = sharpness
        self.potency = potency
        self.weight = weight
        self.value = value

    def __str__(self):
        return "Material({})".format(self.name)
