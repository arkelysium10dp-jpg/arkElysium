from InterfaceObject import InterfaceObject
from Object import TriggerBox
from draw import draw_rect


class Button(InterfaceObject):
    def __init__(self, surface, game, x, y, width, height, colour="gray", hover_colour="black"):
        # TODO: FIX COLOURS
        hoverbox = TriggerBox(x, y, width, height)
        super().__init__(surface, game, x, y, hoverbox=hoverbox)
        self.colour = colour
        self.hover_colour = hover_colour
        self.hover = False
        self.width = width
        self.height = height

    def clicked(self, cursor):
        return

    def show(self, cursor):
        draw_rect(self.screen, self.colour, [*self.xy, self.width, self.height])
        return

    def hovered(self, cursor):
        draw_rect(self.screen, self.hover_colour, [*self.xy, self.width, self.height])
        return