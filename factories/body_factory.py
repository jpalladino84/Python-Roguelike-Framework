from copy import deepcopy
from components.body import BodyPart
from components.abilities.physical_abilities import PhysicalAbilities


class BodyFactory(object):
    def __init__(self, body_templates, bodyparts_templates):
        self.body_templates = body_templates
        self.bodyparts_templates = bodyparts_templates

    def build_body(self, uid):
        """
        Builds a body instance from a template using the uid.
        :param uid: uid of the template to instantiate.
        :return: Built instance from template.
        """

        body_template = self.body_templates[uid]
        if body_template:
            body_instance = self._create_instance_of_template(body_template)
            self.assemble_body(body_instance)
            return body_instance
        else:
            raise Exception("Could not find template for UID " + uid)

    def build_bodypart(self, uid):
        template = self.bodyparts_templates[uid]

        # TODO This is a fix because of json pickle which turns an enum into a string...
        def str_to_enum(string_key):
            return PhysicalAbilities[string_key.split('.')[1].split(':')[0]]

        instance = BodyPart(
            uid=template.uid,
            physical_abilities={str_to_enum(key): value for key, value in template.physical_abilities.items()},
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
