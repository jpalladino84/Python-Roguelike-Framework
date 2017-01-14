import tdl
from components.stats import CharacterStats
from managers.console_manager import Menu


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

        self.control_name = InputControl("Name:")
        self.control_class = ListChoiceControl("Class:", root_console=self.main_console,
                                               options=self.game_context.character_factory.class_templates.values())
        self.control_race = ListChoiceControl(question="Race:", root_console=self.main_console,
                                              options=self.game_context.character_factory.race_templates.values())
        self.control_stats = PointDistributionControl(
            question="Stats:",
            options=["Strength", "Dexterity", "Constitution", "Intelligence", "Charisma", "Wisdom"],
            root_console=self.main_console,
            total_points=16,
            initial_value=8,
            max_value=18
        )

        self.controls = [
            self.control_name,
            self.control_class,
            self.control_race,
            self.control_stats
        ]
        self.menu = Menu('Main Menu', self.options, self.main_console.width, self.main_console.height)
        self.active_control = self.control_name

        # TODO THIS should be in the menu itself.
        self.menu_draws = []
        self.current_x = 0
        self.current_y = 0
        self.start_game_callback = start_game_callback
        self.create_menu()

    def get_next_y(self):
        self.current_y += 2
        return self.current_y

    def get_next_x(self):
        self.current_x += 5
        return self.current_x

    def create_menu(self):
        x = self.get_next_x()
        for option_text in self.options:
            text = '(' + chr(self.menu.letter_index) + ') ' + option_text
            y = self.get_next_y()
            self.menu.print_str(text, x, y)
            self.menu.letter_index += 1
            self.menu_draws.append((text, x, y))

    def render_menu(self):
        for text, x, y in self.menu_draws:
            self.menu.print_str(text, x, y)

    def render(self, **kwargs):
        self.current_x = 0
        self.current_y = 0
        self.menu.clear()
        for control in self.controls:
            if self.active_control is None \
                    or self.controls.index(self.active_control) >= self.controls.index(control):
                self.menu.print_str(control.text, self.current_x, self.current_y)
                self.current_y += 1

        if not self.active_control:
            self.render_menu()
        self.main_console.blit(self.menu, 0, 0)
        tdl.flush()

    def handle_input(self, **kwargs):
        if self.active_control:
            self.active_control.handle_input()
            if self.active_control.finished:
                new_index = self.controls.index(self.active_control) + 1
                if new_index < len(self.controls):
                    self.active_control = self.controls[new_index]
                else:
                    self.active_control = None
        else:
            key_event = tdl.event.keyWait()
            if key_event.keychar.upper() == 'A':
                # TODO Assign new player here, via SERVICE is preferred.
                # TODO Player should choose his class, race, default racial body should be assigned
                # TODO He should be able to choose his stats but racial BONUSES to his stats should be applied somehow.
                self.game_context.player = self.character_factory.create(
                    name=self.control_name.answer,
                    class_uid=self.control_class.answer.uid,
                    race_uid=self.control_race.answer.uid,
                    stats=CharacterStats(health=16),
                    body_uid="humanoid"
                )
                self.start_game_callback()


# TODO This is the wrong place to put this
class InputControl(object):
    """
    This object is used to catch text input
    """
    def __init__(self, question):
        self.question = question
        self.answer = ""
        self.finished = False

    def handle_input(self, **kwargs):
        key_event = tdl.event.keyWait()
        if key_event.keychar:
            if key_event.key == "F4":
                # TODO I REALLY dislike the F4.. as if F4 always closed the game! Find the source and make it right
                raise SystemExit("Window was closed.")
            if key_event.key == "ENTER":
                self.finished = True
                return
            if key_event.key == "BACKSPACE":
                if len(self.answer) > 0:
                    self.answer = self.answer[:-1]
            else:
                self.answer += key_event.char

    @property
    def text(self):
        return self.question + " " + self.answer


