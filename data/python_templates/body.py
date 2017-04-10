from bodies.body_part_tree import BodypartTree
from components.body import Body


def build_humanoid_body():
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

humanoid_body = build_humanoid_body()

body_templates = {
    humanoid_body.uid: humanoid_body
}

