from pygame import draw

from Object import Object

class InterfaceObject(Object):
    def __init__(self, surface, game, x, y,  anim = None, script = lambda a: None, hitbox = None, hoverable: bool = False, draggable: bool = False):
        super().__init__(surface, game, x, y, anim, script, hitbox)
        self.hoverable = hoverable
        self.is_draggable = draggable
        self.dragged = False
        self.dragged_pos = self.xy

    def is_hovered(self, cursor):
        return self.hitbox.triggered(cursor)

    def clicked(self, cursor):
        self.dragged_pos = (self.x - cursor[0], self.y - cursor[1])
        if self.is_draggable:
            self.dragged = True


