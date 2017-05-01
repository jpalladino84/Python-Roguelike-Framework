from data.python_templates.items import item_templates
from data.python_templates.material import material_templates
from items.item import Item


class ItemFactory(object):
    """
    At first this will only instantiate templates but eventually it should be able
    to pump out variations of a template ex: Adjusted to match player level.
    """
    def __init__(self):
        self.template_instance_count = {}

    def build(self, uid):
        """
        Builds an item instance from a template using the uid.
        :param uid: uid of the template to instantiate.
        :return: Built instance from template.
        """

        item_instance = item_templates[uid]
        if item_instance:
            return self._create_instance_of_template(item_instance)
        else:
            raise Exception("Could not find template for UID " + uid)

    def _create_instance_of_template(self, item_template):
        instance_id = 0
        if item_template.uid in self.template_instance_count:
            instance_id = self.template_instance_count[item_template.uid]
            self.template_instance_count[item_template.uid] += 1
        else:
            self.template_instance_count[item_template.uid] = 1

        instance_uid = item_template.uid + "_" + str(instance_id)
        new_instance = Item(
            uid=instance_uid,
            name=item_template.name,
            description=item_template.description,
            display=item_template.display.copy(),
        )
        item_template.copy_to(new_instance)

        return new_instance

    def get_material_template_by_uid(self, uid):
        return material_templates[uid]

    def get_item_template_by_uid(self, uid):
        return item_templates[uid]
