from copy import deepcopy


class BodyFactory(object):
    def __init__(self, body_templates):
        self.body_templates = body_templates

    def build(self, uid):
        """
        Builds a body instance from a template using the uid.
        :param uid: uid of the template to instantiate.
        :return: Built instance from template.
        """

        body_template = self.body_templates[uid]
        if body_template:
            return self._create_instance_of_template(body_template)
        else:
            raise Exception("Could not find template for UID " + uid)

    @staticmethod
    def _create_instance_of_template(body_template):
        return deepcopy(body_template)
