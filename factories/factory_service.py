class FactoryService(object):
    """
    This allows us to call for something built.
    This is rudimentary for now but it could be nice to have each factory provide a list of
    types it handles and dispatch each request to the factory that handles it.
    """
    def __init__(self, body_factory, character_factory=None):
        self.body_factory = body_factory
        self.character_factory = character_factory

    def build_body_instance_by_uid(self, body_uid):
        return self.body_factory.build_body(body_uid)

    def assemble_body(self, body):
        return self.body_factory.assemble_body(body)

    def build_character_instance_by_uid(self, character_uid):
        if self.character_factory:
            return self.character_factory.build(character_uid)
