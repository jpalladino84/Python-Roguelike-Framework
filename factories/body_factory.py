from copy import deepcopy

from abilities.physical_abilities import PhysicalAbilities
from bodies.body_part import BodyPart
from data.python_templates.body_parts import body_part_templates
from data.python_templates.body import body_templates


class BodyFactory(object):
    def build_body(self, uid):
        """
        Builds a bodies instance from a template using the uid.
        :param uid: uid of the template to instantiate.
        :return: Built instance from template.
        """

        body_template = body_templates[uid]
        if body_template:
            body_instance = self._create_instance_of_template(body_template)
            self.assemble_body(body_instance)
            return body_instance
        else:
            raise Exception("Could not find template for UID " + uid)

    def build_bodypart(self, uid):
        template = body_part_templates[uid]
        instance = BodyPart(
            uid=template.uid,
            physical_abilities=template.physical_abilities,
            relative_size=template.relative_size,
            threat_level=template.threat_level
        )

        return instance

    def assemble_body(self, body):
        for node in body.bodypart_tree.nodes:
            node.instance = self.build_bodypart(node.body_part_uid)

    @staticmethod
    def _create_instance_of_template(body_template):
        return deepcopy(body_template)
