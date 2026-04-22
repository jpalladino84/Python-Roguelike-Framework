import tdl

from base.scene import BaseScene
from components.stats import make_character_stats
from data.python_templates.outfits import starter_warrior
from ui.controls import InputControl


# figlet standard font
HEADER_ART = [
    r" _____                       __   __                    _                        _  ",
    r"|  ___|__  _ __ __ _  ___   \ \ / /__  _   _ _ __     | |    ___  __ _  ___ _ _  __| |",
    r"| |_ / _ \| '__/ _` |/ _ \   \ V / _ \| | | | '__|    | |   / _ \/ _` |/ _ \ '_ \/ _` |",
    r"|  _| (_) | | | (_| |  __/    | | (_) | |_| | |       | |__|  __/ (_| |  __/ | | \__,_|",
    r"|_|  \___/|_|  \__, |\___|    |_|\___/ \__,_|_|       |_____\___|\__, |\___|_| |_\__,_|",
    r"                |___/                                              |___/                 ",
]

WARRIOR_ART = [
    r"    /\ ",
    "   /  \\",
    r"  / /\ \ ",
    " /-'  '-\\",
    r"   (  ) ",
    r"  --|--  ",
    r" /  |  \ ",
    r"'   |   '",
    r"    |    ",
    r"   / \   ",
    "  /   \\  ",
]

SWORD_ART = [
    r"    |    ",
    r"    |    ",
    r"   \|/   ",
    r"  --*--  ",
    r"    |    ",
    r"    |    ",
    r"   (__)  ",
]

# colors — same palette as main menu
GOLD       = (220, 180,  40)
GOLD_DIM   = (120,  90,  15)
BLOOD      = (200,  30,  30)
BORDER_CLR = ( 80,  55,  20)
TEXT_CLR   = (200, 200, 180)
DIM_CLR    = ( 90,  90,  70)
INPUT_CLR  = (255, 255, 100)
INPUT_BOX  = ( 60,  50,  20)
CONFIRM_CLR= (100, 220, 100)
INACTIVE   = (140, 140, 100)
BLACK      = (  0,   0,   0)
WARRIOR_CLR= (180, 160, 100)
ACCENT_CLR = (160, 120,  30)


