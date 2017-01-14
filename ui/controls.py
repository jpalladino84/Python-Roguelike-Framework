import tdl

ACTIVE_CONTROL_COLOR = (255, 255, 100)
INACTIVE_CONTROL_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)


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

    def render(self, console, active):
        if active:
            color = ACTIVE_CONTROL_COLOR
        else:
            color = INACTIVE_CONTROL_COLOR
        console.setColors(fg=color, bg=BLACK_COLOR)
        console.printStr(self.text)


class ListChoiceControl(object):
    def __init__(self, question, options, root_console):
        self.letter_index = ord('a')
        self.question = question
        self.options = [(self.__assign_letter(), option) for option in options]
        self.answer = None
        self.root_console = root_console
        self.finished = False
        self._formatted_options = ""

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

    def render(self, console, active):
        if active:
            color = ACTIVE_CONTROL_COLOR
        else:
            color = INACTIVE_CONTROL_COLOR

        console.setColors(fg=color, bg=BLACK_COLOR)
        console.printStr(self.text)


class PointDistributionControl(object):
    # TODO This works well for a point system, but modifiers aren't shown
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
        self.list_formatted_options = []

    @property
    def text(self):
        return self.question + "\n" + self._get_formatted_options()

    @property
    def answer(self):
        return self.assigned_points

    def _get_formatted_options(self):
        text = ""
        self.list_formatted_options.clear()
        for option in self.options:
            new_text = "    {}: {} \n".format(option, self.assigned_points[option])
            self.list_formatted_options.append((option, new_text))
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

    def render(self, console, active):
        self._get_formatted_options()
        for option, text in self.list_formatted_options:
            if active and option == self.active_option:
                console.setColors(fg=ACTIVE_CONTROL_COLOR, bg=BLACK_COLOR)
            else:
                console.setColors(fg=INACTIVE_CONTROL_COLOR, bg=BLACK_COLOR)
            console.printStr(text)

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
