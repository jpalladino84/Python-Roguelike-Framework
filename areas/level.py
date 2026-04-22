class Level(object):
    def __init__(self):
        # Permanent variables
        self.name = ""
        self.description = ""
        self.max_room_size = 0
        self.min_room_size = 0
        self.max_rooms = 0
        self.width = None
        self.height = None
        self.monster_spawn_list = []
        self.item_spawn_list = []

        self.depth = 1

        # Generated variables
        self.num_rooms = 0
        self.tiles = []
        self.rooms = []
        self.spawned_monsters = []
        self.spawned_items = []
        self.stair_down_pos = None
        self.stair_up_pos = None

