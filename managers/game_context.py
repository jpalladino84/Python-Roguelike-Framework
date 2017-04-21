# TODO This is probably the wrong place to put it.
class GameContext(object):
    """
    This object will hold the instances required to be passed around.
    Avoiding the need to pass 40 arguments just in case something down the line needs it.
    """
    def __init__(self):
        self.player = None
        self.factory_service = None
        self.body_factory = None
        self.character_factory = None
        self.json_template_loader = None
        self.item_factory = None
        self.echo_service = None
        self.current_level = None

        # TODO That factory service up there should contain the needs to use the factories themselves..
