class Display(object):
    def __init__(self):
        self.foreground_color = None
        self.background_color = None
        self.ascii_character = None

    def get_draw_info(self):
        return dict(char=str(self.ascii_character), fgcolor=self.foreground_color, bgcolor=self.background_color)
