class Tile(object):
    def __init__(self, x, y, is_blocked=False):
        self.x = x
        self.y = y
        self.is_blocked = is_blocked
        self.is_explored = False
        self.is_ground = False
        self.contains_object = None
        self.block_sight = is_blocked
