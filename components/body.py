from collections import OrderedDict
from abilities.physical_abilities import PhysicalAbilities


class Body(object):
    """
    Height is in feet, Weight in pounds
    """
    def __init__(self, uid, name="", height=0, weight=0, central_bodypart=None, outer_material_uid=None,
                 internal_material_uid=None, structural_material_uid=None, internal_organs_uid=None, blood_type=None):

        self.uid = uid
        self.name = name
        self.height = height
        self.weight = weight
        self.central_bodypart = central_bodypart
        self.outer_material_uid = outer_material_uid
        self.inner_material_uid = internal_material_uid
        self.structural_material_uid = structural_material_uid
        self.blood_type = blood_type
        if internal_organs_uid:
            self.internal_organs_uid = internal_organs_uid
        else:
            self.internal_organs_uid = []

    def __str__(self):
        return "Body({})".format(self.name)

    def to_json(self):
        return OrderedDict(uid=self.uid, name=self.uid, height=self.height, weight=self.weight,
                           outer_material_uid=self.outer_material_uid,
                           inner_material_uid=self.inner_material_uid,
                           structural_material_uid=self.structural_material_uid,
                           internal_organs_uid=self.internal_organs_uid,
                           central_bodypart=self.central_bodypart.to_json())


class BodyPart(object):
    def __init__(self, name, parent_body_part=None, physical_abilities=None, internal=False, relative_size=1):
        """
        :param name: Name of the body part
        :param parent_body_part: Parent of the body part
        :param physical_abilities: Dictionary with abilities granted if any with its relative power as value
        :param internal: If the body part is inside it's parent.
        :param relative_size: Percentage of body size, does not have to add up to 100
        """
        self.name = name
        self.parent_body_part = None
        self.internal = internal
        self.relative_size = relative_size
        if parent_body_part:
            self.connect(parent_body_part)
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

    def to_json(self):
        return OrderedDict(name=self.name, children_body_parts=[
            body_part.to_json() for body_part in self.children_body_parts])


class Blood(object):
    """
    Most characters will have ordinary blood but some could have acidic blood or with other properties.
    """
    def __init__(self, uid, name):
        self.uid = uid
        self.name = name


def get_humanoid_body_sample():
    humanoid_body = Body('humanoid', 'Humanoid', 5, 150)

    torso_body_part = BodyPart('Torso', relative_size=50)
    head = BodyPart('Head', torso_body_part, relative_size=25)
    left_eye = BodyPart('Left Eye', head, {PhysicalAbilities.SEE: 1}, relative_size=5)
    right_eye = BodyPart('Right Eye', head, {PhysicalAbilities.SEE: 1}, relative_size=5)
    left_ear = BodyPart('Left Ear', head, {PhysicalAbilities.HEAR: 1}, relative_size=5)
    right_ear = BodyPart('Right Ear', head, {PhysicalAbilities.HEAR: 1}, relative_size=5)
    mouth = BodyPart('Mouth', head, {PhysicalAbilities.EAT: 1}, relative_size=5)
    brain = BodyPart('Brain', head, {PhysicalAbilities.THINK: 1}, internal=True, relative_size=15)

    left_arm = BodyPart('Left Arm', torso_body_part, relative_size=25)
    right_arm = BodyPart('Right Arm', torso_body_part, relative_size=25)
    left_hand = BodyPart('Left Hand', left_arm, {PhysicalAbilities.GRASP: 1}, relative_size=10)
    right_hand = BodyPart('Right Hand', right_arm, {PhysicalAbilities.GRASP: 1}, relative_size=10)
    left_leg = BodyPart('Left Leg', torso_body_part,  {PhysicalAbilities.STAND: 1,
                                                       PhysicalAbilities.MOVE: 1}, relative_size=25)
    right_leg = BodyPart('Right Leg', torso_body_part,  {PhysicalAbilities.STAND: 1,
                                                         PhysicalAbilities.MOVE: 1}, relative_size=25)
    left_foot = BodyPart('Left Foot', left_leg, {PhysicalAbilities.STAND: 1,
                                                 PhysicalAbilities.MOVE: 1}, relative_size=10)
    right_foot = BodyPart('Right Foot', right_leg, {PhysicalAbilities.STAND: 1,
                                                    PhysicalAbilities.MOVE: 1}, relative_size=10)

    humanoid_body.central_bodypart = torso_body_part
    humanoid_body.inner_material = 'flesh'
    humanoid_body.outer_material = 'skin'
    humanoid_body.structural_material = 'bone'
    humanoid_body.internal_organs_uid = ['humanoid_heart']
    humanoid_body.blood_type = Blood('humanoid_blood', 'humanoid_blood')

    return humanoid_body
