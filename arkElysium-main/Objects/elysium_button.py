from pygame.draw_py import draw_line
from pygame.image import load
from OperatorTile import PlaceTile
from spritesheet import SpriteSheet


class ElysiumButton(PlaceTile):
    def __init__(self, surface, game, x, y, width_t, height_t, colour):
        elysssium = load("sprites/elysium_spreadsheet.jpg").convert_alpha()
        elysssium = SpriteSheet(elysssium)
        anim = [
            elysssium.get_image(0, 206, 382, 0.32, (0, 0, 0))
        ]
        agent_pic = SpriteSheet(
            load("sprites/Elysium_icon.webp").convert_alpha()).get_image(
            0, 180, 180, 0.5, (0, 0, 0))
        super().__init__(surface, game, x, y, anim=anim, script=lambda a: None, operator_data={}, agent_pic=agent_pic)
        self.orig_xy = x, y
        self.width = width_t
        self.height = height_t
        self.colour = colour
        self.is_draggable = True
        self.dragged = False
        self.dragged_pos = self.xy

    def hovered(self, cursor):
        print("???YES???")
        x, y = self.xy
        wdt, hgt = self.width, self.height
        x_neg = int(x - wdt / 2)
        x_pos = int(x + wdt / 2)
        y_neg = int(y - hgt / 2)
        y_pos = int(y + hgt / 2)
        tst_lines = [
            [[x_neg, int(y + hgt / 2)], [int(x + wdt / 2), int(y + hgt / 2)]],
            [[int(x - wdt / 2), int(y - hgt / 2)], [int(x + wdt / 2), int(y - hgt / 2)]],
            [[x_pos, y_pos], [int(x + wdt / 2), int(y - hgt / 2)]],
            [[x_neg, y_pos], [x_neg, y_neg]]
        ]
        draw_line(self.screen, [0, 255, 0], *tst_lines[0])
        draw_line(self.screen, [0, 255, 0], *tst_lines[1])
        draw_line(self.screen, [0, 255, 0], *tst_lines[2])
        draw_line(self.screen, [0, 255, 0], *tst_lines[3])




"""    def show_dragged(self, outline=False):
        sprite = self.anim[self.data["anim_frame"]]
        timer = self.data.get("anim_timer")
        if not timer:
            timer = Timer(0.01)
            self.data["anim_timer"] = timer
        self.screen.blit(sprite, self.xy)
        if outline:
            game_over_screen_fade = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
            game_over_screen_fade.fill((0, 0, 0))
            game_over_screen_fade.set_alpha(160)
            self.screen.blit(game_over_screen_fade, (0, 0))
            outline = self.outline_anim[self.data["anim_frame"]]
            self.screen.blit(outline, self.xy)
            sprite.set_alpha(255)
        if timer.is_late():
            self.data["anim_frame"] += 1
            self.data["anim_timer"] = Timer(0.01)
        if self.data["anim_frame"] >= len(self.anim):
            self.data["anim_frame"] = 0
        return

    def show(self, cursor):
        if self.dragged:
            self.xy = cursor[0] + self.dragged_pos[0], cursor[1] + self.dragged_pos[1]
            collided = self.game.game_tiles_collide(cursor)
            if collided:
                self.xy = (collided.xy[0]-10, collided.xy[1]-90)
                self.show_dragged(True)
                return
            self.show_dragged()
            return
        self.xy = self.orig_xy
        draw_rect(self.screen, self.colour, [*self.xy, self.width, self.height])
        self.screen.blit(self.agent_pic, self.xy)
        """



