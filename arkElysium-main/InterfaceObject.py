from Object import Object

class InterfaceObject(Object):
    def __init__(self, surface, x, y,  anim = None, script = lambda a: None, hitbox = None, hoverable: bool = False):
        super().__init__(surface, x, y, anim, script, hitbox)
        self.hoverable = hoverable

    def is_hovered(self, cursor):
        return self.hitbox.triggered(cursor)
