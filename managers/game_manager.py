import tdl

from managers.console_manager import ConsoleManager
from managers.scene_manager import SceneManager
from managers.game_context import GameContext
from factories.body_factory import BodyFactory
from factories.character_factory import CharacterFactory
from factories.factory_service import FactoryService
from factories.item_factory import ItemFactory


class GameManager(object):
    """
    Game Manager: Handles setup and progression of the game
    Admittedly this is a bit of a mess and will need to be cleaned up.
    """
    def __init__(self):
        # Pre-load levels into database
        self.game_context = GameContext()

        self.console_manager = ConsoleManager()
        self.scene_manager = SceneManager(self.console_manager,
                                          game_context=self.game_context)
        self.load_game_data()

    def start(self):
        tdl.setTitle("Roguelike Framework")
        while True:  # Continue in an infinite game loop.
            self.console_manager.main_console.clear()  # Blank the console
            self.scene_manager.render_current_scene(player=self.game_context.player)
            # TODO We might want to GET the tdl key event here so we don't have to reimplement generic stuff.
            all_key_events = list(tdl.event.get())
            for key_event in all_key_events:
                if key_event.type == 'QUIT':
                    # Halt the script using SystemExit
                    raise SystemExit('The window has been closed.')
            key_events = [key_event for key_event in all_key_events if key_event.type == 'KEYDOWN']

            self.scene_manager.handle_input(player=self.game_context.player, key_events=key_events)
            tdl.flush()
            # TODO When dead it should switch to a new scene for character dump.

    def load_game_data(self):
        """
        This is where the game templates / data is loaded.
        """
        self.game_context.factory_service = FactoryService(body_factory=BodyFactory())
        factory_service = self.game_context.factory_service
        character_factory = CharacterFactory(factory_service=self.game_context.factory_service)
        factory_service.character_factory = character_factory
        self.game_context.character_factory = character_factory
        self.game_context.body_factory = factory_service.body_factory
        self.game_context.item_factory = ItemFactory()