class ListChoiceControl(object):
    def __init__(self, question, options, root_console):
        self.letter_index = ord('a')
        self.question = question
        self.options = [(self.__assign_letter(), option) for option in options]
        self.answer = None
        self.root_console = root_console
        self.finished = False
        self._formatted_options = ""
        # TODO This isn't very good
        self.lines = 0

    def __assign_letter(self):
        self.letter_index += 1
        return chr(self.letter_index)

    @property
    def text(self):
        return self.question + "\n" + self._get_formatted_options()

    def _get_formatted_options(self):
        if self._formatted_options:
            return self._formatted_options

        text = ""
        width_char_count = 0
        for letter, option in self.options:
            new_text = "    ({}){}".format(letter, option.name)
            if width_char_count + len(new_text) > self.root_console.width:
                new_text += "\n"
                width_char_count = 0
                self.lines += 1

            text += new_text
            width_char_count += len(new_text)
        self._formatted_options = text

        return self._formatted_options

    def handle_input(self, **kwargs):
        key_event = tdl.event.keyWait()
        if key_event.keychar:
            if key_event.key == "F4":
                # TODO I REALLY dislike the F4.. as if F4 always closed the game! Find the source and make it right
                raise SystemExit("Window was closed.")

            chosen_option = next((option for letter, option in self.options if letter == key_event.keychar), None)
            if chosen_option:
                self.answer = chosen_option
                self.finished = True


class PointDistributionControl(object):
    def __init__(self, question, options, root_console, initial_value, max_value, total_points):
        self.question = question
        self.options = options
        self.initial_value = initial_value
        self.max_value = max_value
        self.total_points = total_points
        self.used_points = 0
        self.assigned_points = {option: initial_value for option in self.options}
        self.active_option = options[0]
        self.root_console = root_console
        self.finished = False
        self._formatted_options = ""
        # TODO This isn't very good
        self.lines = 0

    @property
    def text(self):
        return self.question + "\n" + self._get_formatted_options()

    @property
    def answer(self):
        return self.assigned_points

    def _get_formatted_options(self):
        text = ""
        for option in self.options:
            new_text = "    {}: {} \n".format(option, self.assigned_points[option])
            self.lines += 1
            text += new_text
        self._formatted_options = text

        return self._formatted_options

    def handle_input(self, **kwargs):
        key_event = tdl.event.keyWait()
        if key_event.keychar:
            if key_event.key == "F4":
                # TODO I REALLY dislike the F4.. as if F4 always closed the game! Find the source and make it right
                raise SystemExit("Window was closed.")

            if key_event.key == 'KP6' or key_event.key == "RIGHT":
                self.__increase_value()

            if key_event.key == 'KP4' or key_event.key == "LEFT":
                self.__decrease_value()

            if key_event.key == "KP8" or key_event.key == "UP":
                self.__cycle_previous_option()

            if key_event.key == "KP2" or key_event.key == "DOWN":
                self.__cycle_next_option()

            if key_event.key == "ENTER":
                if self.options.index(self.active_option) == len(self.options) - 1:
                    self.finished = True
                    return
                else:
                    self.__cycle_next_option()

    def __increase_value(self):
        if (self.used_points < self.total_points
                and self.assigned_points[self.active_option] < self.max_value):
            self.used_points += 1
            self.assigned_points[self.active_option] += 1

    def __decrease_value(self):
        if self.assigned_points[self.active_option] > self.initial_value:
            self.used_points -= 1
            self.assigned_points[self.active_option] -= 1

    def __cycle_next_option(self):
        current_index = self.options.index(self.active_option)
        if current_index == len(self.options) - 1:
            self.active_option = self.options[0]
        else:
            self.active_option = self.options[current_index + 1]

    def __cycle_previous_option(self):
        current_index = self.options.index(self.active_option)
        if current_index == 0:
            self.active_option = self.options[-1]
        else:
            self.active_option = self.options[current_index - 1]