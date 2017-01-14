import tdl
from managers.console_manager import Menu
from ui import controls
import math
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class InventoryScene(object):
    ID = "Inventory"

    def __init__(self, console_manager, game_context, exit_inventory_callback):
        self.console_manager = console_manager
        self.main_console = console_manager.main_console
        self.game_context = game_context
        self.exit_inventory_callback = exit_inventory_callback
        self.item_list_window = ItemListWindow(self.main_console)
        self.item_detail_window = ItemDetailWindow(self.main_console)
        self.active_window = 0
        self.windows = [
            self.item_list_window,
            self.item_detail_window
        ]

    def on_switch(self, **kwargs):
        if "player" not in kwargs:
            logger.error("Render: Player was not given in kwargs.")
            return

        player = kwargs["player"]
        self.item_list_window.build(player)

    def render(self, **kwargs):
        for window in self.windows:
            window.render(**kwargs)

    def handle_input(self, **kwargs):
        key_event = kwargs["key_event"]
        if key_event.key == "ESCAPE":
            self.exit_inventory_callback()
            return
        for window in self.windows:
            window.handle_input(**kwargs)

        if self.active_window == self.windows.index(self.item_list_window):
            if self.item_list_window.chosen_item is not None:
                self.item_detail_window.build(self.item_list_window.chosen_item)
                self.active_window = self.windows.index(self.item_detail_window)


class ItemListWindow(object):
    def __init__(self, main_console):
        self.main_console = main_console
        self.window = tdl.Window(
            self.main_console, 0, 0,
            width=int(math.floor(self.main_console.width / 2)),
            height=self.main_console.height
        )
        self.control = None
        self.chosen_item = None

    def build(self, player):
        # TODO Not sure how often this should be rebuilt but at least every time the menu is opened
        # TODO and another every removed item
        if player and player.inventory:
            self.control = controls.ListChoiceControl("Items:", player.inventory.get_all_items(), self.window)

    def render(self, **kwargs):
        if self.control:
            self.control.render()

    def handle_input(self, **kwargs):
        if self.control:
            self.control.handle_input(**kwargs)
            if self.control.finished:
                self.chosen_item = self.control.answer


class ItemDetailWindow(object):
    def __init__(self, main_console):
        self.main_console = main_console
        self.window = tdl.Window(
            self.main_console, int(math.floor(self.main_console.width / 2)) + 1, 0,
            width=int(math.floor(self.main_console.width / 2)),
            height=self.main_console.height
        )
        self.control = None
        self.chosen_item = None

    def build(self, item):
        # TODO This should be rebuilt every detailed item
        if item:
            # TODO Show Item Detail View here
            pass

    def render(self, **kwargs):
        if self.control:
            self.control.render()

    def handle_input(self, **kwargs):
        if self.control:
            self.control.handle_input(**kwargs)
