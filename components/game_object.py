from components.component import valid_components


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
        if item in valid_components:
            component = self.get_component(item)
            if component:
                return component
            else:
                if not hasattr(self, item):
                    return NoneVoid()

        return super().__getattribute__(item)


class NoneVoid(object):
    """
    This class's only purpose is to Falsify any other calls make to get attributes from it.
    It allows us to duck type into components a little easier.
    """
    def __getattr__(self, item):
        return None
