from timer import Timer
from pygame import Surface

class TriggerBox:
    def __init__(self, x, y, h_width, h_height):
        self.xy = x, y # central xy
        self.width = h_width
        self.height = h_height

    @property
    def y(self):
        return self.xy[1]

    @property
    def x(self):
        return self.xy[0]

    def triggered(self, trigger: list[int, int] | list[int, int, int, int]):
        """triger: either x, y coordinates or box x, y and width, height"""
        if len(trigger) == 2:
            return (self.x - self.width / 2 <= trigger[0] <= self.x + self.width / 2) and \
                (self.y - self.height / 2 <= trigger[1] <= self.y + self.height / 2)

            # If 'trigger' is another box (x, y, w, h) - AABB Collision
        elif len(trigger) == 4:
            ox, oy, ow, oh = trigger
            return (abs(self.x - ox) * 2 <= (self.width + ow)) and \
                (abs(self.y - oy) * 2 <= (self.height + oh))
        return False


class Object:

    def __init__(self, screen, game, x, y, anim = None, script = lambda a: None, hoverbox: TriggerBox = None):
        """
        Base Object
        x, y is central.
        hitbox 
        """
        self.screen: Surface = screen
        self.game = game
        self.hoverable = False
        game.colliders.append(self)
        self.anim = anim
        self.xy = [x, y]
        self.script = script
        self.hoverbox = hoverbox
        self.data = {"anim_frame": 0}

    def display_xy(self, obj_width, obj_height):
        """to regard xy as the center of object"""
        return [self.x-obj_width/2, self.y-obj_height/2]

    @property
    def x(self):
        return self.xy[0]

    @property
    def y(self):
        return self.xy[1]

    def run(self):
        self.script(self)

    def is_hovered(self, cursor):
        if self.hoverbox:
            return self.hoverbox.triggered(cursor)

    def hovered(self, cursor):
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

    def quitted_click(self):
        return

