import json
from math import sqrt
from random import randint, seed, random

from pygame import Surface, draw, Vector2, font

import timer
from InterfaceObject import InterfaceObject
from Object import TriggerBox
from Operator import OperatorObject
from draw_arrow import draw_arrow
from draw import draw_rect
from outliner import generate_outline
from timer import Timer

width_t, height_t = 70, 70

class PlaceTile(InterfaceObject):
    """
    The interface tile to place objects
    """
    def __init__(self, surface, game, x, y, anim: list[Surface], agent_pic: Surface, operator_data,
                 script = lambda a: None, hoverbox=None, colour = None, until_deployment=None,
                 ):
        if not hoverbox:
            hoverbox = TriggerBox(x, y, width_t, height_t)
        super().__init__(surface, game, x, y,
                         anim, script, hoverbox, hoverable = True, draggable = True)
        self.width, self.height = width_t, height_t
        self.outline_anim = generate_outline(self.anim, 180, 180)
        self.agent_pic = agent_pic
        self.orig_xy = self.xy
        self.colour = colour
        self.collided = None
        self.until_deployment = until_deployment
        self.operator_data = operator_data
        self.test = []

    def _process_anim(self):
        sprite = self.anim[self.data["anim_frame"]]
        timer = self.data.get("anim_timer")
        if not timer:
            timer = Timer(0.01)
            self.data["anim_timer"] = timer
        if timer.is_late():
            self.data["anim_frame"] += 1
            self.data["anim_timer"] = Timer(0.01)
        if self.data["anim_frame"] >= len(self.anim):
            self.data["anim_frame"] = 0
        return sprite

    def show_dragged(self, outline=False):
        sprite: Surface = self._process_anim()
        disp_xy = self.display_xy(sprite.get_width(), sprite.get_height()*1.5)
        self.screen.blit(sprite, disp_xy)
        if outline:
            game_over_screen_fade = Surface((self.screen.get_width(), self.screen.get_height()))
            game_over_screen_fade.fill((0, 0, 0))
            game_over_screen_fade.set_alpha(200)
            self.screen.blit(game_over_screen_fade, (0, 0))
            outline = self.outline_anim[self.data["anim_frame"]]
            self.screen.blit(outline, disp_xy)
            sprite.set_alpha(255)
        return

    def show(self, cursor):
        if self.collided and not self.until_deployment:
            self.placing(cursor)
            return
        elif self.dragged and not self.until_deployment:
            self.xy = cursor[0] + self.dragged_pos[0], cursor[1] + self.dragged_pos[1]
            collided = self.collided = self.game.game_tiles_collide(cursor)
            if self.collided:
                self.xy = (collided.xy[0], collided.xy[1])
                self.show_dragged(True)
                self.dragged = False
                return
            self.show_dragged()
            return
        self.xy = self.orig_xy
        self.hoverbox.xy = self.xy
        draw_rect(self.screen, self.colour, [*self.xy, self.width, self.height])
        self.screen.blit(self.agent_pic, self.xy)

    def transform_into_operator(self, direction, tile):
        OperatorObject.initialize_agent(self.operator_data, direction, self.game, self.screen, tile.x, tile.y)
        return

    def show_dmg_area(self):
        dmg_area = self.operator_data["dmg_area"]


    def placing(self, cursor):
        self.show_dragged(True)
        self.hoverbox.xy = self.xy
        x, y = self.xy
        # x, y = self.display_xy(self.width, self.height)

        draw.line(self.screen, (255, 255, 255), (x, y - 160), (x + 160, y), 5)
        draw.line(self.screen, (255, 255, 0), (x - 160, y), (x, y - 160), 5)
        draw.line(self.screen, (255, 255, 255), (x, y + 160), (x - 160, y), 5)
        draw.line(self.screen, (255, 255, 0), (x + 160, y), (x, y + 160), 5)
        draw_rect(self.screen, (0,0,0), [x, y, 10, 10])
        draw_rect(self.screen, self.colour, [x/2, y/2, 10, 10])
        if self.dragged:
            print("IN DRAGGED")
            area = self.operator_data["dmg_area"]

            draw.line(self.screen, (0,0,255), cursor, (x, y), 100)


            """# rendering a text written in
            # this font
            w = randint(0, self.screen.get_width())
            h = randint(0, self.screen.get_height())
            rng = (int(0.001*(1.1**len(self.test))),int(0.01*(1.1**len(self.test))))
            print(rng)
            if rng[0] == rng[1]:
                rng = rng[0]
            elif rng[0] > rng[1]:
                rng =randint(rng[1], rng[0])
            else:
                rng = randint(*rng)
            if rng > 255:
                tr,tg, tb = 255, 0, 0
                r, g, b = 0, 0, 0
            else:
                r = randint(0, 255-rng)
                #seed(r)
                g = randint(0, 255-rng)
                #seed(r*g)
                b = randint(0, 255-rng)
                tr, tg, tb = r, g, b
            exy = cursor
            smallfont = font.SysFont('Corbel', 35)

            if not len(self.test):
                self.test.append(Timer(-1))
            if self.test[0].is_late():
                self.test.pop(0)
                self.test.insert(0, Timer(4/(len(self.test)+1)))
                self.test.append([[w,h], (r,g,b),randint(int(1*(1+len(self.test)*0.01)),int(30*(1+len(self.test)*0.01))), (tr, tg, tb)])
            # rendering a text written in
            # this font
            exy = cursor
            for letrs in self.test[1:]:
                text = smallfont.render("KYS", True, letrs[3])
                if randint(0,100) >99:
                    exy = cursor
                exy_chance = sqrt((exy[0]**2 - letrs[0][0]**2 + exy[1]**2 - letrs[0][1]**2)**2)

                lxy = letrs[0]
                if exy_chance < randint(0, int(exy_chance*1.2)):
                   lxy = [lxy[0]+(lxy[0] - exy[0])/10,
                          lxy[1]+(lxy[1] - exy[1])/10]
                draw.line(self.screen, (letrs[1]), lxy, exy, letrs[2])
                self.screen.blit(text, (letrs[0]))
                exy = letrs[0]

            """
        return

    def on_place(self):
        self.collided.placed(self)

        return

    @staticmethod
    def get_operator_data(game, key):
        return game.operators_data[key]

