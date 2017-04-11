from factories.factory_service import FactoryService
from factories.body_factory import BodyFactory
from factories.character_factory import CharacterFactory
from data.python_templates.characters import weak_orc as weak_orc_template
import unittest


class CharacterFactoryTests(unittest.TestCase):
    def setUp(self):
        self.factory_service = FactoryService(body_factory=BodyFactory())
        self.factory_service.character_factory = CharacterFactory(factory_service=self.factory_service)

    def test_monster_instance(self):
        weak_orc = self.factory_service.build_character_instance_by_uid("weak_orc")
        assert weak_orc.name == weak_orc_template.name
