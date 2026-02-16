from Object import Object, TriggerBox
from pygame import draw, Surface

from draw import draw_rect


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
        self.hoverbox = TriggerBox(*self.xy, width_t, height_t)

    @property
    def y(self):
        return self.xy[1]

    @property
    def x(self):
        return self.xy[0]

    def clicked(self, cursor):
        self.dragged_pos = (self.x - cursor[0], self.y - cursor[1])
        if self.is_draggable:
            self.dragged = True

    def show(self, cursor):
        if self.dragged:
            self.xy = cursor[0] + self.dragged_pos[0], cursor[1] + self.dragged_pos[1]
        draw_rect(self.surface, self.colour, [*self.xy, self.width, self.height])

    def hovered(self, cursor):
        x, y = self.hoverbox.xy
        wdt, hgt = self.hoverbox.width, self.hoverbox.height
        x_neg = int(x - wdt / 2)
        x_pos = int(x + wdt / 2)
        y_neg = int(y - hgt / 2)
        y_pos = int(y + hgt / 2)
        tst_lines = [
            [[x_neg, int(y + hgt / 2)], [int(x + wdt / 2), int(y + hgt / 2)]],
            [[int(x - wdt / 2), int(y - hgt / 2)], [int(x + wdt / 2), int(y - hgt / 2)]],
            [[x_pos, y_pos], [int(x + wdt / 2), int(y - hgt / 2)]],
            [[x_neg, y_pos], [x_neg, y_neg]]
        ]
        from pygame.draw_py import draw_line
        draw_line(self.screen, [0, 255, 0], *tst_lines[0])
        draw_line(self.screen, [0, 255, 0], *tst_lines[1])
        draw_line(self.screen, [0, 255, 0], *tst_lines[2])
        draw_line(self.screen, [0, 255, 0], *tst_lines[3])


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
                n_tile = Tile(st.surface, st.game, st.x+st.width*w, st.y+st.height*h,
                     st.width, st.height, col, is_draggable = st.is_draggable)
                self.tiles.append(
                    n_tile
                )
                pass

    def __iter__(self):
        for t in self.tiles:
            yield t

    def tile_hovered(self, cursor): # ???
        for t in self.tiles:
            if (t.x - self.width/2 <= cursor[0] <= t.x+t.width/2) & \
                (t.y - self.height/2 <= cursor[1] <= t.y+t.height/2):
                return t


    def clicked(self, cursor):
        return