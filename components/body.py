import logging

from components.abilities.physical_abilities import PhysicalAbilities

logger_ = logging.getLogger()


class Body(object):
    """
    Height is in feet, Weight in pounds
    """
    def __init__(self, uid, bodypart_tree, name="", height=0, weight=0, outer_material_uid=None,
                 internal_material_uid=None, structural_material_uid=None, blood_uid=None):

        self.uid = uid
        self.bodypart_tree = bodypart_tree
        self.name = name
        self.height = height
        self.weight = weight
        self.outer_material_uid = outer_material_uid
        self.inner_material_uid = internal_material_uid
        self.structural_material_uid = structural_material_uid
        self.blood_uid = blood_uid

    def __str__(self):
        return "Body({})".format(self.name)


class BodyPart(object):
    def __init__(self, uid, physical_abilities=None, relative_size=1):
        """
        :param uid: ID Name of the body part
        :param physical_abilities: Dictionary with abilities granted if any with its relative power as value
        :param relative_size: Percentage of body size, does not have to add up to 100
        """
        self.uid = uid
        self.parent_body_part = None
        self.relative_size = relative_size
        self.children_body_parts = []
        if physical_abilities:
            self.physical_abilities = physical_abilities
        else:
            self.physical_abilities = {}

    def connect(self, parent_body_part):
        self.parent_body_part = parent_body_part
        parent_body_part.add_child(self)

    def add_child(self, child_body_part):
        if child_body_part not in self.children_body_parts:
            self.children_body_parts.append(child_body_part)


class BodypartTree(object):
    CONNECTION_TYPE_CENTER = 0
    CONNECTION_TYPE_ATTACHED = 1
    CONNECTION_TYPE_INSERTED = 2

    def __init__(self, central_node_name, central_body_part_uid):
        self.nodes = [BodypartTreeNode(central_node_name, central_body_part_uid, self.CONNECTION_TYPE_CENTER)]

    def attach(self, parent_node_name, children_node_name, children_body_part_uid):
        self._bind_new_child_to_parent(
            parent_node_name, children_node_name, children_body_part_uid, self.CONNECTION_TYPE_ATTACHED)

    def insert(self, parent_node_name, children_node_name, children_body_part_uid):
        self._bind_new_child_to_parent(
            parent_node_name, children_node_name, children_body_part_uid, self.CONNECTION_TYPE_INSERTED)

    def _bind_new_child_to_parent(self, parent_node_name, children_node_name, children_body_part_uid, connection_type):
        parent_node = next((node for node in self.nodes if node.name == parent_node_name), None)
        if parent_node:
            child_bodypart_node = BodypartTreeNode(children_node_name, children_body_part_uid, connection_type)
            parent_node.add_child_node(child_bodypart_node)
            self.nodes.append(child_bodypart_node)
        else:
            logger_.error("Tried to bind bodypart {} to non existing parent {}.".format(children_node_name,
                                                                                        parent_node_name))


class BodypartTreeNode(object):
    def __init__(self, name, body_part_uid, connection_type):
        self.name = name
        self.body_part_uid = body_part_uid
        self.connection_type = connection_type
        self.children_nodes = []

    def add_child_node(self, child_node):
        self.children_nodes.append(child_node)


class Blood(object):
    """
    Most characters will have ordinary blood but some could have acidic blood or with other properties.
    """
    def __init__(self, uid, name):
        self.uid = uid
        self.name = name


def get_body_parts_sample():
    return [
        BodyPart('humanoid_head', relative_size=25),
        BodyPart('humanoid_eye', {PhysicalAbilities.SEE: 1}, relative_size=5),
        BodyPart('humanoid_ear', {PhysicalAbilities.HEAR: 1}, relative_size=5),
        BodyPart('humanoid_mouth', {PhysicalAbilities.EAT: 1}, relative_size=5),
        BodyPart('humanoid_brain', {PhysicalAbilities.THINK: 1}, relative_size=15),
        BodyPart('humanoid_torso', relative_size=50),
        BodyPart('humanoid_heart', {PhysicalAbilities.LIVE: 1}, relative_size=25),
        BodyPart('humanoid_lungs', {PhysicalAbilities.BREATHE: 1}, relative_size=25),
        BodyPart('humanoid_arm', relative_size=25),
        BodyPart('humanoid_hand', {PhysicalAbilities.GRASP: 1}, relative_size=10),
        BodyPart('humanoid_leg', {PhysicalAbilities.STAND: 1,
                                  PhysicalAbilities.MOVE: 1}, relative_size=25),
        BodyPart('humanoid_foot', {PhysicalAbilities.STAND: 1,
                                   PhysicalAbilities.MOVE: 1}, relative_size=10)
    ]


def get_humanoid_body_sample():
    humanoid_tree = BodypartTree('torso', 'humanoid_torso')
    humanoid_tree.insert('torso', 'heart', 'humanoid_heart')
    humanoid_tree.insert('torso', 'lungs', 'humanoid_lungs')
    humanoid_tree.attach('torso', 'head', 'humanoid_head')
    humanoid_tree.attach('head', 'left eye', 'humanoid_eye')
    humanoid_tree.attach('head', 'right eye', 'humanoid_eye')
    humanoid_tree.attach('head', 'left ear', 'humanoid_ear')
    humanoid_tree.attach('head', 'right ear', 'humanoid_ear')
    humanoid_tree.attach('head', 'mouth', 'humanoid_mouth')
    humanoid_tree.insert('head', 'brain', 'humanoid_brain')
    humanoid_tree.attach('torso', 'left arm', 'humanoid_arm')
    humanoid_tree.attach('left arm', 'left hand', 'humanoid_hand')
    humanoid_tree.attach('torso', 'right arm', 'humanoid_arm')
    humanoid_tree.attach('right arm', 'right hand', 'humanoid_hand')
    humanoid_tree.attach('torso', 'left leg', 'humanoid_leg')
    humanoid_tree.attach('left leg', 'left foot', 'humanoid_foot')
    humanoid_tree.attach('torso', 'right leg', 'humanoid_leg')
    humanoid_tree.attach('right leg', 'right foot', 'humanoid_foot')

    humanoid_body = Body('humanoid', humanoid_tree, 'Humanoid', 5, 150)
    humanoid_body.inner_material = 'flesh'
    humanoid_body.outer_material = 'skin'
    humanoid_body.structural_material = 'bone'
    humanoid_body.blood_type = 'humanoid_blood'

    return humanoid_body


