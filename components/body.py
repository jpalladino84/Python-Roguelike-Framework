class Body(object):
    """
    Height is in feet, Weight in pounds
    """
    def __init__(self, uid, name="", height=0, weight=0, central_bodypart=None, outer_material_uid=None,
                 internal_material_uid=None, structural_material_uid=None, internal_organs_uid=None):

        self.uid = uid
        self.name = name
        self.height = height
        self.weight = weight
        self.central_bodypart = central_bodypart
        self.outer_material_uid = outer_material_uid
        self.inner_material_uid = internal_material_uid
        self.structural_material_uid = structural_material_uid
        if internal_organs_uid:
            self.internal_organs = internal_organs_uid
        else:
            self.internal_organs = []

    def __str__(self):
        return "Body({})".format(self.name)


class BodyPart(object):
    def __init__(self, name, parent_body_part=None):
        self.name = name
        self.parent_body_part = None
        if parent_body_part:
            self.connect(parent_body_part)
        self.children_body_parts = []

    def connect(self, parent_body_part):
        self.parent_body_part = parent_body_part
        parent_body_part.add_child(self)

    def add_child(self, child_body_part):
        if child_body_part not in self.children_body_parts:
            self.children_body_parts.append(child_body_part)




    # TODO IMPLEMENT A LIST OF BODYPARTS WITH AN ENUM COLLECTION OF PHYSICAL ABILITIES THAT WOULD BE PROVIDED
    # EXAMPLE A HAND GIVES THE ABILITY TO GRASP, AN ARM CAN GIVE IMPROVISED_GRASP, EYES GIVES SIGHT
    # THE CENTRAL BODYPART COULD RETURN AN ENTIRE LIST OF ABILITIES
    # EACH BODYPART CAN HAVE ANOTHER ATTACHED, DON'T GET INTO THE SAME DETAILS AS DF BUT STILL HAVE A NICE SELECTION


humanoid_body = Body('humanoid', 'Humanoid', 5, 150)

torso_body_part = BodyPart('Torso')
head = BodyPart('Head', torso_body_part)
left_eye = BodyPart('Left Eye', head)
right_eye = BodyPart('Right Eye', head)
left_ear = BodyPart('Left Ear', head)
right_ear = BodyPart('Right Ear', head)
mouth = BodyPart('Mouth', head)
brain = BodyPart('Brain', head)

left_arm = BodyPart('Left Arm', torso_body_part)
right_arm = BodyPart('Right Arm', torso_body_part)
left_hand = BodyPart('Left Hand', left_arm)
right_hand = BodyPart('Right Hand', right_arm)
left_leg = BodyPart('Left Leg', torso_body_part)
right_leg = BodyPart('Right Leg', torso_body_part)
left_foot = BodyPart('Left Foot', left_leg)
right_foot = BodyPart('Right Foot', right_leg)

humanoid_body.central_bodypart = torso_body_part
humanoid_body.inner_material = 'flesh'
humanoid_body.outer_material = 'skin'
humanoid_body.structural_material = 'bone'