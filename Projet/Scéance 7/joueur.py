import pygame, sys  

pygame.mixer.init()
sound = pygame.mixer.Sound("jump.mp3")

class Joueur(pygame.sprite.Sprite):
    def __init__(player):
        super().__init__()

        player.idle_image = pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur000.png").convert_alpha(), (150,150))
        player.image = player.idle_image
        player.rect = pygame.Rect(0, 6299, 32, 32)

        player.sprites = []
        player.sprites.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur000.png").convert_alpha(),(150,150)))
        player.sprites.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur001.png").convert_alpha(),(150,150)))
        player.sprites.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur002.png").convert_alpha(),(150,150)))
        player.sprites.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur003.png").convert_alpha(),(150,150)))
        player.sprites.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur004.png").convert_alpha(),(150,150)))
        player.sprites.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur005.png").convert_alpha(),(150,150)))
        player.sprites.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur006.png").convert_alpha(),(150,150)))
        player.sprites.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur007.png").convert_alpha(),(150,150)))
        player.sprites.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur012.png").convert_alpha(),(150,150)))



        player.current_sprite = 0
        player.sprite_offset = ((150 - 32)//2, (150 - 32)//2)
        
        # Mouvement
        player.vitesse = 4
        player.vel_y = 0
        player.gravity = 0.8
        player.jump_force = -15

        player.facing_left = False


    def update(player):
        if player.is_animating:
            player.current_sprite += 0.08
            if player.current_sprite > 7:
                player.current_sprite = 1  # on évite la frame 0
            img = player.sprites[int(player.current_sprite)]
        else:
            img = player.sprites[0]  # frame immobile

    # appliquer la direction MEME A L'ARRET
        if player.facing_left:
            player.image = pygame.transform.flip(img, True, False)
        else:
            player.image = img

    






    











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
            player.image = player.sprites[8]  # image de saut
            player.vel_y = player.jump_force
            sound.play()
            sound.set_volume(0.4)


    def est_au_sol(player, plateformes):
        # Vérifie si le joueur est posé sur une plateforme
        player.rect.y += 1
        au_sol = any(player.rect.colliderect(p) for p in plateformes)
        player.rect.y -= 1
        return au_sol


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
        if player.est_au_sol(plateformes) == False:
            if player.facing_left == True:
                player.image = pygame.transform.flip(player.sprites[8]  # image de saut si en l'air
, True, False)
            else:
                player.image = player.sprites[8]  # image de saut si en l'air



    
    
    