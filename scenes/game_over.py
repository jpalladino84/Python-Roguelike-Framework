from base.scene import BaseScene
from stats.enums import StatsEnum


class GameOverScene(BaseScene):
    ID = "GameOver"

    def __init__(self, console_manager, scene_manager, game_context):
        super().__init__(console_manager, scene_manager, game_context)
        player = game_context.player
        self.player_name = player._name if player else "Unknown"
        self.depth_reached = game_context.depth_reached

        pool = player.experience_pool
        self.char_level = pool.total_level
        self.xp = pool.experience
        self.max_hp = int(player.stats.get_maximum_value(StatsEnum.Health))
        self.strength = int(player.stats.get_current_value(StatsEnum.Strength))
        self.dexterity = int(player.stats.get_current_value(StatsEnum.Dexterity))
        self.defense = player.get_armor_class()

    def render(self, **kwargs):
        self.main_console.clear()
        w = self.main_console.width

        def draw_centered(text, row):
            x = max(0, (w - len(text)) // 2)
            self.main_console.drawStr(x, row, text)

        draw_centered("*  G A M E   O V E R  *", 10)
        draw_centered("{} has fallen in the depths...".format(self.player_name), 13)

        col = (w - 26) // 2
        self.main_console.drawStr(col, 17, "Depth Reached:    {}".format(self.depth_reached))
        self.main_console.drawStr(col, 18, "Character Level:  {}".format(self.char_level))
        self.main_console.drawStr(col, 19, "Experience:       {}".format(self.xp))
        self.main_console.drawStr(col, 20, "Max HP:           {}".format(self.max_hp))
        self.main_console.drawStr(col, 21, "Strength:         {}".format(self.strength))
        self.main_console.drawStr(col, 22, "Dexterity:        {}".format(self.dexterity))
        self.main_console.drawStr(col, 23, "Defense:          {}".format(self.defense))

        draw_centered("[R] Play Again    [Q] Quit", 27)

    def handle_input(self, **kwargs):
        for key_event in kwargs.get("key_events", []):
            if key_event.type == 'KEYDOWN':
                if key_event.keychar.upper() == 'R':
                    self.game_context.depth_reached = 1
                    self.transition_to("CharacterCreationScene")
                elif key_event.keychar.upper() == 'Q':
                    raise SystemExit('Player quit.')
