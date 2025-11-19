from InterfaceObject import InterfaceObject
from Object import Object
from Tile import GameTile, TileMap
from outliner import Outliner


class Game:
    def __init__(self):
        self.colliders: list[Object] = []
        self.game_tiles_colliders: list[GameTile] = []
        self.tile_maps: list[TileMap] = []
        self.interface: list[InterfaceObject] = []
        self.Outliner = Outliner()
        self._events = []


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

    def game_tiles_collide(self, xy):
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
