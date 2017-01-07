class Level(object):
    def __init__(self):
        self.name = ""
        self.description = ""
        self.max_room_size = 0
        self.min_room_size = 0
        self.max_rooms = 0
        self.num_rooms = 0
        self.monster_rooms = []
        self.tiles = []
        self.monster_spawn_list = []
        self.item_spawn_list = []
        self.spawned_monsters = []
        self.spawned_items = []
        self.width = None
        self.height = None
