import pygame
from joueur import Joueur

def get_image(sheet, width, height):
    image = pygame.Surface((width, height)).convert.alpha()
    image.blit(sheet, (0,0))

    return image

frame_0 = get_image(player.image, 32, 32)
frame_1 = get_image(player.image, 64, 32)
frame_2 = get_image(player.image, 96, 32)
frame_3 = get_image(player.image, 128, 32)
frame_4 = get_image(player.image, 160, 32)
frame_5 = get_image(player.image, 192, 32)
frame_6 = get_image(player.image, 224, 32)