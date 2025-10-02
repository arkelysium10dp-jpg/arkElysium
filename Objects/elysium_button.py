from pygame import draw
from pygame.image import load
from Tile import Tile
from spritesheet import SpriteSheet
from timer import Timer


class ElysiumButton(Tile):
    def __init__(self, surface, x, y, width_t, height_t, colour, is_draggable):
        super().__init__(surface, x, y, width_t, height_t, colour, is_draggable)

        elysssium = load("sprites/elysium_spreadsheet.jpg").convert_alpha()
        elysssium = SpriteSheet(elysssium)
        self.anim = [
            elysssium.get_image(0, 206, 382, 0.40, (0, 0, 0))
        ]
        """
        elysssium = pygame.image.load("sprites/elysium_spreadsheet.jpg").convert_alpha()
        elysssium = SpriteSheet(elysssium)
        elysssium_anim = []
        for i in range(0, 42):
            elysssium_anim.append(elysssium.get_image(i,206, 382, 0.40,(0,0,0)))
        """

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
            self.show_dragged(cursor)
            return
        draw.rect(self.surface, self.colour, [*self.xy, self.width, self.height])

