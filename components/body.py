import logging
import random

import six

from abilities.physical_abilities import PhysicalAbilities
from bodies.body_part_tree import BodypartTree
from combat.enums import ThreatLevel
from components.component import Component

logger_ = logging.getLogger()


class Body(Component):
    NAME = "body"
    """
    Height is in feet, Weight in pounds
    """
    def __init__(self, uid, bodypart_tree, name="", height=0, weight=0, outer_material_uid=None,
                 inner_material_uid=None, structural_material_uid=None, blood_uid=None):
        super().__init__()
        self.uid = uid
        self.bodypart_tree = bodypart_tree
        self.name = name
        self.height = height
        self.weight = weight
        self.outer_material_uid = outer_material_uid
        self.inner_material_uid = inner_material_uid
        self.structural_material_uid = structural_material_uid
        self.blood_uid = blood_uid

    def copy(self):
        return Body(
            uid=self.uid,
            name=self.name,
            bodypart_tree=self.bodypart_tree.copy(),
            height=self.height,
            weight=self.weight,
            outer_material_uid=self.outer_material_uid,
            inner_material_uid=self.inner_material_uid,
            structural_material_uid=self.structural_material_uid,
            blood_uid=self.blood_uid,
        )

    def __str__(self):
        return "Body({})".format(self.name)

    def get_body_part(self, uid):
        for node in self.bodypart_tree.nodes:
            if node.instance.uid == uid:
                return node.instance

    def get_body_parts(self, uid):
        return [node.instance for node in
                self.bodypart_tree.nodes
                if node.instance.uid == uid]

    @staticmethod
    def _random_roll_body_part(body_parts):
        tries = 0
        max_tries = 3
        while tries < max_tries:
            tries += 1
            for node in body_parts:
                if random.randrange(0, 100) <= node.instance.relative_size:
                    return node

        return random.choice(body_parts)

    def get_random_body_part_for_threat_level(self, threat_level):
        size_sorted_body_parts = [node for node in self.bodypart_tree.nodes
                                  if node.instance.threat_level == threat_level]
        if not size_sorted_body_parts:
            if threat_level < ThreatLevel.Fatal:
                return self.get_random_body_part_for_threat_level(ThreatLevel[threat_level.value + 1])
            else:
                return self.get_random_body_part_by_relative_size()

        return self._random_roll_body_part(size_sorted_body_parts)

    def get_random_body_part_by_relative_size(self):
        size_sorted_body_parts = sorted([node for node in self.bodypart_tree.nodes
                                         if node.connection_type == BodypartTree.CONNECTION_TYPE_ATTACHED],
                                        key=lambda node: node.instance.relative_size, reverse=True)

        return self._random_roll_body_part(size_sorted_body_parts)

    def get_grasp_able_body_parts(self):
        return [node.instance for node in self.bodypart_tree.nodes
                if PhysicalAbilities.GRASP in node.instance.physical_abilities]

    def get_physical_abilities(self):
        abilities = {}
        for node in self.bodypart_tree.nodes:
            for ability_name, ability_value in six.iteritems(node.instance.physical_abilities):
                if ability_name not in abilities:
                    abilities[ability_name] = ability_value
                else:
                    if abilities[ability_name] < ability_value:
                        abilities[ability_name] = ability_value

        return abilities
