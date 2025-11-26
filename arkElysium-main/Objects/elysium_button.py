import pygame
from pygame import draw
from pygame.image import load

from InterfaceObject import InterfaceObject
from Object import Hitbox
from outliner import generate_outline
from spritesheet import SpriteSheet
from timer import Timer



# TODO: to be placeable, to make object from tile
class ElysiumButton(InterfaceObject):
    def __init__(self, surface, game, x, y, width_t, height_t, colour, hitbox):
        self.hitbox = Hitbox(x, y, width_t, height_t)
        super().__init__(surface, game, x, y, anim=None, script=lambda a: None, hitbox=self.hitbox, hoverable=True,
                         draggable=True)
        self.orig_xy = x, y
        self.width = width_t
        self.height = height_t
        self.colour = colour
        self.is_draggable = True
        self.dragged = False
        self.dragged_pos = self.xy

        elysssium = load("sprites/elysium_spreadsheet.jpg").convert_alpha()
        elysssium = SpriteSheet(elysssium)
        self.anim = [
            elysssium.get_image(0, 206, 382, 0.40, (0, 0, 0))
        ]
        self.outline_anim = generate_outline(self.anim,180, 180)
        self.agent_pic = SpriteSheet(
            load("sprites/Elysium_icon.webp").convert_alpha()).get_image(
            0, 180, 180, 0.5, (0,0,0))

    def show_dragged(self, outline=False):
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
        x, y = self.xy
        # TODO: TOFIX
        pygame.draw.line(self.screen, (255, 255, 255), (x, y - 160), (x + 160, y), 5)
        pygame.draw.line(self.screen, (255, 255, 0), (x - 160, y), (x, y - 160), 5)
        pygame.draw.line(self.screen, (255, 255, 255), (x, y + 160), (x - 160, y), 5)
        pygame.draw.line(self.screen, (255, 255, 0), (x + 160, y), (x, y + 160), 5)
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
        draw.rect(self.screen, self.colour, [*self.xy, self.width, self.height])
        self.screen.blit(self.agent_pic, self.xy)



