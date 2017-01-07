"""
Action commands

This is where the main business logic lives.

Any action that can be taken by the player or a npc (e.g. monster) is defined here.
"""
import math
import random

from components.colors import Colors
from managers.console_manager import CONSOLES

# TODO One thing I want to change is the tile contains flag
# TODO It should not have to be changed EVERY time something moves, instead we should
# TODO Abstract it to another layer which would handle WHATEVER it needs to move something
# TODO Because many actions will move characters and not all of them will make it "walk"
# TODO also because it only take one forgotten line to make difficult to track bugs.


def attack(attacker, target):
    # a simple formula for attack damage
    hitroll = random.randint(1, 20)
    damroll = random.randint(1, 4)
    hit_check = int(attacker.get_attack()) + hitroll - int(target.get_defense())
    if hit_check > 0:
        # make the target take some damage
        take_damage(target, damroll)
    else:
        CONSOLES['action_log'].printStr('{} dodges the attack.\n\n'.format(target.name))


def player_death(player):
    # TODO This should not be here
    # the game ended!
    CONSOLES['action_log'].printStr('You have died... Game Over\n\n')
    player.character_state = 'dead'

    # for added effect, transform the player into a corpse!
    player.ascii_char = '%'
    player.display_foreground_color = Colors.BLOOD_RED
    player.save()


def monster_death(monster):
    # TODO This should not be here
    # transform it into a nasty corpse! it doesn't block, can't be
    # attacked and doesn't move
    CONSOLES['action_log'].printStr('{} has died.\n\n'.format(monster.name))
    monster.ascii_char = '%'
    monster.display.foreground_color = Colors.BLOOD_RED
    monster.blocks = False
    monster.character_state = 'dead'
    monster.name = 'remains of ' + monster.name


def take_damage(actor, damage):
    # TODO This should not be here
    # apply damage if possible
    if damage > 0:
        CONSOLES['action_log'].printStr('{} takes {} damage.\n\n'.format(actor.name, damage))
        actor.get_health().modify_current(-damage)

    # check for death. if there's a death function, call it
    if int(actor.get_health()) <= 0:
        if actor.name == 'player':
            player_death(actor)
        else:
            monster_death(actor)

        x, y = actor.location.get_local_coords()
        actor.current_level.maze[x][y].contains_object = False


def move(actor, dx, dy):
    x, y = actor.location.get_local_coords()
    new_x = x + dx
    new_y = y + dy

    old_tile = actor.current_level.maze[x][y]
    new_tile = actor.current_level.maze[new_x][new_y]

    # move by the given amount, if the destination is not blocked
    if not new_tile.is_blocked:
        actor.location.local_x = new_x
        actor.location.local_y = new_y
        old_tile.contains_object = False
        new_tile.contains_object = True


def move_towards(actor, target):
    # TODO I think this should be split,  a part that determines in which direction you have to move
    # TODO then reuse the part where we try to move instead.
    # TODO Because we will be able to reuse it for missiles/spells
    actor_x, actor_y = actor.location.get_local_coords()
    target_x, target_y = target.location.get_local_coords()
    # vector from this object to the target, and distance
    distance_x = target_x - actor_x
    distance_y = target_y - actor_y
    distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

    # normalize it to length 1 (preserving direction), then round it and
    # convert to integer so the movement is restricted to the map grid
    distance_x = int(round(distance_x / distance))
    distance_y = int(round(distance_y / distance))
    move(actor, distance_x, distance_y)


def distance_to(actor, target):
    # TODO This should not be here
    actor_x, actor_y = actor.location.get_local_coords()
    target_x, target_y = target.location.get_local_coords()

    # return the distance to another object
    distance_x = target_x - actor_x
    distance_y = target_y - actor_y
    return math.sqrt(distance_x ** 2 + distance_y ** 2)


def move_or_attack(character, target_x, target_y):
    """
    Either move to a new tile or attack
    whatever is in your way.
    """
    # the coordinates the player is moving to/attacking
    x = character.location.local_x
    y = character.location.local_y
    new_x = x + target_x
    new_y = y + target_y
    new_tile = character.current_level.maze[new_x][new_y]

    # try to find an attack-able object there
    if new_tile.contains_object:
        tile_coords = (new_tile.x, new_tile.y)
        monster = next((monster for monster in character.current_level.spawned_monsters
                        if monster.location.get_local_coords() == tile_coords))
        if monster:
            CONSOLES['action_log'].printStr('Player attacks {}...\n\n'.format(monster.name))
            attack(character, monster)
    else:
        move(character, target_x, target_y)


def heal_damage(a):
    # TODO This should not be here, also the amount must be able to vary
    a.character_class.hp = min(a.character_class.hp + 10, a.character_class.max_hp)


def monster_take_turn(monster, player):
    # TODO This should not be here, it should be in an AI component which uses actions from here
    """
    A basic monster takes its turn.
    If you can see it, it can see you
    """
    if not monster.is_dead:
        x, y = monster.location.get_local_coords()
        if (x, y) in player.fov:

            # move towards player if far away
            if distance_to(monster, player) >= 2:
                move_towards(monster, player)

            # close enough, attack! (if the player is still alive.)
            elif player.character_class.hp > 0:
                CONSOLES['action_log'].printStr('{} attacks player...\n\n'.format(monster.name))
                attack(monster, player)


def get_item(character, item, tile_x, tile_y):
    character.inventory.add_item(item)
