from settings import DUNGEON_COLORS as COLORS


class GameScene(object):
    ID = "Game"

    def __init__(self, console_manager):
        self.console_manager = console_manager
        self.main_console = console_manager.main_console

    def render(self, **kwargs):
        """
        Render the areas, characters, items, etc..
        """
        current_level = self.player.location.level
        self.render_gui()
        self.set_tiles_background_color(current_level)

        player_x = self.player.location.local_x
        player_y = self.player.location.local_y

        def is_transparent_callback(x, y):
            return self.is_transparent(current_level, x, y)

        self.player.fov = map.quickFOV(player_x, player_y, is_transparent_callback, 'basic')
        # NB: Order in which things are render is important
        self.render_map()
        self.render_items()
        self.render_characters()
        self.render_player()

    def handle_input(self):
        pass

    def render_gui(self):
        CONSOLES['status'].drawStr(0, 2, "Health: {}\n\n".format(int(self.player.get_health())))
        CONSOLES['status'].drawStr(0, 5, "Attack Power: {}\n\n".format(self.player.get_attack()))
        CONSOLES['status'].drawStr(0, 8, "Defense: {}\n\n".format(self.player.get_defense()))
        CONSOLES['status'].drawStr(0, 11, "Speed: {}\n\n".format(self.player.get_speed()))

        self.console_manager.render_console(CONSOLES['action_log'], 0, 45)
        self.console_manager.render_console(CONSOLES['status'], 41, 45)

    def render_map(self, current_level, viewer_fov):
        for x, y in viewer_fov:
            if not x >= len(current_level.maze) and not y >= len(current_level.maze[x]):
                try:
                    if current_level.maze[x][y].is_blocked:
                        self.main_console.drawChar(x, y, '#', fgcolor=COLORS['light_wall'])
                        current_level.maze[x][y].is_explored = True
                    if current_level.maze[x][y].is_ground is True:
                        self.main_console.drawChar(x, y, '.', fgcolor=COLORS['light_ground'])
                        current_level.maze[x][y].is_explored = True
                except IndexError:
                    raise

    def render_items(self):
        for item in self.items:
            x, y = item.location.coords
            if (x, y) in self.player.fov:
                console.drawChar(x, y, **item.display.get_draw_info())

    def render_characters(self):
        # draw monsters
        for monster in self.player.location.level.spawned_monsters:
            x, y = monster.location.get_local_coords()
            if (x, y) in self.player.fov:
                console.drawChar(x, y, **monster.display.get_draw_info())

    def render_player(self):
        # draw player2
        console.drawChar(player_x, player_y, **self.player.display.get_draw_info())

    def set_tiles_background_color(self, current_level):
        for y in range(current_level.height):
            for x in range(current_level.width):
                tile = current_level.maze[x][y]
                wall = tile.block_sight
                ground = tile.is_ground

                if tile.is_explored:
                    if wall:
                        console.drawChar(x, y, '#', fgcolor=COLORS['dark_gray_wall'])
                    elif ground:
                        console.drawChar(x, y, '.', fgcolor=COLORS['dark_ground'])

    @staticmethod
    def is_transparent(current_level, x, y):
        """
        Used by map.quickFOV to determine which tile fall within the players "field of view"
        """
        try:
            # Pass on IndexErrors raised for when a player gets near the edge of the screen
            # and tile within the field of view fall out side the bounds of the maze.
            tile = current_level.maze[x][y]
            if tile.block_sight and tile.is_blocked:
                return False
            else:
                return True
        except IndexError:
            pass