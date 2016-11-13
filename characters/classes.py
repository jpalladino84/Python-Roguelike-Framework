class CharacterClass(object):
    def __init__(self, uid, name, level_tree, experience_penalty=0):
        self.uid = uid
        self.name = name
        self.level_tree = level_tree
        self.experience_penalty = experience_penalty

