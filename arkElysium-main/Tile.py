from Object import Object
from pygame import draw, Surface


class Tile(Object):
    def __init__(self, surface: Surface, game, x, y, width_t, height_t, colour, is_draggable):
        super().__init__(surface, game, x, y)
        self.surface = surface
        self.xy = (x, y)
        self.width = width_t
        self.height = height_t
        self.initial_xy = self.xy
        self.colour = colour
        self.is_draggable = is_draggable
        self.dragged = False
        self.dragged_pos = self.xy

    @property
    def y(self):
        return self.xy[1]

    @property
    def x(self):
        return self.xy[0]

    def is_hovered(self, cursor):
        if self.x <= cursor[0] <= self.x + 140 and self.y <= cursor[1] <= self.y + 40:
            return True

    def clicked(self, cursor):
        self.dragged_pos = (self.x - cursor[0], self.y - cursor[1])
        if self.is_draggable:
            self.dragged = True

    def show(self, cursor):
        if self.dragged:
            self.xy = cursor[0] + self.dragged_pos[0], cursor[1] + self.dragged_pos[1]
        draw.rect(self.surface, self.colour, [*self.xy, self.width, self.height])


class GameTile(Tile):
    def __init__(self, surface: Surface, game, x, y, width_t, height_t, colour, is_draggable, is_placeable: bool):
        super().__init__(surface, game, x, y, width_t, height_t, colour, is_draggable)
        self.is_placeable = is_placeable
        self.placed_obj: Object | None = None

    def placed(self, obj):
        center_xy = self.x * self.width /2, self.y * self.height/2
        obj.xy = center_xy
        self.placed_obj = obj


class TileMap:
    def __init__(self, start_tile: Tile, t_width, t_height, colors_gradient):
        self._original_tile = start_tile
        self.width = t_width
        self.height = t_height
        self.colors_gradient = colors_gradient
        self.tiles = []
        self.surface = self._original_tile.surface
        st = self._original_tile
        for h in range(0, self.height):
            for w in range(0, self.width):
                col_ind = h+h*self.width+w-int((h+h*self.width+w)/len(colors_gradient))*len(colors_gradient)
                col = self.colors_gradient[
                    col_ind
                ]
                self.tiles.append(
                Tile(st.surface, st.game, st.x+st.width*w, st.y+st.height*h,
                     st.width, st.height, col, is_draggable = st.is_draggable)
                )
                pass

    def __iter__(self):
        for t in self.tiles:
            yield t

    def tile_hovered(self, cursor): # ???
        orig_tile = self._original_tile
        if not orig_tile.is_draggable:
            height = self.surface.get_height()
            width = self.surface.get_width()
            if orig_tile.x >= cursor[0] >= orig_tile.x*width*orig_tile.width & \
                    orig_tile.y >= cursor[1] >= orig_tile.y*height*orig_tile.height:
                tile_index = cursor[0]/self.surface.get_width()/ self.width * cursor[1]/height/self.height
            return
        return

    def clicked(self, cursor):
        return