import pygame

from Game import Game
from Object import Object, Hitbox
from Objects.elysium_button import ElysiumButton
from Tile import Tile, TileMap

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

def small_ai(obj: Object):
    if not obj.data.get("ai_tick"):
        obj.data["ai_tick"] = Timer(1, 0)
    if obj.data["ai_tick"].is_late():
        obj.data["ai_tick"] = Timer(1, 0)
        obj.xy[0] += 10

img = pygame.image.load("sprites/K8qTBCA.png").convert_alpha()
img = SpriteSheet(img)
img = img.get_image(0,218, 224, 0.3,
              (0,0,0))

game = Game()
tile = Tile(screen, game, width / 4, height / 4, 70, 70, (255, 255, 255), is_draggable=False)
tile_map = TileMap(tile, 2, 3, (color_dark, color_light))
elysssium = pygame.image.load("sprites/elysium_spreadsheet.jpg").convert_alpha()
elysssium = SpriteSheet(elysssium)
elysssium_anim = []
for i in range(0, 42):
    elysssium_anim.append(elysssium.get_image(i,206, 382, 0.40,(0,0,0)))


obj0 = Object(screen, game, *tile_map.tiles[0].xy, [img], small_ai)
ELYSIUM = Object(screen, game, tile_map.tiles[1].x, tile_map.tiles[1].y , elysssium_anim)
objs = [obj0, ELYSIUM]

elysium_hitbox = Hitbox(70, height-72, 70, 70)
elysium_button = ElysiumButton(screen, game, 70, height-72,  70, 70, (215, 215, 215), True, )

game.interface.append(elysium_button)
interface = [elysium_button]

# TODO: units

while True:
    mouse = pygame.mouse.get_pos()

    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            pygame.quit()
            break

        # checks if a mouse is clicked
        if ev.type == pygame.MOUSEBUTTONDOWN:
            print("CLICKED")
            for i in tile_map:
                if i.is_hovered(mouse):
                    i.clicked(mouse)
            for i in interface:
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
            for i in interface:
                i.dragged = False


    # fills the screen with a color
    screen.fill((60, 25, 60))
    print(mouse)

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
        o.show(mouse)

    for t in interface:
        t.show(mouse)

    # updates the frames of the game
    pygame.display.update()