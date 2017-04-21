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
        """This will be called by the scene_manager."""
        pass

    @abc.abstractmethod
    def handle_input(self):
        """Handle any player expected input here."""
        pass

    def transition_to(self, scene_name):
        """Tells the scene_manager to move to the provided scene."""
        self.scene_manager.transition_to(scene_name)
