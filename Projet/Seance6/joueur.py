import pygame

class Joueur:
    def __init__(player):
        # Image et rectangle
        player.image = pygame.image.load("images/joueur.png").convert_alpha()
        player.image = pygame.transform.scale(player.image, (768, 192))
        player.rect = player.image.get_rect(topleft=(200, 400))  # juste au-dessus d'une plateforme

        # Vitesse
        player.vitesse = 5

        # Gravité et saut
        player.vel_y = 0
        player.gravity = 0.8
        player.jump_force = -15

    def deplacement(player, plateformes):
        touches = pygame.key.get_pressed()
        dx = 0
        if touches[pygame.K_q]:
            dx = -player.vitesse
        if touches[pygame.K_d]:
            dx = player.vitesse

        player.rect.x += dx

        # Collisions horizontales
        for plat in plateformes:
            if player.rect.colliderect(plat):
                if dx > 0:
                    player.rect.right = plat.left
                elif dx < 0:
                    player.rect.left = plat.right

        # Saut uniquement si au sol
        if touches[pygame.K_SPACE] and player.est_au_sol(plateformes):
            player.vel_y = player.jump_force

    def appliquer_gravite(player, plateformes):
        # Appliquer gravité
        player.vel_y += player.gravity
        player.rect.y += player.vel_y

        # Collisions verticales
        for plat in plateformes:
            if player.rect.colliderect(plat):
                if player.vel_y >= 0:  # descente ou immobile
                    player.rect.bottom = plat.top
                    player.vel_y = 0
                elif player.vel_y < 0:  # montée
                    player.rect.top = plat.bottom
                    player.vel_y = 0

    def est_au_sol(player, plateformes):
        # Vérifie si le joueur est posé sur une plateforme
        player.rect.y += 1
        au_sol = any(player.rect.colliderect(p) for p in plateformes)
        player.rect.y -= 1
        return au_sol








    
