import pygame

class Joueur:
    def __init__(player):

        player.x = 1280 // 2
        player.y = 720 // 2
        player.vitesse = 5

        player.image = pygame.image.load("images/galileo.png").convert_alpha()
        player.rect = player.image.get_rect()
        player.image = pygame.transform.scale(player.image, (200, 200))  # réduction



    def deplacement(player):
        touches = pygame.key.get_pressed()

        if touches[pygame.K_q]:
            player.rect.x -= player.vitesse
        if touches[pygame.K_d]:
            player.rect.x += player.vitesse
        if touches[pygame.K_z]:
            player.rect.y -= player.vitesse
        if touches[pygame.K_s]:
            player.rect.y += player.vitesse

    def dessiner(player, ecran):
        ecran.blit(player.image, player.rect)

