from scenes import (
    CharacterCreationScene,
    GameScene,
    InventoryScene,
    MainMenuScene
)


class SceneManager(object):
    def __init__(self, console_manager, game_context):
        # TODO Should have a service to access templates instead of using the manager..
        # TODO Not sure about the callbacks, think of a better way.
        self.console_manager = console_manager
        self.game_context = game_context
        self.current_scene = None
        self.scenes = {
            "CharacterCreationScene": CharacterCreationScene,
            "GameScene": GameScene,
            "InventoryScene": InventoryScene,
            "MainMenuScene": MainMenuScene
        }
        self.transition_to("MainMenuScene")

    def transition_to(self, scene_name):
        self.current_scene = self.scenes[scene_name](self.console_manager, self, self.game_context)

    def render_current_scene(self, **kwargs):
        self.current_scene.render(**kwargs)

    def handle_input(self, **kwargs):
        self.current_scene.handle_input(**kwargs)
