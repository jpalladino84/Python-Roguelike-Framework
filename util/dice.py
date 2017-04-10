class Dice(object):
    __slots__ = ['sides']

    def __init__(self, sides):
        self.sides = sides


class DiceStack(object):
    __slots__ = ['amount', 'dice']

    def __init__(self, amount, dice):
        self.amount = amount
        self.dice = dice