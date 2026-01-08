import pygame
from ecran import creer_ecran
from joueur import Joueur

pygame.init()

ecran = creer_ecran()
clock = pygame.time.Clock()
running = True

joueur = Joueur()

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    joueur.deplacement()

    x = max(0, min(joueur.rect.x, 1280 - 100))
    y = max(0, min(joueur.rect.y, 720 - 100))

    ecran.fill((0, 0, 0))

    ecran.blit(joueur.image, (joueur.rect.x, joueur.rect.y))

    pygame.display.flip()





pygame.quit()
