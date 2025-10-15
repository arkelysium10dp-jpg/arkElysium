from pygame import draw
from pygame.image import load
from Tile import Tile
from spritesheet import SpriteSheet
from timer import Timer

# TODO: to be placeable, to make object from tile
class ElysiumButton(Tile):
    def __init__(self, surface, game, x, y, width_t, height_t, colour, hitbox):
        super().__init__(surface, game, x, y, width_t, height_t, colour, True)
        self.orig_xy = x, y

        elysssium = load("sprites/elysium_spreadsheet.jpg").convert_alpha()
        elysssium = SpriteSheet(elysssium)
        self.anim = [
            elysssium.get_image(0, 206, 382, 0.40, (0, 0, 0))
        ]
        self.agent_pic = SpriteSheet(
            load("sprites/Elysium_icon.webp").convert_alpha()).get_image(
            0, 180, 180, 0.5, (0,0,0))

    def show_dragged(self, cursor):
        sprite = self.anim[self.data["anim_frame"]]
        timer = self.data.get("anim_timer")
        if not timer:
            timer = Timer(0.01)
            self.data["anim_timer"] = timer
        self.screen.blit(sprite, self.xy)
        if timer.is_late():
            self.data["anim_frame"] += 1
            self.data["anim_timer"] = Timer(0.01)
        if self.data["anim_frame"] >= len(self.anim):
            self.data["anim_frame"] = 0
        return

    def show(self, cursor):
        if self.dragged:
            self.xy = cursor[0] + self.dragged_pos[0], cursor[1] + self.dragged_pos[1]
            collided = self.game.game_tiles_collide(self.xy)
            if collided:
                self.xy = collided.xy
            self.show_dragged(cursor)
            return
        if self.xy != self.orig_xy:
            if self.game.collides_with(self.xy):
                # TODO: When dragged to tile show attached agent
                pass

        self.xy = self.orig_xy
        draw.rect(self.surface, self.colour, [*self.xy, self.width, self.height])
        self.screen.blit(self.agent_pic, self.xy)

