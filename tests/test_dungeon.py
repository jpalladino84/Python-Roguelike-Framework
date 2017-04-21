"""
Run with:
python2.7 -m unittest discover tests
"""
import unittest

from areas.level import Level
from managers.game_manager import GameManager
from components.stats import Stats


@unittest.skip('This is out of date and causes travis to fail')
class DungeonTestCase(unittest.TestCase):

    def setUp(self):
        self.game_manager = GameManager()
        level = Level()
        level.name = "DEFAULT"
        level.min_room_size = 1
        level.max_room_size = 10
        level.max_rooms = 10
        level.width = 80
        level.height = 45

        self.game_manager.game_context.player = self.game_manager.game_context.character_factory.create(
            "test", "warrior", "human", Stats(), "humanoid")
        self.game_manager.init_dungeon(level)
        self.level = level

    def tearDown(self):
        self.game_manager.console_manager._close_font()

    def test_generate_dungeon(self):
        self.assertEqual(self.level.name, "DEFAULT")

    def test_dungeon_contains_player(self):
        player = self.game_manager.game_context.player
        self.assertEqual(player.current_level, self.level)
        self.assertFalse(player.is_dead())

    def test_dungeon_contains_monsters(self):
        self.assertGreater(len(self.level.spawned_monsters), 0)
