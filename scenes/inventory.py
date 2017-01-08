class InventoryScene(object):
    ID = "Inventory"

    def __init__(self, console_manager):
        pass

    def render(self, **kwargs):
        width = 40
        height = 30
        inventory_menu = Menu('Inventory', inventory_list, width, height)
        inventory_menu.drawFrame(0, 0, width, height, '#', (255, 255, 255), None)
        tdl.setTitle('Inventory Menu')

        if len(inventory_list) > inventory_menu.max_options_len:
            raise ValueError('Cannot have a menu with more than 26 options.')

        x = 5
        y = 5

        for letter, item in inventory_list.iteritems():
            text = '(' + letter + ') ' + item.name
            inventory_menu.print_str(text, x, y)
            y += 2
            inventory_menu.letter_index += 1

        inventory_menu.print_str('Press (I) to exit the menu', 10, 28)
        self.render_console(inventory_menu, 20, 10)

    def handle_input(self, **kwargs):
        pass
