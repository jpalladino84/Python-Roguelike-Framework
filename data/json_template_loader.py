import logging
import jsonpickle
import os
from components.material import materials
from data.python_templates.body_parts import body_parts
from data.python_templates.body import bodies
from data.python_templates.items import items
from data.python_templates.characters import characters
from data.python_templates.classes import character_classes
from data.python_templates.races import races

logger_ = logging.getLogger()


class JsonTemplateManager(object):
    TEMPLATE_FOLDER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    MATERIAL_FULL_PATH = os.path.join(TEMPLATE_FOLDER_PATH, 'materials.json')
    BODIES_FULL_PATH = os.path.join(TEMPLATE_FOLDER_PATH, 'bodies.json')
    BODYPARTS_FULL_PATH = os.path.join(TEMPLATE_FOLDER_PATH, 'bodyparts.json')
    MONSTERS_FULL_PATH = os.path.join(TEMPLATE_FOLDER_PATH, 'monsters.json')
    RACE_FULL_PATH = os.path.join(TEMPLATE_FOLDER_PATH, 'races.json')
    CLASSES_FULL_PATH = os.path.join(TEMPLATE_FOLDER_PATH, 'classes.json')
    ITEMS_FULL_PATH = os.path.join(TEMPLATE_FOLDER_PATH, 'items.json')

    def __init__(self):
        self.material_templates = {}
        self.bodies_templates = {}
        self.bodyparts_templates = {}
        self.monster_templates = {}
        self.race_templates = {}
        self.class_templates = {}
        self.item_templates = {}
        self.load_templates()

    def load_templates(self):
        self.material_templates = self._load_template_file(self.MATERIAL_FULL_PATH, 'Materials')
        self.bodies_templates = self._load_template_file(self.BODIES_FULL_PATH, 'Bodies')
        self.bodyparts_templates = self._load_template_file(self.BODYPARTS_FULL_PATH, 'Bodyparts')
        self.monster_templates = self._load_template_file(self.MONSTERS_FULL_PATH, 'Monsters')
        self.race_templates = self._load_template_file(self.RACE_FULL_PATH, 'Races')
        self.class_templates = self._load_template_file(self.CLASSES_FULL_PATH, 'Classes')
        self.item_templates = self._load_template_file(self.ITEMS_FULL_PATH, 'Items')

    @staticmethod
    def _load_template_file(full_path, template_name):
        if os.path.isfile(full_path):
            with open(full_path, 'r') as open_json_file:
                return jsonpickle.loads(open_json_file.read())
        else:
            logger_.error(template_name + " template file not found at " + full_path)

    def save_templates(self):
        self._save_templates_file(self.MATERIAL_FULL_PATH, self.material_templates)
        self._save_templates_file(self.BODIES_FULL_PATH, self.bodies_templates)
        self._save_templates_file(self.BODYPARTS_FULL_PATH, self.bodyparts_templates)
        self._save_templates_file(self.MONSTERS_FULL_PATH, self.monster_templates)
        self._save_templates_file(self.RACE_FULL_PATH, self.race_templates)
        self._save_templates_file(self.CLASSES_FULL_PATH, self.class_templates)
        self._save_templates_file(self.ITEMS_FULL_PATH, self.item_templates)

    @staticmethod
    def _save_templates_file(full_path, templates):
        with open(full_path, 'w') as new_json_file:
            new_json_file.write(jsonpickle.dumps(templates))


if __name__ == '__main__':
    template_manager = JsonTemplateManager()
    template_manager.material_templates = {material.uid: material for material in materials}
    template_manager.bodies_templates = {body.uid: body for body in bodies}
    template_manager.bodyparts_templates = {body_part.uid: body_part for body_part in body_parts}
    template_manager.race_templates = {race.uid: race for race in races}
    template_manager.class_templates = {c_class.uid: c_class for c_class in character_classes}
    template_manager.monster_templates = {monster.uid: monster for monster in characters}
    template_manager.item_templates = {item.uid: item for item in items}
    template_manager.save_templates()
