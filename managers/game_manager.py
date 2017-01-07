from enum import Enum

import settings
import tdl
from areas.level import Level
from characters import actions
from data.json_template_loader import JsonTemplateManager
from factories.body_factory import BodyFactory
from factories.character_factory import CharacterFactory
from factories.factory_service import FactoryService
from generators.dungeon_generator import DungeonGenerator
from managers.console_manager import ConsoleManager, CONSOLES
from managers.scene_manager import SceneManager
from tdl import map


class GameState(Enum):
    PLAYING = 0
    ENDED = 1


class GameManager(object):
    """
    Game Manager: Handles setup and progression of the game

    Admittedly this is a bit of a mess and will need to be cleaned up.
    """
    game_state = GameState.PLAYING

    player_action = None
    player = None
    monsters = []
    items = []
    show_inventory = False

    colors = settings.DUNGEON_COLORS
    movement_keys = settings.KEY_MAPPINGS
    console_manager = ConsoleManager()

    def __init__(self):
        # Pre-load levels into database
        self.loaded_levels = []
        self.factory_service = None
        self.load_game_data()
        self.dungeon_generator = DungeonGenerator(self.factory_service)
        self.scene_manager = SceneManager(self.console_manager)

    def start(self):
        self.scene_manager.current_scene.render()
        while True:  # Continue in an infinite game loop.
            self.game_state = GameState.PLAYING if not self.player.is_dead() else None
            self.console_manager.main_console.clear()  # Blank the console.
            self.scene_manager.render()
            self.scene_manager.handle_input()

    def new_game(self):
        # TODO This should prepare the first level
        level = Level()
        level.name = "DEFAULT"
        level.min_room_size = 1
        level.max_room_size = 10
        level.max_rooms = 10
        level.width = 80
        level.height = 45
        tdl.setTitle(level.name)
        self.init_dungeon(level)

    def init_dungeon(self, level):
        # TODO The player must be built and retrieved here.
        self.player = self.monsters[0]
        level.monster_spawn_list = self.monsters
        self.dungeon_generator.generate(level, self.player)

    def player_wins(self):
        # the game ended
        self.game_state = GameState.ENDED



    def play_game(self):
        """
        The main game loop
        """
        while True:  # Continue in an infinite game loop.
            self.game_state = GameState.PLAYING if not self.player.is_dead() else None
            self.console_manager.main_console.clear()  # Blank the console.
            self.render_all()

            if self.player.is_dead():
                CONSOLES['status'].drawStr(0, 4, 'You have died!')

            # TODO: Fix win condition
            # elif player.character_state == 'done':
            #     STATUS.move(0, 4)
            #     STATUS.printStr('CONGRATULATIONS!\n\nYou have found a Cone of Dunshire!')

            tdl.flush()  # Update the window.
            self.listen_for_events()

    def listen_for_events(self):
        """
        Any keyboard interaction from the user occurs here
        """
        # TODO We need a binding system.
        # TODO Possibly just a dictionary with keyboard input as keys and Action Enum as value
        for event in tdl.event.get():  # Iterate over recent events.
            if event.type == 'KEYDOWN':
                if self.game_state == GameState.PLAYING:

                    # TODO: Fix inventory system
                    # if self.show_inventory:
                    #     if event.keychar in self.player.inventory:
                    #         self.player.heal_damage()
                    #         del self.player.inventory[event.keychar]
                    #     elif event.keychar.upper() == 'I':
                    #         self.show_inventory = False
                    #         tdl.setTitle(self.level.name)

                    # We mix special keys with normal characters so we use keychar.
                    if event.keychar.upper() in self.movement_keys:
                        # Get the vector and unpack it into these two variables.
                        key_x, key_y = self.movement_keys[event.keychar.upper()]
                        # Then we add the vector to the current player position.

                        # player moves or attacks in the specified direction
                        actions.move_or_attack(self.player, key_x, key_y)

                        # TODO: Fix the stairs
                        # if (self.areas.stairs and
                        #    (self.areas.stairs.x, self.areas.stairs.y) == (self.player.x, self.player.y)):
                        #     self.next_level()

                        # let monsters take their turn
                        if self.game_state == GameState.PLAYING:
                            for monster in self.monsters:
                                actions.monster_take_turn(monster, self.player, self.maze)

                    # TODO: Fix pick up and inventory menu functions
                    # else:
                    #     if event.keychar.upper() == 'G':
                    #         # pick up an items
                    #         for object in self.areas.objects:  # look for an items in the player's tile
                    #             if object.x == self.player.x and object.y == self.player.y and object.items:
                    #                 is_cone = object.items.pickUp(self.areas.objects)
                    #                 if is_cone:
                    #                     self.player_wins()
                    #                 else:  # user picked up a health potion
                    #                     letter_index = ord('a')
                    #
                    #                     while chr(letter_index) in self.player.inventory:
                    #                         letter_index += 1
                    #
                    #                     self.player.inventory[chr(letter_index)] = object
                    #
                    #     elif event.keychar.upper() == 'I':
                    #         if len(self.player.inventory) > 0 and self.show_inventory is False:
                    #             self.show_inventory = True

            if event.type == 'QUIT':
                # Halt the script using SystemExit
                raise SystemExit('The window has been closed.')

    def load_game_data(self):
        """
        This is where the data is loaded.
        """
        # TODO This should load all templates to be instantiated later.
        json_template_loader = JsonTemplateManager()
        self.factory_service = FactoryService(
            template_loader=json_template_loader,
            body_factory=BodyFactory(json_template_loader.bodies_templates),
        )
        character_factory = CharacterFactory(
            character_templates=json_template_loader.monster_templates,
            factory_service=self.factory_service,
            race_templates=json_template_loader.race_templates,
            class_templates=json_template_loader.class_templates
        )
        self.factory_service.character_factory = character_factory
        self.monsters = [character_factory.build(uid) for uid, monster in
                         json_template_loader.monster_templates.items()]
        self.items = []
