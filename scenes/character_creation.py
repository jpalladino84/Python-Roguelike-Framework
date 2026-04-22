import tdl

from base.scene import BaseScene

from components.stats import make_character_stats
from data.python_templates.outfits import starter_warrior
from managers.console_manager import Menu
from ui import controls


class CharacterCreationScene(BaseScene):
    ID = "CharacterCreation"

    def __init__(self, console_manager, scene_manager, game_context):
        super().__init__(console_manager, scene_manager, game_context)
        self.character_factory = self.game_context.character_factory
        self.body_factory = self.game_context.body_factory
        self.options = ["Finish"]

        self.control_name = controls.InputControl("Name:")

        self.controls = [
            self.control_name,
        ]
        self.menu = Menu('Character Creation',
                         """
                         Create your adventure!
                         """,
                         self.options,
                         self.main_console.width,
                         self.main_console.height)
        self.active_control = self.control_name

        self.menu_draws = []
        self.create_menu()

    def create_menu(self):
        for option_text in self.options:
            text = '(' + chr(self.menu.letter_index) + ') ' + option_text + '   '
            self.menu.letter_index += 1
            self.menu_draws.append(text)

    def render_menu(self):
        for text in self.menu_draws:
            self.menu.printStr(text)

    def render(self, **kwargs):
        self.menu.clear()
        self.menu.move(0, 0)
        for control in self.controls:
            if self.active_control is None \
                    or self.controls.index(self.active_control) >= self.controls.index(control):
                if control == self.active_control:
                    control.render(self.menu, True)
                else:
                    control.render(self.menu, False)
            self.menu.printStr("\n")

        if not self.active_control:
            self.render_menu()
        self.main_console.blit(self.menu, 0, 0)
        tdl.flush()

    def handle_input(self, **kwargs):
        if self.active_control:
            self.active_control.handle_input(**kwargs)
            if self.active_control.finished:
                new_index = self.controls.index(self.active_control) + 1
                if new_index < len(self.controls):
                    self.active_control = self.controls[new_index]
                else:
                    self.active_control = None
        else:
            key_events = kwargs["key_events"]
            for key_event in key_events:
                if key_event.keychar.upper() == 'A':
                    self.game_context.player = self.character_factory.create(
                        name=self.control_name.answer,
                        class_uid="warrior",
                        race_uid="human",
                        stats=make_character_stats(),
                        body_uid="humanoid"
                    )
                    player = self.game_context.player
                    starter_warrior.apply(player)
                    self.transition_to("GameScene")
