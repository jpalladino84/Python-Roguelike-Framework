import abc
from managers import echo


class DefenseTemplate(object):
    def __init__(self, name, description, message, requirements=None):
        self.name = name
        self.description = description
        self.message = message
        self.requirements = requirements

    @abc.abstractmethod
    def evaluate(self, attacker, hit_roll):
        pass

    def _evaluate(self, hit_roll, minimum_ac, maximum_ac):
        if hit_roll > minimum_ac < maximum_ac:
            return True
        return False


class MissTemplate(DefenseTemplate):
    def __init__(self, name, description, message, requirements=None):
        super().__init__(name, description, message, requirements)

    def evaluate(self, attacker, hit_roll):
        return True


class DodgeTemplate(DefenseTemplate):
    def __init__(self, name, description, message, requirements=None):
        super().__init__(name, description, message, requirements)

    def evaluate(self, attacker, hit_roll):
        if hit_roll > 10 < 10 + attacker.get_effective_dex_modifier():
            return True
        return False


class ParryTemplate(DefenseTemplate):
    def __init__(self, name, description, message, requirements=None):
        super().__init__(name, description, message, requirements)

    def evaluate(self, attacker, hit_roll):
        # TODO A parry should have a different condition than a dodge.
        minimum_ac = 10
        maximum_ac = minimum_ac + attacker.get_effective_dex_modifier()
        self._evaluate(hit_roll, minimum_ac, maximum_ac)


class BlockTemplate(DefenseTemplate):
    def __init__(self, name, description, message, requirements=None):
        super().__init__(name, description, message, requirements)

    def evaluate(self, attacker, hit_roll):
        minimum_ac = 10 + attacker.get_effective_dex_modifier()
        maximum_ac = minimum_ac + attacker.get_shield_modifiers()
        self._evaluate(hit_roll, minimum_ac, maximum_ac)


class ArmorAbsorb(DefenseTemplate):
    def __init__(self, name, description, message, requirements=None):
        super().__init__(name, description, message, requirements)

    def evaluate(self, attacker, hit_roll):
        minimum_ac = 10 + attacker.get_effective_dex_modifier() + attacker.get_shield_modifiers()
        maximum_ac = minimum_ac + attacker.get_armor_modifiers()
        self._evaluate(hit_roll, minimum_ac, maximum_ac)


# TODO Move this out
dodge = DodgeTemplate(
    name="Dodge",
    description="Standard move out of the way.",
    message="{You} dodge it.",
)
parry = ParryTemplate(
    name="Parry",
    description="Standard parry weapon with weapon.",
    message="{You} parry it with {your} {defender_weapon} !"
)
block = BlockTemplate(
    name="Block",
    description="Standard block something with something.",
    message="{You} block it with {your} {defender_weapon}"
)
armor_absorb = ArmorAbsorb(
    name="Armor Absorb",
    description="Standard armor saves your ass.",
    message="The hit is absorbed by {defender_bodypart_armor}"
)
base_defenses = [
    dodge, parry, block, armor_absorb
]