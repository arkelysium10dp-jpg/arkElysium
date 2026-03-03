from pygame.draw import rect


def draw_rect(screen, color, rectangle):
    """Draws rectangular in center"""
    # TODO: FIX COLOURS
    st_x, st_y, width, height = rectangle
    st_x -= width/2
    st_y -= height/2
    rect(screen, color, [st_x, st_y, width, height])
