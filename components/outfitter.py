import random
from .component import Component
from data.python_templates.outfits import outfits


class Outfitter(Component):
    """ Component outfitting a character. """
    def __init__(self, outfit_uids):
        super().__init__()
        self.outfit_uids = outfit_uids
        self.is_on_template = True

    # TODO This component must unregister and apply an outfit to a host.
    # TODO Maybe on Update?


    def on_register(self, host):
        random_outfit = random.choice([outfit for outfit in outfits if outfit.uid in self.outfit_uids])
        random_outfit.apply(self.host)

