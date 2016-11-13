class FactoryService(object):
    """
    This allows us to call for something built or samples to feed back.
    """
    def __init__(self, template_loader, body_factory, character_factory):
        self.template_loader = template_loader
        self.body_factory = body_factory
        self.character_factory = character_factory
