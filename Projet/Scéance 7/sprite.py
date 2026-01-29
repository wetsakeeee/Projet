import pygame
from joueur import Joueur

def get_image(sheet, width, height, scale):
    image = pygame.Surface((width, height)).convert.alpha()
    image.blit(sheet, (0,0))
    image = pygame.transform.scale(img, (width * scale, height * scale))

    return image

frame_0 = get_image(player.image, 0, 32, 32, 1)
frame_1 = get_image(player.image, 1, 32, 32, 1)
frame_2 = get_image(player.image, 2, 32, 32, 1)
frame_3 = get_image(player.image, 3, 32, 32, 1)
frame_4 = get_image(player.image, 4, 32, 32, 1)
frame_5 = get_image(player.image, 5, 32, 32, 1)
frame_6 = get_image(player.image, 6, 224, 32, 1)