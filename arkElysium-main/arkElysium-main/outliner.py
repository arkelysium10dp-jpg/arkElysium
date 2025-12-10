from pygame import mask, Surface, pixelarray


def generate_masks(pic_list, a, b):
    mask_list = []
    for pic in pic_list:
        surf = Surface((a, b))
        surf.set_colorkey((0, 0, 0))
        mask_ = mask.from_surface(pic)
        pic_mask = mask_.to_surface()

        var = pixelarray.PixelArray(pic_mask)
        var.replace((255, 255, 255), (255, 0, 0))
        del var

        surf.blit(pic_mask, (0, 0))
        pic.set_alpha(100)
        surf.blit(pic, (0, 0))

        mask_list.append(surf)
        pic.set_alpha(255)
    return mask_list

def generate_outline(pic_list, a, b):
    outlined_list = []
    for pic in pic_list:
        surf = Surface((a, b))
        surf.set_colorkey((0, 0, 0))
        mask_ = mask.from_surface(pic)
        pic_mask = mask_.to_surface()
        pic_mask.set_colorkey((0, 0, 0))
        surf.blit(pic_mask, (0, 1))
        surf.blit(pic_mask, (0, -1))
        surf.blit(pic_mask, (1, 0))
        surf.blit(pic_mask, (-1, 0))
        surf.blit(pic, (0, 0))
        outlined_list.append(surf)
    return outlined_list