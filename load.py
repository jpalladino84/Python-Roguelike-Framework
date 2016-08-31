"""
Loads data from config files into the database
This needs to happen before the game fully loads.
"""
import json

from peewee import SqliteDatabase

from settings import DATABASE_NAME
from dungeon.config import LEVELS
from dungeon.models import Dungeon, DungeonObject, DungeonLevel
from item.models import Item
from character.models import Character
from character.components import CharacterClass
from character.config import PLAYER

TABLES = [Dungeon, DungeonObject, DungeonLevel, Item, Character, CharacterClass]
database = SqliteDatabase(DATABASE_NAME)


# TODO as a game gets bigger this could take longer... Should maybe insert a loading screen.
def load_game():
    init_database()
    load_levels()
    load_player()


def init_database():
    """
    Initialize the database with the necessary tables.

    This is to be done once at the start of the game.
    """
    database.connect()
    database.create_tables(TABLES, safe=True)


def load_levels():
    for level in LEVELS:
        new_level = DungeonLevel(
            level_id=level['id'],
            level_name=level['name'],
            level_desc=level['desc'],
            max_room_size=level['max_room_size'],
            min_room_size=level['min_room_size'],
            max_rooms=level['max_rooms'],
            is_final_level=level['is_final_level']
        )
        new_level.save()

        # load any items for the level
        for item in level['items']:
            new_item = Item(
                level_id=level['id'],
                name=item['name'],
                description=item['desc'],
                ascii_char=item['ascii_char'],
                inventory_list=item['inventory_list'],
                category=item['category'],
                stat_mod=item['stat_mod'],
                operation=item['op'],
                value=item['value']
            )
            new_item.save()

        load_monsters(level)


def load_monsters(level_config):

    level = DungeonLevel.get(DungeonLevel.level_id == level_config['id'])

    for monster in level_config['monsters']:
        character_class = monster['character_class']
        new_character_class = CharacterClass(
            class_name=character_class['name'],
            max_hp=character_class['max_hp'],
            hp=character_class['hp'],
            defense=character_class['defense'],
            attack=character_class['attack'],
            speed=character_class['speed'],
        )
        new_character_class.save()

        new_monster = Character(
            level=level,
            name=monster['name'],
            ascii_char=monster['ascii_char'],
            fgcolor=json.dumps(monster['fgcolor']),
            bgcolor=json.dumps(monster['bgcolor']),
            character_state=monster['character_state'],
            character_class=new_character_class,
        )
        new_monster.save()


def load_player():
    character_class = PLAYER['character_class']
    new_character_class = CharacterClass(
        class_name=character_class['name'],
        max_hp=character_class['max_hp'],
        hp=character_class['hp'],
        defense=character_class['defense'],
        attack=character_class['attack'],
        speed=character_class['speed'],
    )
    new_character_class.save()

    new_player = Character(
        name=PLAYER['name'],
        ascii_char=PLAYER['ascii_char'],
        fgcolor=json.dumps(PLAYER['fgcolor']),
        bgcolor=json.dumps(PLAYER['bgcolor']),
        character_state=PLAYER['character_state'],
        character_class=new_character_class
    )
    new_player.save()