def _center_x(w, text):
    return max(0, (w - len(text)) // 2)


class CharacterCreationScene(BaseScene):
    ID = "CharacterCreation"

    def __init__(self, console_manager, scene_manager, game_context):
        super().__init__(console_manager, scene_manager, game_context)
        self.character_factory = self.game_context.character_factory
        self.body_factory = self.game_context.body_factory
        self.control_name = InputControl("Name:")
        self.active_control = self.control_name

    def render(self, **kwargs):
        c = self.main_console
        c.clear()
        w = c.width   # 100
        h = c.height  # 60

        # --- border ---
        for x in range(w):
            c.drawChar(x, 0,     char='=', fgcolor=BORDER_CLR, bgcolor=BLACK)
            c.drawChar(x, h - 1, char='=', fgcolor=BORDER_CLR, bgcolor=BLACK)
        for y in range(1, h - 1):
            c.drawChar(0,     y, char='|', fgcolor=BORDER_CLR, bgcolor=BLACK)
            c.drawChar(w - 1, y, char='|', fgcolor=BORDER_CLR, bgcolor=BLACK)
        for corner_x, corner_y in [(0, 0), (w-1, 0), (0, h-1), (w-1, h-1)]:
            c.drawChar(corner_x, corner_y, char='+', fgcolor=BORDER_CLR, bgcolor=BLACK)

        # --- header title (smaller, use simple styled text if art is too wide) ---
        header_y = 2
        title_line = "~  F O R G E   Y O U R   L E G E N D  ~"
        c.drawStr(_center_x(w, title_line), header_y, title_line, fgcolor=GOLD, bgcolor=BLACK)

        sub_line = "Every great hero needs a name."
        c.drawStr(_center_x(w, sub_line), header_y + 1, sub_line, fgcolor=GOLD_DIM, bgcolor=BLACK)

        # decorative divider
        divider = "-~-" * 16 + "-"
        c.drawStr(_center_x(w, divider), header_y + 2, divider, fgcolor=GOLD_DIM, bgcolor=BLACK)

        # --- warrior silhouette (left side) ---
        warrior_x = 8
        warrior_y = 10
        for i, line in enumerate(WARRIOR_ART):
            c.drawStr(warrior_x, warrior_y + i, line, fgcolor=WARRIOR_CLR, bgcolor=BLACK)

        # sword below warrior
        sword_y = warrior_y + len(WARRIOR_ART) + 1
        for i, line in enumerate(SWORD_ART):
            c.drawStr(warrior_x, sword_y + i, line, fgcolor=ACCENT_CLR, bgcolor=BLACK)

        # label under warrior
        c.drawStr(warrior_x, sword_y + len(SWORD_ART) + 1,
                  " Warrior ", fgcolor=GOLD_DIM, bgcolor=BLACK)

        # --- name input area (center-right) ---
        box_x = 30
        box_y = 14
        box_w = 56
        box_h = 7

        # draw input box border
        c.drawStr(box_x, box_y, '+' + '-' * (box_w - 2) + '+', fgcolor=ACCENT_CLR, bgcolor=BLACK)
        for row in range(1, box_h - 1):
            c.drawChar(box_x,           box_y + row, char='|', fgcolor=ACCENT_CLR, bgcolor=BLACK)
            c.drawChar(box_x + box_w - 1, box_y + row, char='|', fgcolor=ACCENT_CLR, bgcolor=BLACK)
        c.drawStr(box_x, box_y + box_h - 1,
                  '+' + '-' * (box_w - 2) + '+', fgcolor=ACCENT_CLR, bgcolor=BLACK)

        # box title
        box_title = "[ ENTER YOUR NAME ]"
        c.drawStr(box_x + (box_w - len(box_title)) // 2, box_y, box_title,
                  fgcolor=GOLD, bgcolor=BLACK)

        # name prompt
        prompt = "Name: "
        name_display = self.control_name.answer
        cursor = "_" if self.active_control else ""
        name_row = box_y + 2
        c.drawStr(box_x + 3, name_row, prompt, fgcolor=TEXT_CLR, bgcolor=BLACK)
        c.drawStr(box_x + 3 + len(prompt), name_row,
                  name_display + cursor, fgcolor=INPUT_CLR, bgcolor=BLACK)

        # hint text
        if self.active_control:
            hint = "Type your name and press ENTER"
            c.drawStr(box_x + (box_w - len(hint)) // 2, box_y + 4,
                      hint, fgcolor=DIM_CLR, bgcolor=BLACK)
        else:
            # name confirmed — show confirm prompt
            ready_line = "Ready, {}!".format(self.control_name.answer or "Adventurer")
            c.drawStr(box_x + (box_w - len(ready_line)) // 2, box_y + 4,
                      ready_line, fgcolor=CONFIRM_CLR, bgcolor=BLACK)

        # --- lore text ---
        lore_y = box_y + box_h + 2
        lore_lines = [
            "You stand at the entrance to a vast dungeon. Monsters lurk in the shadows,",
            "treasure glitters in forgotten halls, and danger waits around every corner.",
            "Only the brave — or the foolish — venture below.",
        ]
        for i, line in enumerate(lore_lines):
            c.drawStr(_center_x(w, line), lore_y + i, line, fgcolor=DIM_CLR, bgcolor=BLACK)

        # --- action prompt ---
        action_y = lore_y + len(lore_lines) + 2
        if not self.active_control:
            confirm = "(a) Begin Adventure"
            c.drawStr(_center_x(w, confirm), action_y, confirm, fgcolor=CONFIRM_CLR, bgcolor=BLACK)
            back = "(ESC) Go Back"
            c.drawStr(_center_x(w, back), action_y + 1, back, fgcolor=DIM_CLR, bgcolor=BLACK)
        else:
            tip = "Tip: You are a seasoned Warrior. Steel yourself — the dungeon is unforgiving."
            c.drawStr(_center_x(w, tip), action_y, tip, fgcolor=ACCENT_CLR, bgcolor=BLACK)

        # --- bottom tagline ---
        tagline = "~ Your legend begins now ~"
        c.drawStr(_center_x(w, tagline), h - 3, tagline, fgcolor=GOLD_DIM, bgcolor=BLACK)

        tdl.flush()

    def handle_input(self, **kwargs):
        if self.active_control:
            self.active_control.handle_input(**kwargs)
            if self.active_control.finished:
                self.active_control = None
        else:
            key_events = kwargs["key_events"]
            for key_event in key_events:
                if key_event.type == 'KEYDOWN':
                    if key_event.keychar.upper() == 'A':
                        name = self.control_name.answer.strip() or "Adventurer"
                        self.game_context.player = self.character_factory.create(
                            name=name,
                            class_uid="warrior",
                            race_uid="human",
                            stats=make_character_stats(),
                            body_uid="humanoid"
                        )
                        starter_warrior.apply(self.game_context.player)
                        self.transition_to("GameScene")
                    elif key_event.key == 'ESCAPE':
                        self.transition_to("MainMenuScene")
