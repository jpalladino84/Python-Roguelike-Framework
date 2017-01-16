import tdl
from components.stats import CharacterStats
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
            options=self.game_context.character_factory.class_templates.values()
        )
        self.control_race = controls.ListChoiceControl(
            question="Race:", root_console=self.main_console,
            options=self.game_context.character_factory.race_templates.values()
        )
        self.control_stats = controls.PointDistributionControl(
            question="Stats:",
            options=["Strength", "Dexterity", "Constitution", "Intelligence", "Charisma", "Wisdom"],
            root_console=self.main_console,
            total_points=20,
            initial_value=8,
            max_value=18
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
                        stats=CharacterStats(
                            health=16,
                            **{uid.lower(): value for uid, value in self.control_stats.answer.items()}),
                        body_uid="humanoid"
                    )
                    # Give that poor guy a sword...
                    self.game_context.player.inventory.add_item(self.game_context.item_factory.build("helmet"))
                    self.game_context.player.equipment.wield(
                        self.game_context.item_factory.build("short_sword"))
                    self.start_game_callback()
