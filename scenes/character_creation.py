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
            self.menu.print_str(text, x, self.get_next_y())
            self.menu.letter_index += 1

    def render(self, **kwargs):
        for control in self.controls:
            self.menu.printStr(control.text)

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
            else:
                self.answer += key_event.keychar

    @property
    def text(self):
        return self.question + " " + self.answer