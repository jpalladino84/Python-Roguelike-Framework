"""
Utility functions
"""


def send_to_back(obj, objects):
    # make this object be drawn first, so all others appear above it if
    # they're in the same tile.

    objects.remove(obj)
    objects.insert(0, obj)


def is_blocked(x, y, dungeon):
    #first test the map tile
    if dungeon.map[x][y].blocked:
        return True

    #now check for any blocking objects
    for object in dungeon.objects:
        if object.blocks and object.x == x and object.y == y:
            return True

    return False
