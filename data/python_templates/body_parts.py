from abilities.physical_abilities import PhysicalAbilities
from bodies.body_part import BodyPart
from combat.enums import ThreatLevel

body_parts = [
        BodyPart('humanoid_head', relative_size=25, threat_level=ThreatLevel.Major),
        BodyPart('humanoid_eye', {PhysicalAbilities.SEE: 1}, relative_size=5, threat_level=ThreatLevel.Critical),
        BodyPart('humanoid_ear', {PhysicalAbilities.HEAR: 1}, relative_size=5),
        BodyPart('humanoid_mouth', {PhysicalAbilities.EAT: 1}, relative_size=5),
        BodyPart('humanoid_brain', {PhysicalAbilities.THINK: 1}, relative_size=15, threat_level=ThreatLevel.Fatal),
        BodyPart('humanoid_torso', relative_size=50, threat_level=ThreatLevel.Major),
        BodyPart('humanoid_heart', {PhysicalAbilities.LIVE: 1}, relative_size=25, threat_level=ThreatLevel.Fatal),
        BodyPart('humanoid_lungs', {PhysicalAbilities.BREATHE: 1}, relative_size=25, threat_level=ThreatLevel.Fatal),
        BodyPart('humanoid_arm', relative_size=25, threat_level=ThreatLevel.Major),
        BodyPart('humanoid_hand', {PhysicalAbilities.GRASP: 1, PhysicalAbilities.PUNCH: 1}, relative_size=10),
        BodyPart('humanoid_leg', {PhysicalAbilities.STAND: 1,
                                  PhysicalAbilities.MOVE: 1}, relative_size=25, threat_level=ThreatLevel.Major),
        BodyPart('humanoid_foot', {PhysicalAbilities.STAND: 1,
                                   PhysicalAbilities.MOVE: 1}, relative_size=10)
]
