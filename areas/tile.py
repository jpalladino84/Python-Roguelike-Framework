class Tile(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.is_blocked = False
        self.is_explored = False
        self.is_ground = False
        self.contains_object = None
        self.block_sight = False