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
        for t in self.game_tiles_colliders:
            t.show(mouse)
        for tm in self.tile_maps:
            for i in tm:
                i.show(mouse)

        for o in self.objs:
            o.run()
            o.show(mouse)

        for t in self.interface:
            t.show(mouse)
        return

    def handle_events(self, cursor):
        for i in self._events:
            i()
        self.hovered(cursor)

    def interface_clicked(self, xy):
        for i in self.interface:
            if i.hoverbox:
                if i.hoverbox.triggered(xy):
                    return i

    def collides_with(self, xy):
        for i in self.colliders:
            if i.hoverbox:
                if i.hoverbox.triggered(xy):
                    return i

    def game_tiles_collide(self, xy) -> GameTile:
        for i in self.game_tiles_colliders:
            if i.hoverbox:
                if i.hoverbox.triggered(xy):
                    return i
        for tm in self.tile_maps:
            hv = tm.tile_hovered(xy)
            if hv:
                if hv.hoverbox.triggered(xy):
                    return hv

    def hovered(self, cursor):
        for i in self.hoverables:
            if i.is_hovered(cursor): i.hovered(cursor)
        return

    def quitted_click(self):
        for tm in self.tile_maps:
            for t in tm:
                t.dragged = False
        for i in self.interface:
            i.dragged = False
        return
