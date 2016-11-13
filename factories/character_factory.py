from characters.character import Character, CharacterTemplate


class CharacterFactory(object):
    """
    At first this will only instantiate templates but eventually it should be able
    to pump out variations of a template ex: Adjusted to match player level.
    """
    def __init__(self, character_templates, factory_service, race_templates, class_templates):
        self.character_templates = character_templates
        self.template_instance_count = {}
        self.factory_service = factory_service
        self.race_templates = race_templates
        self.class_templates = class_templates

    def build(self, uid):
        """
        Builds a characters instance from a template using the uid.
        :param uid: uid of the template to instantiate.
        :return: Built instance from template.
        """

        character_template = next((template for template in self.character_templates if template.uid == uid), None)
        if character_template:
            return self._create_instance_of_template(character_template)
        else:
            raise Exception("Could not find template for UID " + uid)

    def _create_instance_of_template(self, character_template):
        instance_id = 0
        if character_template.uid in self.template_instance_count:
            instance_id = self.template_instance_count[character_template.uid]
            self.template_instance_count[character_template.uid] += 1
        else:
            self.template_instance_count[character_template.uid] = 1

        instance_uid = character_template.uid + "_" + instance_id
        new_instance = Character(
            uid=instance_uid,
            name=character_template.name

        )
        return Character(**character_template.__dict__)
