class ComponentMessage(object):
    __slots__ = ['sender']

    def __init__(self, sender):
        self.sender = sender

    @classmethod
    def create_response(cls, replier):
        return ComponentResponse(replier)


class ComponentResponse(object):
    def __init__(self, replier):
        self.replier = replier


class QueryStatModifierMessage(ComponentMessage):
    """This requests any component that modifies requested core stat."""
    __slots__ = ['sender', 'stat']

    def __init__(self, sender, stat):
        super().__init__(sender)
        self.stat = stat

    @classmethod
    def create_response(cls, replier):
        return QueryStatModifierResponse(replier)


class QueryStatModifierResponse(ComponentResponse):
    __slots__ = ['replier', 'stat_modifier_value']

    def __init__(self, replier):
        super().__init__(replier)
        self.stat_modifier_value = None

