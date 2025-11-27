from InterfaceObject import InterfaceObject
from Object import Object
from Tile import GameTile, TileMap


class Game:
    def __init__(self):
        self.colliders: list[Object] = []
        self.game_tiles_colliders: list[GameTile] = []
        self.tile_maps: list[TileMap] = []
        self.interface: list[InterfaceObject] = []
        self._events = []
        self.hoverables: list[Object] = []
        self.objs = []

    def tick(self, mouse):
        for tm in self.tile_maps:
            for i in tm:
                i.show(mouse)

        for o in self.objs:
            o.run()
            o.show(mouse)

        for t in self.interface:
            t.show(mouse)
        return

    def handle_events(self):
        for i in self._events:
            i()

    def interface_clicked(self, xy):
        for i in self.interface:
            if i.hitbox:
                if i.hitbox.triggered(xy):
                    return i

    def collides_with(self, xy):
        for i in self.colliders:
            if i.hitbox:
                if i.hitbox.triggered(xy):
                    return i

    def game_tiles_collide(self, xy) -> GameTile:
        for i in self.game_tiles_colliders:
            if i.hitbox:
                if i.hitbox.triggered(xy):
                    return i
        for tm in self.tile_maps:
            for i in tm:
                tl = tm.tile_hovered(xy)
                if tl:
                    if i.hitbox.triggered(xy):
                        return i
