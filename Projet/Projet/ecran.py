import pygame
# par la même occasion cela importe pygame.locals dans l'espace de nom de Pygame

pygame.init()

ecran = pygame.display.set_mode((300, 200))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            running = False

pygame.quit()