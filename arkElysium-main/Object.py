from timer import Timer


class Hitbox:
    def __init__(self, x, y, h_width, h_height):
        self.xy = x, y
        self.width = h_width
        self.height = h_height

    @property
    def y(self):
        return self.xy[1]

    @property
    def x(self):
        return self.xy[0]

    def triggered(self, trigger_xy):
        return self.x >= trigger_xy[0] >= self.x * self.width * self.width & \
        self.y >= trigger_xy[1] >= self.y * self.height * self.height

class Object:

    def __init__(self,surface, game, x, y,  anim = None, script = lambda a: None, hitbox: Hitbox = None):
        self.screen = surface
        self.game = game
        game.colliders.append(self)
        self.anim = anim
        self.xy = [x, y]
        self.script = script
        self.hitbox = hitbox
        self.data = {"anim_frame": 0}

    def run(self):
        self.script(self)

    def is_hovered(self, cursor):
        return

    def show(self, cursor):
        if not self.anim:
            return
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

