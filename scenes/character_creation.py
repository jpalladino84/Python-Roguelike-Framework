import tdl
from managers.console_manager import Menu


class CharacterCreationScene(object):
    ID = "CharacterCreation"

    def __init__(self, console_manager, template_manager, start_game_callback):
        self.console_manager = console_manager
        self.template_manager = template_manager
        self.main_console = console_manager.main_console
        self.menus = []
        self.control_name = InputControl("Name:")
        self.controls = [
            self.control_name
        ]
        self.active_control = self.control_name
        self.options = ["Finish"]
        self.menu = Menu('Main Menu', self.options, self.main_console.width, self.main_console.height)
        # TODO THIS should be in the menu itself.
        self.menu_draws = []
        self.current_x = 20
        self.current_y = 20
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
        self.current_x = 20
        self.current_y = 20
        self.menu.clear()
        for control in self.controls:
            self.menu.print_str(control.text, self.current_x, self.current_y)
            self.current_y += 1

        self.render_menu()
        self.main_console.blit(self.menu, 0, 0)
        tdl.flush()

    def handle_input(self, **kwargs):
        if self.active_control:
            self.active_control.handle_input()
            if self.active_control.finished:
                self.active_control = None
        else:
            key_event = tdl.event.keyWait()
            if key_event.keychar.upper() == 'A':
                # TODO Assign new player here, via SERVICE is preferred.
                self.start_game_callback()
            elif key_event.keychar.upper() == 'B':
                # Halt the script using SystemExit
                raise SystemExit('The window has been closed.')


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