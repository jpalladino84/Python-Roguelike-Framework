from data.json_template_loader import JsonTemplateManager
from factories.factory_service import FactoryService
from factories.body_factory import BodyFactory
from factories.character_factory import CharacterFactory
import unittest


class CharacterFactoryTests(unittest.TestCase):
    def setUp(self):
        self.template_manager = JsonTemplateManager()
        self.template_manager.load_templates()
        self.factory_service = FactoryService(
            template_loader=self.template_manager,
            body_factory=BodyFactory(self.template_manager.bodies_templates)
        )
        self.factory_service.character_factory = CharacterFactory(
            character_templates=self.template_manager.monster_templates,
            factory_service=self.factory_service,
            race_templates=self.template_manager.race_templates,
            class_templates=self.template_manager.class_templates
        )

    def test_monster_instance(self):
        weak_orc_template = self.template_manager.monster_templates["weak_orc"]
        weak_orc = self.factory_service.build_character_instance_by_uid("weak_orc")
        assert weak_orc.name == weak_orc_template.name
