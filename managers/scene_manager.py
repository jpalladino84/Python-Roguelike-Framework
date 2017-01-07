from scenes import (
    GameScene,
    InventoryScene,
    MainMenuScene
)


class SceneManager(object):
    def __init__(self, console_manager):
        self.console_manager = console_manager
        self.scenes = {
            GameScene.ID: GameScene(self.console_manager),
            InventoryScene.ID: InventoryScene(self.console_manager),
            MainMenuScene.ID: MainMenuScene(self.console_manager, self.start_game)
        }
        self.current_scene = self.scenes[MainMenuScene.ID]

    def start_game(self):
        self.current_scene = self.scenes[GameScene.ID]

    def render(self):
        self.current_scene.render()

    def handle_input(self):
        self.current_scene.handle_input()
