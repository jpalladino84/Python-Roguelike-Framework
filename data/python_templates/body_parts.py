from abilities.physical_abilities import PhysicalAbilities
from bodies.body_part import BodyPart
from combat.enums import ThreatLevel


humanoid_head = BodyPart('humanoid_head', relative_size=25, threat_level=ThreatLevel.Major)
humanoid_eye = BodyPart('humanoid_eye', {PhysicalAbilities.SEE: 1}, relative_size=5, threat_level=ThreatLevel.Critical)
humanoid_ear = BodyPart('humanoid_ear', {PhysicalAbilities.HEAR: 1}, relative_size=5)
humanoid_mouth = BodyPart('humanoid_mouth', {PhysicalAbilities.EAT: 1}, relative_size=5)
humanoid_brain = BodyPart('humanoid_brain', {PhysicalAbilities.THINK: 1}, relative_size=15, threat_level=ThreatLevel.Fatal)
humanoid_torso = BodyPart('humanoid_torso', relative_size=50, threat_level=ThreatLevel.Major)
humanoid_heart = BodyPart('humanoid_heart', {PhysicalAbilities.LIVE: 1}, relative_size=25, threat_level=ThreatLevel.Fatal)
humanoid_lungs = BodyPart('humanoid_lungs', {PhysicalAbilities.BREATHE: 1}, relative_size=25, threat_level=ThreatLevel.Fatal)
humanoid_arm = BodyPart('humanoid_arm', relative_size=25, threat_level=ThreatLevel.Major)
humanoid_hand = BodyPart('humanoid_hand', {PhysicalAbilities.GRASP: 1, PhysicalAbilities.PUNCH: 1}, relative_size=10)
humanoid_leg = BodyPart('humanoid_leg', {PhysicalAbilities.STAND: 1, PhysicalAbilities.MOVE: 1}, relative_size=25, threat_level=ThreatLevel.Major)
humanoid_foot = BodyPart('humanoid_foot', {PhysicalAbilities.STAND: 1, PhysicalAbilities.MOVE: 1}, relative_size=10)

body_part_templates = {
    humanoid_head.uid: humanoid_head,
    humanoid_eye.uid: humanoid_eye,
    humanoid_ear.uid: humanoid_ear,
    humanoid_mouth.uid: humanoid_mouth,
    humanoid_brain.uid: humanoid_brain,
    humanoid_torso.uid: humanoid_torso,
    humanoid_heart.uid: humanoid_heart,
    humanoid_lungs.uid: humanoid_lungs,
    humanoid_arm.uid: humanoid_arm,
    humanoid_hand.uid: humanoid_hand,
    humanoid_leg.uid: humanoid_leg,
    humanoid_foot.uid: humanoid_foot,
}