from characters.enums import Sex
from enum import Enum


class MessageVariables(Enum):
    attacker_his_her_it = "%Ahis"
    attacker_him_her_it = "%Ahim"
    attacker_or_you_name = "%A"
    defender_his_her_it = "%Dhis"
    defender_him_her_it = "%Dhim"
    defender_or_you_name = "%D"
    target_bodypart = "%BP"
    weapon_used = "%WP"


def his_her_it(target, **kwargs):
    if hasattr(target, 'sex'):
        if target.sex == Sex.Male:
            return "his"
        if target.sex == Sex.Female:
            return "her"
    return "it"


def him_her_it(target, **kwargs):
    if hasattr(target, 'sex'):
        if target.sex == Sex.Male:
            return "him"
        if target.sex == Sex.Female:
            return "her"
    return "it"


def name_or_you(target, player, **kwargs):
    if target == player:
        return "you"
    return target.name


message_router = {
    MessageVariables.attacker_his_her_it: lambda **kwargs: his_her_it(target=kwargs["attacker"], **kwargs),
    MessageVariables.attacker_him_her_it: lambda **kwargs: him_her_it(target=kwargs["attacker"], **kwargs),
    MessageVariables.attacker_or_you_name: lambda **kwargs: name_or_you(target=kwargs["attacker"], **kwargs),
    MessageVariables.defender_his_her_it: lambda **kwargs: his_her_it(target=kwargs["defender"], **kwargs),
    MessageVariables.defender_him_her_it: lambda **kwargs: him_her_it(target=kwargs["defender"], **kwargs),
    MessageVariables.defender_or_you_name: lambda **kwargs: name_or_you(target=kwargs["defender"], **kwargs)
}


def apply_variables_to_attack_message(message, attacker, defender, player):
    for variable in MessageVariables:
        if variable.value in message:
            message.replace(
                variable.value,
                message_router[variable.value](attacker, defender, player)
            )