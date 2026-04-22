import random

from stats.enums import StatsEnum
from managers import echo
from util.colors import Colors
from util.dice import DiceStack, Dice


def execute_combat_round(attacker, defender):
    damage = _calculate_damage(attacker, defender)
    console = echo.EchoService.singleton.console
    console.printStr("{} hits {} for {} damage!\n".format(
        attacker.name, defender.name, damage))

    defender.stats.modify_core_current_value(StatsEnum.Health, -damage)

    if defender.stats.get_current_value(StatsEnum.Health) <= 0:
        if defender.is_player:
            player_death(defender, console)
        else:
            monster_death(defender, console, attacker)
        x, y = defender.location.get_local_coords()
        defender.current_level.maze[x][y].contains_object = False


def _calculate_damage(attacker, defender):
    damage_dice, _ = _get_weapon_damage(attacker)
    raw = sum(random.randint(1, damage_dice.dice.sides) for _ in range(damage_dice.amount))
    str_bonus = (attacker.stats.get_current_value(StatsEnum.Strength) - 10) // 2
    armor = max(0, defender.get_armor_class() - 10)
    return max(1, raw + str_bonus - armor)


def _get_weapon_damage(attacker):
    for item in attacker.equipment.get_wielded_items():
        weapon = item.get_component('weapon')
        if weapon and weapon.damage_dice:
            return weapon.damage_dice, item.name
    return DiceStack(1, Dice(4)), "fist"


def player_death(player, console):
    console.printStr('You have died... Game Over\n\n')
    player.display.ascii_character = '%'
    player.display.foreground_color = Colors.BLOOD_RED


def monster_death(monster, console, attacker=None):
    console.printStr('{} has died.\n\n'.format(monster.name))
    monster.display.ascii_character = '%'
    monster.display.foreground_color = Colors.BLOOD_RED
    monster.blocks = False
    monster.name = 'remains of ' + monster.name

    if attacker is not None and monster.xp_value > 0:
        levels_gained = attacker.experience_pool.add_experience(monster.xp_value)
        if levels_gained:
            console.printStr('You reached level {}!\n'.format(
                attacker.experience_pool.total_level))
