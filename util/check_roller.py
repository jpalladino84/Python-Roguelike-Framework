import random
"""
A helper module for making rolls.
"""


def d20_check_roll(difficulty_class, modifiers=0, advantage=None):
    """
    :param difficulty_class: Target for Success
    :param modifiers: Total amount of modifiers
    :param advantage: If is applicable, True if advantage, False if disadvantage.
    :return: Bool Tuple Success, Critical
    """
    natural_roll = random.randint(1, 20)
    additional_roll = random.randint(1, 20)
    final_roll = natural_roll
    if advantage is not None:
        if advantage:
            final_roll = natural_roll if natural_roll > additional_roll else additional_roll
        else:
            final_roll = natural_roll if natural_roll < additional_roll else additional_roll

    if final_roll == 1:
        return False, True
    if final_roll == 20:
        return True, True
    if final_roll + modifiers >= difficulty_class:
        return True, False

    return False, False


def roll_damage(dice_stacks, modifiers, critical=False):
    """
    :param dice_stacks: Stacks of Dice to apply
    :param modifiers: Total of modifiers affecting the roll
    :param critical: If is a critical damage roll
    :return: Total damage to apply.
    """
    if critical:
        dice_stacks = dice_stacks.extend(dice_stacks.copy())

    total_dice_result = 0
    for dice_stack in dice_stacks:
        for i in range(0, dice_stack.amount):
            total_dice_result += random.randint(1, dice_stack.sides)

    return total_dice_result + modifiers
