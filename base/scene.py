"""
This is the scene module. 
"""
import abc


class BaseScene(object):
    """Abstract class for all scenes"""
    __metaclass__ = abc.ABCMeta

    def __init__(self, console_manager, scene_manager, game_context):
        self.console_manager = console_manager
        self.main_console = console_manager.main_console
        self.scene_manager = scene_manager
        self.game_context = game_context

    @abc.abstractmethod
    def render(self):
        pass

    @abc.abstractmethod
    def handle_input(self):
        pass

    def transition_to(self, scene_name):
        self.scene_manager.transition_to(scene_name)
