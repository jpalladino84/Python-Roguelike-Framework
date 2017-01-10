from scenes import (
    CharacterCreationScene,
    GameScene,
    InventoryScene,
    MainMenuScene
)


class SceneManager(object):
    def __init__(self, console_manager, start_game_callback, template_manager):
        # TODO Should have a service to access templates instead of using the manager..
        # TODO Not sure about the callbacks, think of a better way.
        self.console_manager = console_manager
        self.scenes = {
            CharacterCreationScene.ID: CharacterCreationScene(console_manager, template_manager, start_game_callback),
            GameScene.ID: GameScene(self.console_manager),
            InventoryScene.ID: InventoryScene(self.console_manager),
            MainMenuScene.ID: MainMenuScene(self.console_manager, self.enter_creation_screen)
        }
        self.current_scene = self.scenes[MainMenuScene.ID]
        self.start_game_callback = start_game_callback

    def start_game(self):
        self.current_scene = self.scenes[GameScene.ID]
        self.console_manager.clear()
        self.start_game_callback()

    def enter_creation_screen(self):
        self.current_scene = self.scenes[CharacterCreationScene.ID]

    def render(self, **kwargs):
        self.current_scene.render(**kwargs)

    def handle_input(self, **kwargs):
        self.current_scene.handle_input(**kwargs)
