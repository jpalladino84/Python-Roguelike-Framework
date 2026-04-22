import tdl

from base.scene import BaseScene


# figlet standard font
TITLE_ART = [
    r" ____  _   _ _   _  ____ _____ ___  _   _ ",
    r"|  _ \| | | | \ | |/ ___| ____/ _ \| \ | |",
    r"| | | | | | |  \| | |  _|  _|| | | |  \| |",
    r"| |_| | |_| | |\  | |_| | |__| |_| | |\  |",
    r"|____/ \___/|_| \_|\____|_____\___/|_| \_|",
]

DEPTHS_ART = [
    r" ____  _____ ____ _____ _   _ ____  ",
    r"|  _ \| ____|  _ \_   _| | | / ___|",
    r"| | | |  _| | |_) || | | |_| \___ \ ",
    r"| |_| | |___| .__ / | | |  _  |___) |",
    r"|____/|_____|_|    |_| |_| |_|____/ ",
]

SKULL_ART = [
    r"   .-.   ",
    r"  (o o)  ",
    r"  | O |  ",
    r"   \-/   ",
    r" __|_|__ ",
    r"/       \\",
]

TORCH_ART = [
    r" ) ",
    r"(|)",
    r" | ",
    r"/_\ ",
]

DIVIDER = "-~-" * 16 + "-"

FLAVOR_LINES = [
    "Venture into the darkness. Claim glory or meet your doom.",
    "",
    "(a) Play          (b) Quit",
]

# colors
GOLD       = (220, 180,  40)
GOLD_DIM   = (120,  90,  15)
BLOOD      = (200,  30,  30)
BLOOD_DIM  = (110,  15,  15)
TORCH_CLR  = (255, 180,  50)
BORDER_CLR = ( 80,  55,  20)
SKULL_CLR  = (160, 160, 160)
TEXT_CLR   = (200, 200, 180)
DIM_CLR    = ( 90,  90,  70)
OPTION_CLR = (255, 240, 160)
BLACK      = (  0,   0,   0)


def _center_x(console_width, text):
    return max(0, (console_width - len(text)) // 2)


class MainMenuScene(BaseScene):
    ID = "MainMenu"

    def __init__(self, console_manager, scene_manager, game_context):
        super().__init__(console_manager, scene_manager, game_context)

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
        c.drawChar(0,     0,     char='+', fgcolor=BORDER_CLR, bgcolor=BLACK)
        c.drawChar(w - 1, 0,     char='+', fgcolor=BORDER_CLR, bgcolor=BLACK)
        c.drawChar(0,     h - 1, char='+', fgcolor=BORDER_CLR, bgcolor=BLACK)
        c.drawChar(w - 1, h - 1, char='+', fgcolor=BORDER_CLR, bgcolor=BLACK)

        # --- torches flanking the title ---
        torch_start_y = 3
        for i, line in enumerate(TORCH_ART):
            c.drawStr(4, torch_start_y + i, line, fgcolor=TORCH_CLR, bgcolor=BLACK)
            c.drawStr(w - 4 - len(line), torch_start_y + i, line, fgcolor=TORCH_CLR, bgcolor=BLACK)

        # --- DUNGEON title (gold) ---
        title_y = 3
        for i, line in enumerate(TITLE_ART):
            x = _center_x(w, line)
            # shadow one pixel down/right in dim gold
            c.drawStr(x + 1, title_y + i + 1, line, fgcolor=GOLD_DIM, bgcolor=BLACK)
            c.drawStr(x,     title_y + i,     line, fgcolor=GOLD,     bgcolor=BLACK)

        # --- DEPTHS subtitle (blood red) ---
        depths_y = title_y + len(TITLE_ART) + 1
        for i, line in enumerate(DEPTHS_ART):
            x = _center_x(w, line)
            c.drawStr(x + 1, depths_y + i + 1, line, fgcolor=BLOOD_DIM, bgcolor=BLACK)
            c.drawStr(x,     depths_y + i,     line, fgcolor=BLOOD,     bgcolor=BLACK)

        # --- decorative divider ---
        div_y = depths_y + len(DEPTHS_ART) + 1
        div_x = _center_x(w, DIVIDER)
        c.drawStr(div_x, div_y, DIVIDER, fgcolor=GOLD_DIM, bgcolor=BLACK)

        # --- skull art (centered) ---
        skull_y = div_y + 2
        skull_width = max(len(line) for line in SKULL_ART)
        skull_x = _center_x(w, ' ' * skull_width)
        for i, line in enumerate(SKULL_ART):
            c.drawStr(skull_x, skull_y + i, line, fgcolor=SKULL_CLR, bgcolor=BLACK)

        # --- dungeon scene below skull ---
        scene_y = skull_y + len(SKULL_ART) + 1
        scene = [
            r"     #########################################     ",
            r"     #  )) .                       . ((  #     ",
            r"     # (||) .  Enter if you dare  . (||) #     ",
            r"     #  ||                           ||  #     ",
            r"     # /##\  * * * * * * * * * * * /##\ #     ",
            r"     #########################################     ",
        ]
        for i, line in enumerate(scene):
            x = _center_x(w, line)
            c.drawStr(x, scene_y + i, line, fgcolor=DIM_CLR, bgcolor=BLACK)

        # --- flavor text and options ---
        options_y = scene_y + len(scene) + 2
        for i, line in enumerate(FLAVOR_LINES):
            color = OPTION_CLR if line.startswith('(') else TEXT_CLR
            x = _center_x(w, line) if line else 0
            c.drawStr(x, options_y + i, line, fgcolor=color, bgcolor=BLACK)

        # --- bottom tagline ---
        tagline = "~ The dungeon awaits ~"
        c.drawStr(_center_x(w, tagline), h - 3, tagline, fgcolor=GOLD_DIM, bgcolor=BLACK)

        tdl.flush()

    def handle_input(self, **kwargs):
        key_events = kwargs["key_events"]
        for key_event in key_events:
            if key_event.keychar.upper() == 'A':
                self.transition_to("CharacterCreationScene")
            elif key_event.keychar.upper() == 'B':
                raise SystemExit('The window has been closed.')
