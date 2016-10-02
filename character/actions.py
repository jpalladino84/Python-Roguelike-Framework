"""
Action commands

This is where the main business logic lives.

Any action that can be taken by the player or a npc (e.g. monster) is defined here.
"""
import json
import math

from . import models
from settings import Colors
from managers.console_manager import CONSOLES
from dungeon.models import DungeonObject


def attack(attacker, target, maze):
    # a simple formula for attack damage
    damage = attacker.character_class.attack - target.character_class.defense
    if damage > 0:
        # make the target take some damage
        take_damage(target, damage, maze)
    else:
        CONSOLES['action_log'].printStr('{} brushes off the attack.\n\n'.format(target.name))


def player_death(player):
    # the game ended!
    CONSOLES['action_log'].printStr('You have died... Game Over\n\n')
    player.character_state = 'dead'

    # for added effect, transform the player into a corpse!
    player.ascii_char = '%'
    player.fgcolor = json.dumps(Colors.BLOOD_RED)
    player.save()


def monster_death(monster):
    # transform it into a nasty corpse! it doesn't block, can't be
    # attacked and doesn't move
    CONSOLES['action_log'].printStr('{} has died.\n\n'.format(monster.name))
    monster.ascii_char = '%'
    monster.fgcolor = json.dumps(Colors.BLOOD_RED)
    monster.blocks = False
    monster.character_state = 'dead'
    monster.name = 'remains of ' + monster.name
    monster.save()


def take_damage(a, damage, maze):
    # apply damage if possible
    if damage > 0:
        CONSOLES['action_log'].printStr('{} takes {} damage.\n\n'.format(a.name, damage))
        a.character_class.hp -= damage
        a.character_class.save()

    # check for death. if there's a death function, call it
    if a.character_class.hp <= 0:
        if a.name == 'player':
            player_death(a)
        else:
            monster_death(a)

        x, y = json.loads(a.dungeon_object.coords)
        maze[x][y].contains_object = False


def move(a, dx, dy, maze):
    x, y = json.loads(a.dungeon_object.coords)
    new_x = x + dx
    new_y = y + dy

    old_tile = maze[x][y]
    new_tile = maze[new_x][new_y]

    # move by the given amount, if the destination is not blocked
    if not new_tile.is_blocked:
        a.dungeon_object.coords = json.dumps((new_x, new_y))
        a.dungeon_object.save()
        old_tile.contains_object = False
        new_tile.contains_object = True


def move_towards(a, b, maze):
    ax, ay = json.loads(a.dungeon_object.coords)
    bx, by = json.loads(b.dungeon_object.coords)
    # vector from this object to the target, and distance
    dx = bx - ax
    dy = by - ay
    distance = math.sqrt(dx ** 2 + dy ** 2)

    # normalize it to length 1 (preserving direction), then round it and
    # convert to integer so the movement is restricted to the map grid
    dx = int(round(dx / distance))
    dy = int(round(dy / distance))
    move(a, dx, dy, maze)


def distance_to(a, b):
    ax, ay = json.loads(a.dungeon_object.coords)
    bx, by = json.loads(b.dungeon_object.coords)

    # return the distance to another object
    dx = bx - ax
    dy = by - ay
    return math.sqrt(dx ** 2 + dy ** 2)


def player_move_or_attack(player, dx, dy, maze):
    """
    Player turn, either move to a new tile or attack
    whatever is in your way.
    """
    # the coordinates the player is moving to/attacking
    x, y = json.loads(player.dungeon_object.coords)
    new_x = x + dx
    new_y = y + dy
    new_tile = maze[new_x][new_y]

    # try to find an attack-able object there
    if new_tile.contains_object:
        tile_coords = json.dumps((new_tile.x, new_tile.y))
        try:
            monster = (models.Character.select().join(DungeonObject).where(
                DungeonObject.coords == tile_coords
            ).get())
            CONSOLES['action_log'].printStr('Player attacks {}...\n\n'.format(monster.name))
            attack(player, monster, maze)
        except models.Character.DoesNotExist:
            pass
    else:
        move(player, dx, dy, maze)


def heal_damage(a):
    a.character_class.hp = min(a.character_class.hp + 10, a.character_class.max_hp)


def monster_take_turn(monster, player, maze):
    """
    A basic monster takes its turn.
    If you can see it, it can see you
    """
    if monster.character_state == 'alive':
        x, y = json.loads(monster.dungeon_object.coords)
        if (x, y) in player.fov:

            # move towards player if far away
            if distance_to(monster, player) >= 2:
                move_towards(monster, player, maze)

            # close enough, attack! (if the player is still alive.)
            elif player.character_class.hp > 0:
                CONSOLES['action_log'].printStr('{} attacks player...\n\n'.format(monster.name))
                attack(monster, player, maze)


def get_item(character, item, tile_x, tile_y):
    character.inventory.add_item(item)
