import pygame, sys
from sfx import sauter

pygame.mixer.init()
sound = sauter

class Joueur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.idle_image = pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur000.png").convert_alpha(), (30,30))
        self.image = self.idle_image
        self.rect = pygame.Rect(0, 6299, 32, 32)

        self.sprites = []
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur000.png").convert_alpha(),(150,150)))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur001.png").convert_alpha(),(150,150)))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur002.png").convert_alpha(),(150,150)))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur003.png").convert_alpha(),(150,150)))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur004.png").convert_alpha(),(150,150)))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur005.png").convert_alpha(),(150,150)))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur006.png").convert_alpha(),(150,150)))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur007.png").convert_alpha(),(150,150)))
        self.sprites.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur012.png").convert_alpha(),(150,150)))



        self.current_sprite = 0
        self.sprite_offset = ((150 - 32)//2, (150 - 32)//2)
        
        # Mouvement
        self.vitesse = 4
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_force = -15

        self.facing_left = False


    def update(self):
        if self.is_animating:
            self.current_sprite += 0.08
            if self.current_sprite > 7:
                self.current_sprite = 1  # on évite la frame 0
            img = self.sprites[int(self.current_sprite)]
        else:
            img = self.sprites[0]  # frame immobile

    # appliquer la direction MEME A L'ARRET
        if self.facing_left:
            self.image = pygame.transform.flip(img, True, False)
        else:
            self.image = img

    






    











    def deplacement(self, plateformes):
        touches = pygame.key.get_pressed()
        dx = 0
        if touches[pygame.K_q]:
            dx = -self.vitesse
        if touches[pygame.K_d]:
            dx = self.vitesse

        self.rect.x += dx

        # Collisions horizontales
        for plat in plateformes:
            if self.rect.colliderect(plat):
                if dx > 0:
                    self.rect.right = plat.left
                elif dx < 0:
                    self.rect.left = plat.right

        # Saut uniquement si au sol
        if touches[pygame.K_SPACE] and self.est_au_sol(plateformes):
            self.image = self.sprites[8]  # image de saut
            self.vel_y = self.jump_force
            sound.play()
            sound.set_volume(0.4)


    def est_au_sol(self, plateformes):
        # Vérifie si le joueur est posé sur une plateforme
        self.rect.y += 1
        au_sol = any(self.rect.colliderect(p) for p in plateformes)
        self.rect.y -= 1
        return au_sol


    def appliquer_gravite(self, plateformes):
        # Appliquer gravité
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # Collisions verticales
        for plat in plateformes:
            if self.rect.colliderect(plat):
                if self.vel_y >= 0:  # descente ou immobile
                    self.rect.bottom = plat.top
                    self.vel_y = 0
                elif self.vel_y < 0:  # montée
                    self.rect.top = plat.bottom
                    self.vel_y = 0
        if self.est_au_sol(plateformes) == False:
            if self.facing_left == True:
                self.image = pygame.transform.flip(self.sprites[8]  # image de saut si en l'air
, True, False)
            else:
                self.image = self.sprites[8]  # image de saut si en l'air



    
    
    