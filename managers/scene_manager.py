from scenes import (
    GameScene,
    InventoryScene,
    MainMenuScene
)


class SceneManager(object):
    def __init__(self, console_manager, start_game_callback):
        self.console_manager = console_manager
        self.scenes = {
            GameScene.ID: GameScene(self.console_manager),
            InventoryScene.ID: InventoryScene(self.console_manager),
            MainMenuScene.ID: MainMenuScene(self.console_manager, self.start_game)
        }
        self.current_scene = self.scenes[MainMenuScene.ID]
        self.start_game_callback = start_game_callback

    def start_game(self):
        self.current_scene = self.scenes[GameScene.ID]
        self.console_manager.clear()
        self.start_game_callback()

    def render(self, **kwargs):
        self.current_scene.render(**kwargs)

    def handle_input(self, **kwargs):
        self.current_scene.handle_input(**kwargs)
