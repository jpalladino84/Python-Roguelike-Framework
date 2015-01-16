"""
Character Classes
"""

from classes.base import Object

MAX_ENERGY = 3


class Fighter:
    #combat-related properties and methods (monster, player, NPC).
    def __init__(self, hp, defense, power, speed, death_function=None):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.death_function = death_function
        self.speed = speed
        #Fighters may act when they have energy = MAX_ENERGY. Fighters get speed energy back each iteration.
        #Make 3 a const somewhere.
        self.energy = speed

    def take_damage(self, damage):
        #apply damage if possible
        if damage > 0:
            self.hp -= damage

        #check for death. if there's a death function, call it
        if self.hp <= 0:
            function = self.death_function
            if function is not None:
                function(self.owner)

    def attack(self, target, console):
        #a simple formula for attack damage
        damage = self.power - target.fighter.defense
        resultStr = ''

        if damage > 0:
            #make the target take some damage
            resultStr = (self.owner.name.capitalize() +
                         ' attacks ' + target.name + ' for ' + str(damage) + ' hit points.\n\n')
            target.fighter.take_damage(damage)
        else:
            resultStr = (self.owner.name.capitalize() +
                         ' attacks ' + target.name + ' but it has no effect!\n\n')

        console.printStr(resultStr)


class BasicMonster:
    #AI for a basic monster.
    def take_turn(self, dungeon, console):
        #a basic monster takes its turn. If you can see it, it can see you
        monster = self.owner
        fighter = monster.fighter

        player = dungeon.player

        if (monster.x, monster.y) in player.fov_coords:

            fighter.energy = min(fighter.energy + fighter.speed, MAX_ENERGY)
            #monsters must have MAX_ENERGY energy to move.
            #Theoretically this restriction could be imposed on the player as well,
            #if the player was meant to be slower than some monsters- i.e. a dwarf player character
            #might have slower movement.
            if fighter.energy < MAX_ENERGY:
                return

            fighter.energy = 0
            #move towards player if far away
            if monster.distance_to(player) >= 2:
                monster.move_towards(player.x, player.y, dungeon)

            #close enough, attack! (if the player is still alive.)
            elif hasattr(player.fighter, 'hp') and player.fighter.hp > 0:
                monster.fighter.attack(player, console)


class Player(Object):

    def __init__(self, *args, **kwargs):
        Object.__init__(self, *args, **kwargs)
        self.fov_coords = set()

    def move_or_attack(self, dx, dy, dungeon, action_log):

        # the coordinates the player is moving to/attacking
        x = self.x + dx
        y = self.y + dy

        # try to find an attackable object there
        target = None

        for object in dungeon.objects:
            if object.fighter and object.x == x and object.y == y:
                target = object
                break

        # attack if target found, move otherwise
        if target is not None:
            self.fighter.attack(target, action_log)
        else:
            self.move(dx, dy, dungeon)

    def heal_damage(self):
        self.fighter.hp = min(self.fighter.hp + 10, self.fighter.max_hp)
