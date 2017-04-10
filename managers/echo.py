from characters.enums import Sex
from enum import Enum
from collections import defaultdict


class EchoService(object):
    # TODO This makes me cry, lets refactor this.
    singleton = None

    def __init__(self, console, game_context):
        self.console = console
        self.game_context = game_context
        if not EchoService.singleton:
            EchoService.singleton = self

    def combat_context_echo(self, message, attacker=None, defender=None,
                            attacker_weapon=None, defender_weapon=None, defender_bodypart=None):
        context_variables = defaultdict(lambda: "N/A")
        context_variables["player"] = self.game_context.player

        if attacker:
            context_variables["attacker"] = attacker
        if defender:
            context_variables["defender"] = defender
        if attacker_weapon:
            context_variables["attacker_weapon"] = attacker_weapon
        if defender_weapon:
            context_variables["defender_weapon"] = defender_weapon
        if defender_bodypart:
            context_variables["defender_bodypart"] = defender_bodypart

        for context_variable in context_variables.keys():
            if context_variable in message_router:
                context_variables[context_variable] = message_router[context_variable](**context_variables)

        for variable in MessageVariables:
            if variable.value in message and not variable.name in context_variables and variable.name in message_router:
                context_variables[variable.name] = message_router[variable.name](**context_variables)

        formatted_message = message.format(**context_variables)
        self.console.printStr(formatted_message + "\n")


class MessageVariables(Enum):
    attacker = "{attacker}"
    attacker_weapon = "{attacker_weapon}"
    attacker_his = "{attacker_his}"
    attacker_him = "{attacker_him}"
    attacker_he = "{attacker_he}"
    defender = "{defender}"
    defender_his = "{defender_his}"
    defender_him = "{defender_him}"
    defender_he = "{defender_he}"
    defender_bodypart = "{defender_bodypart}"
    defender_armor = "{defender_armor}"
    defender_weapon = "{defender_weapon}"


def his_her_it(target, **kwargs):
    if 'player' in kwargs and kwargs['player'] == target:
        return "your"

    if hasattr(target, 'sex'):
        if target.sex == Sex.Male:
            return "his"
        if target.sex == Sex.Female:
            return "her"
    return "its"


def him_her_it(target, **kwargs):
    if 'player' in kwargs and kwargs['player'] == target:
        return "your"

    if hasattr(target, 'sex'):
        if target.sex == Sex.Male:
            return "him"
        if target.sex == Sex.Female:
            return "her"
    return "its"


def he_her_it(target, **kwargs):
    if 'player' in kwargs and kwargs['player'] == target:
        return "You"

    if hasattr(target, 'sex'):
        if target.sex == Sex.Male:
            return "he"
        if target.sex == Sex.Female:
            return "her"
    return "it"


def name_or_you(target, **kwargs):
    if 'player' in kwargs and kwargs['player'] == target:
        return "You"

    return target.name


message_router = {
    MessageVariables.attacker_his.name: lambda **kwargs: his_her_it(target=kwargs["attacker"], **kwargs),
    MessageVariables.attacker_him.name: lambda **kwargs: him_her_it(target=kwargs["attacker"], **kwargs),
    MessageVariables.attacker.name: lambda **kwargs: name_or_you(target=kwargs["attacker"], **kwargs),
    MessageVariables.attacker_weapon.name: lambda **kwargs: kwargs.get("attacker_weapon").name,
    MessageVariables.attacker_he.name: lambda **kwargs: he_her_it(target=kwargs.get("attacker")),
    MessageVariables.defender_his.name: lambda **kwargs: his_her_it(target=kwargs["defender"], **kwargs),
    MessageVariables.defender_him.name: lambda **kwargs: him_her_it(target=kwargs["defender"], **kwargs),
    MessageVariables.defender_he.name: lambda **kwargs: he_her_it(target=kwargs.get("defender")),
    MessageVariables.defender.name: lambda **kwargs: name_or_you(target=kwargs["defender"], **kwargs),
    MessageVariables.defender_weapon.name: lambda **kwargs: kwargs.get("defender_weapon").name,
    MessageVariables.defender_bodypart.name: lambda **kwargs: kwargs.get("defender_bodypart").name,
}
