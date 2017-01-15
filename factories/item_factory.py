from components.stats import ItemStats
from components.display import Display
from items.item import Item


class ItemFactory(object):
    """
    At first this will only instantiate templates but eventually it should be able
    to pump out variations of a template ex: Adjusted to match player level.
    """
    def __init__(self, item_templates, material_templates):
        self.item_templates = item_templates
        self.template_instance_count = {}
        self.material_templates = material_templates

    def build(self, uid):
        """
        Builds an item instance from a template using the uid.
        :param uid: uid of the template to instantiate.
        :return: Built instance from template.
        """

        item_instance = self.item_templates[uid]
        if item_instance:
            return self._create_instance_of_template(item_instance)
        else:
            raise Exception("Could not find template for UID " + uid)

    def create(self, uid, name, description, display, material_uid, stats, melee_damage_type, wearable_bodyparts_uid):
        """
        Creates a new item based on arguments
        :return:
        """
        instance_id = 0
        if uid in self.template_instance_count:
            instance_id = self.template_instance_count[uid]
            self.template_instance_count[uid] += 1
        else:
            self.template_instance_count[uid] = 1

        instance_uid = uid + "_" + str(instance_id)
        new_instance = Item(
            uid=instance_uid,
            name=name,
            description=description,
            display=display,
            material=self.get_material_template_by_uid(material_uid),
            stats=stats,
            melee_damage_type=melee_damage_type,
            wearable_bodyparts_uid=wearable_bodyparts_uid
        )
        return new_instance

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
            display=Display(**item_template.display.__dict__),
            material=self.get_material_template_by_uid(item_template.material_uid),
            stats=ItemStats(**item_template.base_stats.__dict__),
            melee_damage_type=item_template.melee_damage_type,
            wearable_bodyparts_uid=item_template.wearable_bodyparts_uid
        )

        return new_instance

    def get_material_template_by_uid(self, uid):
        if uid in self.material_templates:
            return self.material_templates[uid]

    def get_item_template_by_uid(self, uid):
        if uid in self.item_templates:
            return self.item_templates[uid]
