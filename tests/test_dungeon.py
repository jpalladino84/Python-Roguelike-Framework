"""
Run with:
python2.7 -m unittest discover tests
"""
import json
import unittest

from peewee import SqliteDatabase

import load
from dungeon.models import Dungeon, DungeonLevel, DungeonObject
from item.models import Item
from character.models import Character
from character.components import CharacterClass
from character.config import ORC, TROLL
from dungeon.generator import DungeonGenerator

database = SqliteDatabase('roguelike_test.db')
TEST_TABLES = [Dungeon, DungeonObject, DungeonLevel, Item, Character, CharacterClass]


LEVEL_FIXTURE = {
    'id': 1,
    'name': 'Test Level',
    'desc': 'A level meant for testing.',
    'max_room_size': 14,
    'min_room_size': 10,
    'max_rooms': 10,
    'is_final_level': False,
    'items': [],
    'monsters': [
        ORC,
        ORC,
        TROLL
    ]
}


class DungeonTestCase(unittest.TestCase):

    def setUp(self):
        database.connect()
        database.create_tables(TEST_TABLES, safe=True)

        load.load_player()
        dungeon_generator = DungeonGenerator()
        new_test_level = DungeonLevel(
            level_id=LEVEL_FIXTURE['id'],
            level_name=LEVEL_FIXTURE['name'],
            level_desc=LEVEL_FIXTURE['desc'],
            max_room_size=LEVEL_FIXTURE['max_room_size'],
            min_room_size=LEVEL_FIXTURE['min_room_size'],
            max_rooms=LEVEL_FIXTURE['max_rooms'],
            is_final_level=LEVEL_FIXTURE['is_final_level']
        )
        new_test_level.save()
        load.load_monsters(LEVEL_FIXTURE)
        dungeon_generator.generate(new_test_level)

    def tearDown(self):
        database.truncate_tables(TEST_TABLES)
        database.drop_tables(TEST_TABLES)
        database.close()

    def test_generate_dungeon(self):
        dungeon = (Dungeon
                   .select()
                   .join(DungeonLevel)
                   .where(DungeonLevel.level_id == 1).get())

        self.assertEqual(dungeon.level_id, 1)

    def test_dungeon_contains_player(self):
        player = Character.get(Character.name == 'player')
        self.assertEqual(player.level.level_id, 1)
        self.assertEqual(player.ascii_char, '@')
        self.assertEqual(player.character_state, 'alive')
        self.assertIsNotNone(player.dungeon_object.coords)
        self.assertEqual(type(json.loads(player.dungeon_object.coords)), list)

    def test_dungeon_contains_monsters(self):
        monsters = [m for m in Character.select().join(DungeonLevel).where(
            (DungeonLevel.level_id == 1) & (Character.name != 'player'))]
        self.assertEqual(len(monsters), 3)
        for m in monsters:
            self.assertIsNotNone(m.dungeon_object.coords)
            self.assertEqual(type(json.loads(m.dungeon_object.coords)), list)
