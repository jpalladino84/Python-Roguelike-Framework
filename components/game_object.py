from components.component import valid_components


class GameObject(object):
    def __init__(self):
        self.components = {}
        self.observers = {}
        self.responders = {}

    def copy_to(self, new_game_object):
        for component in self.components.values():
            new_game_object.register_component(component.copy())

        return new_game_object

    def get_component(self, component_name):
        return self.components.get(component_name, None)

    def update(self):
        for component in self.components.values():
            component.update()

    def transmit_message(self, sender, message_type, **kwargs):
        if message_type in self.observers:
            for observer, func in self.observers[message_type]:
                if observer != sender:
                    func(**kwargs)

    def transmit_query(self, sender, query_type, **kwargs):
        responses = []
        if query_type in self.responders:
            for responder, func in self.responders[query_type]:
                if responder != sender:
                    responses.append(func(**kwargs))

        return responses

    def register_observer(self, observer, message_type, func):
        if message_type not in self.observers:
            self.observers[message_type] = []
        if func not in self.observers[message_type]:
            self.observers[message_type].append((observer, func))

    def register_query_responder(self, responder, query_type, func):
        if query_type not in self.responders:
            self.responders[query_type] = []
        if func not in self.responders[query_type]:
            self.responders[query_type].append((responder, func))

    def register_component(self, component):
        if component.NAME in self.components:
            self.unregister_component(component)

        self.components[component.NAME] = component
        component.on_register(self)

    def unregister_component(self, component):
        if component.NAME in self.components:
            component.on_unregister()
            del self.components[component.NAME]

    def __getattr__(self, item):
        if item in valid_components:
            component = self.get_component(item)
            if component:
                return component
            return NoneVoid()
        raise AttributeError()


class NoneVoid(object):
    """
    This class's only purpose is to Falsify any other calls make to get attributes from it.
    It allows us to duck type into components a little easier.
    """
    def __getattr__(self, item):
        return None

    def __bool__(self):
        return False

