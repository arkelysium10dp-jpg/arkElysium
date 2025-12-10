
from pygame import Surface, draw, Vector2

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
        disp_xy = self.display_xy(sprite.get_width(), sprite.get_height())
        self.screen.blit(sprite, disp_xy)
        if outline:
            game_over_screen_fade = Surface((self.screen.get_width(), self.screen.get_height()))
            game_over_screen_fade.fill((0, 0, 0))
            game_over_screen_fade.set_alpha(160)
            self.screen.blit(game_over_screen_fade, (0, 0))
            outline = self.outline_anim[self.data["anim_frame"]]
            self.screen.blit(outline, disp_xy)
            sprite.set_alpha(255)
        return

    def show(self, cursor):
        # FIXME: assigns to diff tile?
        if self.dragged and not self.until_deployment:
            self.xy = cursor[0] + self.dragged_pos[0], cursor[1] + self.dragged_pos[1]
            collided = self.collided = self.game.game_tiles_collide(cursor)
            if self.collided:
                self.xy = (collided.xy[0] - 10, collided.xy[1] - 90)
                self.show_dragged(True)
                return
            self.show_dragged()
            return
        elif self.collided and not self.until_deployment:
            self.placing(cursor)
            return
        self.xy = self.orig_xy
        self.hoverbox.xy = self.xy
        draw_rect(self.screen, self.colour, [*self.xy, self.width, self.height])
        self.screen.blit(self.agent_pic, self.xy)

    def transform_into_operator(self, direction, tile):
        OperatorObject.initialize_agent(self.operator_data, direction, self.game, self.screen, tile.x, tile.y)
        return

    def placing(self, cursor):
        self.show_dragged(True)
        self.hoverbox.xy = self.xy
        x, y = self.display_xy(self.width, self.height)

        draw.line(self.screen, (255, 255, 255), (x, y - 160), (x + 160, y), 5)
        draw.line(self.screen, (255, 255, 0), (x - 160, y), (x, y - 160), 5)
        draw.line(self.screen, (255, 255, 255), (x, y + 160), (x - 160, y), 5)
        draw.line(self.screen, (255, 255, 0), (x + 160, y), (x, y + 160), 5)
        draw_rect(self.screen, (0,0,0), [x, y, 10, 10])
        draw_rect(self.screen, self.colour, [x/2, y/2, 10, 10])
        if self.dragged:
            print("IN DRAGGED")
            draw.line(self.screen, (0, 255, 255), cursor, (x, y), 100)
        return

    def on_place(self):
        self.collided.placed(self)

        return

