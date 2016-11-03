class Display(object):
    def __init__(self):
        self.foreground_color = (255, 255, 255)
        self.background_color = (0, 0, 0)
        self.ascii_character = "@"

    def get_draw_info(self):
        return dict(char=str(self.ascii_character), fgcolor=self.foreground_color, bgcolor=self.background_color)
