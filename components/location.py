from .component import Component


class Location(Component):
    NAME = "location"

    def __init__(self):
        super().__init__()
        # TODO THIS HOLDS ALL THE INFORMATION NEEDED TO LOCATE SOMETHING
        self.local_x = 0
        self.local_y = 0
        self.global_x = 0
        self.global_y = 0
        self.area = None
        self.level = None

    def get_local_coords(self):
        return self.local_x, self.local_y
