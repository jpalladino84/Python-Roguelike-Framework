from .component import Component

# TODO Material needs a serious overhaul to fit in D&D system.
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

    def copy(self):
        return Material(uid=self.uid, name=self.name, hardness=self.hardness, sharpness=self.sharpness,
                        potency=self.potency, weight=self.weight, value=self.value)
