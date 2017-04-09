import tdl
from areas.level import Level
from factories.body_factory import BodyFactory
from factories.character_factory import CharacterFactory
from factories.factory_service import FactoryService
from factories.item_factory import ItemFactory
from generators.dungeon_generator import DungeonGenerator
from managers.console_manager import ConsoleManager
from managers.scene_manager import SceneManager
from managers.game_context import GameContext
from data.python_templates.characters import character_templates
from data.python_templates.items import item_templates


class GameManager(object):
    """
    Game Manager: Handles setup and progression of the game
    Admittedly this is a bit of a mess and will need to be cleaned up.
    """
    def __init__(self):
        # Pre-load levels into database
        self.game_context = GameContext()
        self.loaded_levels = []
        self.items = []
        self.monsters = []
        self.load_game_data()
        self.console_manager = ConsoleManager()
        self.scene_manager = SceneManager(self.console_manager,
                                          start_game_callback=self.new_game,
                                          game_context=self.game_context)
        self.dungeon_generator = DungeonGenerator(self.game_context.factory_service)

    def start(self):
        self.scene_manager.current_scene.render()
        tdl.setTitle("Roguelike Framework")
        while True:  # Continue in an infinite game loop.
            self.console_manager.main_console.clear()  # Blank the console
            self.scene_manager.render(player=self.game_context.player)
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

    def new_game(self):
        # TODO This should prepare the first level
        level = Level()
        level.name = "DEFAULT"
        level.min_room_size = 1
        level.max_room_size = 10
        level.max_rooms = 10
        level.width = 80
        level.height = 45
        self.init_dungeon(level)

    def init_dungeon(self, level):
        # TODO The player must be built and retrieved here.
        player = self.game_context.player
        player.is_player = True
        level.monster_spawn_list = self.monsters
        self.dungeon_generator.generate(level, player)

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
        item_factory = self.game_context.item_factory
        # TODO Currently it builds the monsters one time, it does validate if the template is correct BUT
        # TODO Do we really want to hold an instance of each in memory?
        self.monsters = [character_factory.build(uid) for uid, monster in character_templates.items()]

        self.items = [item_factory.build(uid) for uid, item in item_templates.items()]
