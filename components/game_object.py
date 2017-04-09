class GameObject(object):
    def __init__(self):
        self.components = []

    def get_component(self, component_name):
        return next((component for component in self.components if component.NAME == component_name), None)

    def update(self):
        for component in self.components:
            component.update()

    def register_component(self, component):
        if component not in self.components:
            component.on_register(self)
            self.components.append(component)

    def unregister_component(self, component):
        if component in self.components:
            component.on_unregister()
            self.components.remove(component)

    def __getattr__(self, item):
        component = self.get_component(item)
        if component:
            return component

        return super().__getattribute__(item)
