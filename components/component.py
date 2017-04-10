class Component(object):
    """Base class for components"""
    NAME = "base_component"

    def __init__(self):
        self.host = None
        if self.NAME not in valid_components:
            valid_components[self.NAME] = self

    def on_register(self, host):
        self.host = host

    def on_unregister(self):
        self.host = None

    def update(self):
        pass

    def handle_message(self, message):
        pass


# TODO If a component is never initialized, is it truly invalid?
valid_components = {}
