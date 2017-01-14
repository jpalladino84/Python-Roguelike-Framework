from characters import actions


class ActionManager(object):
    def __init__(self, action_log_console):
        self.action_log_console = action_log_console

    def move_or_attack(self, player, key_x, key_y):
        actions.move_or_attack(player, key_x, key_y, self.action_log_console)

    def monster_take_turn(self, monster, player):
        actions.monster_take_turn(monster, player, self.action_log_console)
