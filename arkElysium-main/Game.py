from InterfaceObject import InterfaceObject
from Object import Object
from Tile import GameTile


class Game():
    def __init__(self):
        self.colliders: list[Object] = []
        self.game_tiles_colliders: list[GameTile] = []
        self.interface: list[InterfaceObject] = []

    def collides_with(self, obj):
        for i in self.colliders:
            if i.hitbox:
                if i.hitbox.triggered(obj.xy):
                    return i

    def game_tiles_collide(self, obj):
        for i in self.game_tiles_colliders:
            if i.hitbox.triggered(obj.xy):
                return i
