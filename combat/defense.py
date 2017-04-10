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

    def make_defense(self, attacker, defender, **kwargs):
        echo.EchoService.singleton.combat_context_echo(
            message="..." + self.message,
            attacker=attacker,
            defender=defender,
            **kwargs
        )

    def get_used_weapon(self, defender):
        return next((weapon for weapon in defender.equipment.get_wielded_items()))


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
        return self._evaluate(hit_roll, minimum_ac, maximum_ac)

    def make_defense(self, attacker, defender, **kwargs):
        defender_weapon = self.get_used_weapon(defender)
        super().make_defense(attacker, defender, defender_weapon=defender_weapon)


class BlockTemplate(DefenseTemplate):
    def __init__(self, name, description, message, requirements=None):
        super().__init__(name, description, message, requirements)

    def evaluate(self, attacker, hit_roll):
        minimum_ac = 10 + attacker.get_effective_dex_modifier()
        maximum_ac = minimum_ac + attacker.get_shield_modifiers()
        return self._evaluate(hit_roll, minimum_ac, maximum_ac)


class ArmorAbsorbTemplate(DefenseTemplate):
    def __init__(self, name, description, message, requirements=None):
        super().__init__(name, description, message, requirements)

    def evaluate(self, attacker, hit_roll):
        minimum_ac = 10 + attacker.get_effective_dex_modifier() + attacker.get_shield_modifiers()
        maximum_ac = minimum_ac + attacker.get_armor_modifiers()
        return self._evaluate(hit_roll, minimum_ac, maximum_ac)
