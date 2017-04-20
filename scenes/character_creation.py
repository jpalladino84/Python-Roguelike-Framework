import tdl

from components.stats import make_character_stats
from data.python_templates.classes import character_class_templates
from data.python_templates.races import race_templates
from data.python_templates.outfits import starter_warrior, starter_thief
from stats.enums import StatsEnum
from managers.console_manager import Menu
from ui import controls


class CharacterCreationScene(object):
    ID = "CharacterCreation"

    # TODO We need a sort of cursor to print every control in its place.
    # TODO For that we need to have a render func passing the cursor
    # TODO and each control needs a menu to render on.
    
    def __init__(self, console_manager, game_context, start_game_callback):
        self.game_context = game_context
        self.character_factory = self.game_context.character_factory
        self.body_factory = self.game_context.body_factory
        self.console_manager = console_manager
        self.main_console = console_manager.main_console
        self.options = ["Finish"]

        self.control_name = controls.InputControl("Name:")
        self.control_class = controls.ListChoiceControl(
            "Class:", root_console=self.main_console,
            options=sorted(character_class_templates.values(), key=lambda c_class: c_class.name)
        )
        self.control_race = controls.ListChoiceControl(
            question="Race:", root_console=self.main_console,
            options=sorted(race_templates.values(), key=lambda race: race.name)
        )
        self.control_stats = controls.PointDistributionControl(
            question="Stats:",
            options=["Strength", "Dexterity", "Constitution", "Intelligence", "Charisma", "Wisdom"],
            root_console=self.main_console,
            total_points=27,
            initial_value=8,
            max_value=15,
            cost_calculator=lambda current: 1 if current < 13 else 2
        )

        self.controls = [
            self.control_name,
            self.control_class,
            self.control_race,
            self.control_stats
        ]
        self.menu = Menu('Main Menu', self.options, self.main_console.width,
                         self.main_console.height)
        self.active_control = self.control_name

        # TODO THIS should be in the menu itself.
        self.menu_draws = []
        self.start_game_callback = start_game_callback
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
                        class_uid=self.control_class.answer.uid,
                        race_uid=self.control_race.answer.uid,
                        stats=make_character_stats(
                            **{uid.lower(): value for uid, value in self.control_stats.answer.items()}),
                        body_uid="humanoid"
                    )
                    player = self.game_context.player
                    # TODO We will need a much better way to assign outfits.
                    if self.control_class.answer.uid.lower() == "thief":
                        starter_thief.apply(player)
                    else:
                        starter_warrior.apply(player)
                    self.start_game_callback()
