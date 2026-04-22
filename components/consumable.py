from components.component import Component


class Consumable(Component):
    NAME = "consumable"

    def __init__(self, use_effect):
        super().__init__()
        self.use_effect = use_effect  # callable(user) -> str message

    def use(self, user):
        return self.use_effect(user)

    def copy(self):
        return Consumable(self.use_effect)
