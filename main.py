import pygame
import sys
from spritesheet import SpriteSheet
from timer import Timer

pygame.display.set_caption("ArkElysium")

# initializing the constructor
pygame.init()

# screen resolution
res = (720, 720)

# opens up a window
screen = pygame.display.set_mode(res)

# white color
color = (255, 255, 255)

# light shade of the button
color_light = (170, 170, 170)

# dark shade of the button
color_dark = (100, 100, 100)

# stores the width of the
# screen into a variable
width = screen.get_width()

# stores the height of the
# screen into a variable
height = screen.get_height()

# defining a font
smallfont = pygame.font.SysFont('Corbel', 35)

# rendering a text written in
# this font
text = smallfont.render('quit', True, color)


class Tile:
    def __init__(self, surface, x, y, width, height, colour, is_draggable,):
        self.surface = surface
        self.xy = (x, y)
        self.width = width
        self.height = height
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
        self.dragged_pos = (self.x-cursor[0], self.y - cursor[1])
        if self.is_draggable:
            self.dragged = True

    def show(self, cursor):
        if self.dragged:
            self.xy = cursor[0] + self.dragged_pos[0], cursor[1] + self.dragged_pos[1]
        pygame.draw.rect(self.surface, self.colour, [*self.xy, self.width, self.height])

class TileMap:
    def __init__(self, start_tile: Tile, t_width, t_height, colors_gradient):
        self._original_tile = start_tile
        self.width = t_width
        self.height = t_height
        self.colors_gradient = colors_gradient
        self.tiles = []
        st = self._original_tile
        for h in range(0, self.height):
            for w in range(0, self.width):
                col_ind = h+h*self.width+w-int((h+h*self.width+w)/len(colors_gradient))*len(colors_gradient)
                col = self.colors_gradient[
                    col_ind
                ]
                self.tiles.append(
                Tile(st.surface, st.x+st.width*w, st.y+st.height*h,
                     st.width, st.height, col, is_draggable = st.is_draggable)
                )
                pass

    def __iter__(self):
        for t in self.tiles:
            yield t

    def tile_hovered(self, cursor): # ???
        orig_tile = self._original_tile
        if not orig_tile.is_draggable:
            if orig_tile.x >= cursor[0] >= orig_tile.x*width*orig_tile.width & \
                    orig_tile.y >= cursor[1] >= orig_tile.y*height*orig_tile.height:
                tile_index = cursor[0]/width/ self.width * cursor[1]/height/self.height
                print(tile_index)
            return
        return

    def clicked(self, cursor):
        return

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
        return self.x >= trigger_xy[0] >= self.x * width * self.width & \
        self.y >= trigger_xy[1] >= self.y * height * self.height



class Object:
    def __init__(self,surface, x, y,  sprite, script = lambda a: None):
        self.screen = surface
        self.sprite = sprite
        self.xy = [x, y]
        self.script = script
        self.data = {}

    def run(self):
        self.script(self)

    def show(self):
        self.screen.blit(self.sprite, self.xy)


def small_ai(obj: Object):
    if not obj.data.get("ai_tick"):
        obj.data["ai_tick"] = Timer(1, 0)
    if obj.data["ai_tick"].is_late():
        obj.data["ai_tick"] = Timer(1, 0)
        obj.xy[0] += 10


img = pygame.image.load("sprites\\k8qTBCA.png").convert_alpha()
img = SpriteSheet(img)
img = img.get_image(0,218, 224, 0.3,
              (0,0,0))


tile = Tile(screen, width / 4, height / 4, 70, 70, (255, 255, 255), is_draggable=False)
tile_map = TileMap(tile, 2, 3, (color_dark, color_light))
elysssium = pygame.image.load("sprites\\videoframe_2417.png").convert_alpha()
elysssium = SpriteSheet(elysssium)
elysssium = elysssium.get_image(0,1024, 575, 0.40,
              (0,0,0))


obj0 = Object(screen, *tile_map.tiles[0].xy, img, small_ai)
ELYSIUM = Object(screen, tile_map.tiles[1].x-10, tile_map.tiles[1].y , elysssium)
objs = [obj0, ELYSIUM]
while True:
    mouse = pygame.mouse.get_pos()

    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            pygame.quit()

        # checks if a mouse is clicked
        if ev.type == pygame.MOUSEBUTTONDOWN:
            print("CLICKED")
            for i in tile_map:
                if i.is_hovered(mouse):
                    i.clicked(mouse)

            # if the mouse is clicked on the
            # button the game is terminated
            if width / 2 <= mouse[0] <= width / 2 + 140 and height / 2 <= mouse[1] <= height / 2 + 40:
                pygame.quit()
        if ev.type == pygame.MOUSEBUTTONUP:
            print("Quitted CLICK")
            for i in tile_map:
                i.dragged = False


    # fills the screen with a color
    screen.fill((60, 25, 60))

    # stores the (x,y) coordinates into
    # the variable as a tuple

    # if mouse is hovered on a button it
    # changes to lighter shade
    if width / 2 <= mouse[0] <= width / 2 + 140 and height / 2 <= mouse[1] <= height / 2 + 40:
        pygame.draw.rect(screen, color_light, [width / 2, height / 2, 140, 40])

    else:
        pygame.draw.rect(screen, color_dark, [width / 2, height / 2, 140, 40])

    # superimposing the text onto our button
    screen.blit(text, (width / 2 + 50, height / 2))

    for i in tile_map:
        i.show(mouse)

    for o in objs:
        o.run()
        o.show()

    # updates the frames of the game
    pygame.display.update()