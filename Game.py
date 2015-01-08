#!/usr/bin/env python
"""

"""

import tdl

from tdl import map
from levelmanager import LevelManager

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 60

color_dark_blue_wall = (0, 0, 100)
color_dark_gray_wall = (75, 75, 75)
color_light_wall = (130, 110, 50)
color_dark_ground = (50, 50, 150)
color_light_ground = (200, 180, 50)

# Create a dictionary that maps keys to vectors.
# Names of the available keys can be found in the online documentation:
# http://packages.python.org/tdl/tdl.event-module.html
MOVEMENT_KEYS = {
    # standard arrow keys
    'UP': [0, -1],
    'DOWN': [0, 1],
    'LEFT': [-1, 0],
    'RIGHT': [1, 0],

    # diagonal keys
    # keep in mind that the keypad won't use these keys even if
    # num-lock is off
    'HOME': [-1, -1],
    'PAGEUP': [1, -1],
    'PAGEDOWN': [1, 1],
    'END': [-1, 1],

    # number-pad keys
    # These keys will always show as KPx regardless if num-lock
    # is on or off.  Keep in mind that some keyboards and laptops
    # may be missing a keypad entirely.
    # 7 8 9
    # 4   6
    # 1 2 3
    'KP1': [-1, 1],
    'KP2': [0, 1],
    'KP3': [1, 1],
    'KP4': [-1, 0],
    'KP6': [1, 0],
    'KP7': [-1, -1],
    'KP8': [0, -1],
    'KP9': [1, -1],
    }

tdl.setFont('terminal8x8_gs_ro.png')  # Configure the font.


# Create the root console.
console = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, 'Roguelike Game')

level_manager = None
level = None
dungeon = None
player = None
action_log = None
status_panel = None


def show_main_menu():
    menu_options = ['Play a new game', 'Quit']

    main_menu = tdl.Console(SCREEN_WIDTH, SCREEN_HEIGHT)

    menu(main_menu, menu_options)
    console.blit(main_menu, 0, 0)

    tdl.flush()

    key_event = tdl.event.keyWait()

    if key_event.keychar.upper() == 'A':
        new_game()
        play_game()
    elif key_event.keychar.upper() == 'B':
        # Halt the script using SystemExit
        raise SystemExit('The window has been closed.')


def menu(console, options):

    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')

    x = 20
    y = 20

    print_str(console, 'Welcome', x, y)
    y += 2
    print_str(console, 'Your goal is to find the Cone of Dunshire (!).', x, y)
    y += 2
    print_str(console, 'Use Caution as there are Trolls (T)and Orcs (o)', x, y)
    y += 1
    print_str(console, 'lurking in this dungeon!', x, y)
    y += 2

    letter_index = ord('a')
    x += 5
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        print_str(console, text, x, y)
        y += 2
        letter_index += 1


def print_str(console, string, x, y):
    console.move(x, y)
    console.printStr(string)
    console.move(x, y)


def new_game():
    global level_manager, level, dungeon, player, action_log, status_panel

    level_manager = LevelManager()
    level = level_manager.createLevel()
    dungeon = level_manager.dungeon
    player = dungeon.player

    action_log = tdl.Console(40, 15)
    action_log.move(0, 1)
    action_log.setMode('scroll')

    status_panel = tdl.Console(40, 15)


def isTransparent(x, y):

    try:
        if dungeon.map[x][y].block_sight and dungeon.map[x][y].blocked:
            return False
        else:
            return True
    except IndexError:
        pass


def render_gui():
    plHealth = player.name + " Health: " + str("%02d" % player.fighter.hp)
    status_panel.drawStr(0, 2, plHealth)
    console.blit(action_log, 0, 45)
    console.blit(status_panel, 41, 45)


def render_all():

    #go through all tiles, and set their background color
    for y in range(dungeon.height):
        for x in range(dungeon.width):
            wall = dungeon.map[x][y].block_sight
            if dungeon.map[x][y].explored:
                if wall:
                    console.drawChar(x, y, '#', fgcolor=color_dark_gray_wall)

    player.fov_coords = map.quickFOV(player.x, player.y, isTransparent, 'basic')

    for x, y in player.fov_coords:
        if dungeon.map[x][y].blocked is not False:
            console.drawChar(x, y, '#', fgcolor=color_light_wall)
            dungeon.map[x][y].explored = True

    render_gui()


def play_game():

    tdl.setTitle('Level 1')

    while True:  # Continue in an infinite game loop.

        console.clear()  # Blank the console.

        render_all()

        #draw all objects in the list
        for object in dungeon.objects:
            obj = object.get(player)
            if obj:
                console.drawChar(obj.x, obj.y, obj.char)

        if dungeon.player_state == 'dead':
            status_panel.drawStr(0, 4, 'You have died!')
        elif dungeon.player_state == 'done':
            # pdb.set_trace()
            status_panel.move(0, 4)
            status_panel.printStr('CONGRADULATIONS!\n\nYou have found a Cone of Dunshire!')

        tdl.flush()  # Update the window.

        for event in tdl.event.get():  # Iterate over recent events.
            if event.type == 'KEYDOWN':
                if dungeon.player_state == 'playing':
                    # We mix special keys with normal characters so we use keychar.
                    if event.keychar.upper() in MOVEMENT_KEYS:
                        # Get the vector and unpack it into these two variables.
                        keyX, keyY = MOVEMENT_KEYS[event.keychar.upper()]
                        # Then we add the vector to the current player position.

                        player.move_or_attack(keyX, keyY, dungeon, action_log)

                        #let monsters take their turn
                        if dungeon.player_state == 'playing':
                            for object in dungeon.objects:
                                if object.ai:
                                    object.ai.take_turn(dungeon, action_log)

                    else:
                        if event.keychar.upper() == 'G':
                            #pick up an item
                            for object in dungeon.objects:  # look for an item in the player's tile
                                if object.x == player.x and object.y == player.y and object.item:
                                    is_cone = object.item.pickUp(dungeon.objects, action_log)
                                    if is_cone:
                                        dungeon.player_wins(player)
                                    else:  # user picked up a health potion
                                        player.heal_damage()

            if event.type == 'QUIT':
                # Halt the script using SystemExit
                raise SystemExit('The window has been closed.')

show_main_menu()
