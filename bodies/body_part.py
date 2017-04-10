from combat.enums import ThreatLevel


class BodyPart(object):
    def __init__(self, uid, physical_abilities=None, relative_size=1, threat_level=ThreatLevel.Minor):
        """
        :param uid: ID Name of the bodies part
        :param physical_abilities: Dictionary with abilities granted if any with its relative power as value
        :param relative_size: Percentage of bodies size, does not have to add up to 100
        """
        self.uid = uid
        self.relative_size = relative_size
        self.threat_level = threat_level
        if physical_abilities:
            self.physical_abilities = physical_abilities
        else:
            self.physical_abilities = {}
