import tdl

from base.scene import BaseScene
from managers.console_manager import Menu
from ui.flavor_text import MAIN_MENU


class MainMenuScene(BaseScene):
    ID = "MainMenu"

    def __init__(self, console_manager, scene_manager, game_context):
        super().__init__(console_manager, scene_manager, game_context)
        self.menu = Menu(MAIN_MENU['name'],
                         MAIN_MENU['text'],
                         MAIN_MENU['options'],
                         self.main_console.width,
                         self.main_console.height)
        self.current_x = 20
        self.current_y = 20
        self.menu.create_menu(self.current_x, self.current_y)

    def render(self, **kwargs):
        self.main_console.blit(self.menu, 0, 0)
        tdl.flush()

    def handle_input(self, **kwargs):
        key_events = kwargs["key_events"]

        for key_event in key_events:
            if key_event.keychar.upper() == 'A':
                self.transition_to("CharacterCreationScene")
            elif key_event.keychar.upper() == 'B':
                # Halt the script using SystemExit
                raise SystemExit('The window has been closed.')
