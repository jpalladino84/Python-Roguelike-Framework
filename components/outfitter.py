import random
from .component import Component
from data.python_templates.outfits import outfits


class Outfitter(Component):
    """ Component outfitting a character. """
    def __init__(self, outfit_uids):
        super().__init__()
        self.outfit_uids = outfit_uids
        self.is_on_template = True

    def copy(self):
        copy_instance = Outfitter(self.outfit_uids)
        copy_instance.is_on_template = False
        return copy_instance

    def on_register(self, host):
        if not self.is_on_template:
            random_outfit = random.choice([outfit for outfit in outfits if outfit.uid in self.outfit_uids])
            random_outfit.apply(self.host)
            self.host.unregister_component(self)

