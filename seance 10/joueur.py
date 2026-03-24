import pygame, sys
from sfx import sauter

pygame.mixer.init(44100)
sound = sauter
sound.set_volume(0.4)
class Joueur(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()

        self.idle_image = pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur000.png").convert_alpha(), (30,30))
        self.image = self.idle_image
        self.rect = pygame.Rect(0, 0, 50, 100)
        self.rect.center = (100, 6299)
        self.draw_offset_x = 8
        self.draw_offset_y = 15
        self.rect = pygame.Rect(1900, 3000, 50, 100) # Enlever le commentaire pour le mettre en haut
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
        self.vx = 0  # vitesse horizontale
        self.friction = 0.6  # entre 0 et 1, plus petit = ralentit plus vite
        self.vitesse = 5
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_force = -15
        self.facing_left = False
        self.peut_bouger = True
        #-------double saut----------------
        #self.double_saut = False
        self.double_saut = True
        self.nb_sauts = 0
        self.dernier_saut = 0
        self.delai_double_saut = 200 # en ms
        self.nb_sauts = 0
        # Effet double saut
        self.double_jump_effects = []  # liste des effets de double saut actifs
    def update(self):
        if self.vel_y !=0:
            return
        if self.is_animating and self.peut_bouger:
            self.current_sprite += 0.2
            if self.current_sprite > 7:
                self.current_sprite = 1  # on évite la frame 0
            img = self.sprites[int(self.current_sprite)]
        else:
            img = self.sprites[0]  # frame immobile

    # appliquer la direction MEME A L'ARRET
        if self.facing_left and self.peut_bouger:
            self.image = pygame.transform.flip(img, True, False)
        else:
            self.image = img

    def deplacement(self, plateformes):
        if not self.peut_bouger:
            return

        touches = pygame.key.get_pressed()
        # accélération
        if touches[pygame.K_q] or touches[pygame.K_LEFT]:
            self.vx = -self.vitesse
            self.facing_left = True
            self.is_animating = True
        elif touches[pygame.K_d] or touches[pygame.K_RIGHT]:
            self.vx = self.vitesse
            self.facing_left = False
            self.is_animating = True
        else:
            self.is_animating = False
            # applique friction pour ralentir progressivement
            self.vx *= self.friction
            # si très proche de 0, stoppe complètement
            if abs(self.vx) < 0.1:
                self.vx = 0

        # déplacement horizontal
        self.rect.x += self.vx

        # collisions horizontales
        for plat in plateformes:
            if self.rect.colliderect(plat):
                if self.vx > 0:
                    self.rect.right = plat.left
                    self.vx = 0
                elif self.vx < 0:
                    self.rect.left = plat.right
                    self.vx = 0

        # Collisions horizontales
        for plat in plateformes:
            if self.rect.colliderect(plat):
                if self.vx > 0:
                    self.rect.right = plat.left
                elif self.vx < 0:
                    self.rect.left = plat.right

        temps_actuel = pygame.time.get_ticks()

        # saut normal
        if touches[pygame.K_SPACE] and self.est_au_sol(plateformes):
            self.vel_y = self.jump_force
            self.nb_sauts = 1
            self.dernier_saut = temps_actuel
            sound.play()

        # double saut
        elif (
            touches[pygame.K_SPACE]
            and not self.est_au_sol(plateformes)
            and self.double_saut
            and self.nb_sauts == 1
            and temps_actuel - self.dernier_saut >= self.delai_double_saut
        ):
            self.vel_y = self.jump_force
            self.nb_sauts = 2
            self.dernier_saut = temps_actuel
            sound.play()
            # Ajouter effet visuel double saut
            self.double_jump_effects.append({
                'x': self.rect.centerx,
                'y': self.rect.y + 150,  # sous le sprite visuel (150px de hauteur)
                'alpha': 255,
                'width': 120,
                'height': 7# trait plus épais (hauteur)
            })


            


    def est_au_sol(self, plateformes):
        # Vérifie si le joueur est posé sur une plateforme
        self.rect.y += 1
        au_sol = any(self.rect.colliderect(p) for p in plateformes)
        self.rect.y -= 1
        return au_sol


    def appliquer_gravite(self, plateformes, murs=None):
        # Appliquer gravité
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # Collisions verticales
        for plat in plateformes:
            if self.rect.colliderect(plat):
                if self.vel_y >= 0:
                    self.rect.bottom = plat.top
                    self.vel_y = 0
                    self.nb_sauts = 0
                elif self.vel_y < 0:  # montée
                    self.rect.top = plat.bottom
                    self.vel_y = 0

        # murs (plateformes hautes)
        if murs:
            for mur in murs:
                if self.rect.colliderect(mur):
                    if self.rect.centerx < mur.centerx:
                        self.rect.right = mur.left
                    else:
                        self.rect.left = mur.right
        if self.est_au_sol(plateformes) == False:
            if self.facing_left == True:
                self.image = pygame.transform.flip(self.sprites[8], True, False)  # image de saut si en l'air
            else:
                self.image = self.sprites[8]  # image de saut si en l'air

    def update_double_jump_effects(self):
        """Met à jour les effets de double saut (fondu)"""
        for effect in self.double_jump_effects[:]:
            effect['alpha'] -= 15  # diminuer l'opacité
            if effect['alpha'] <= 0:
                self.double_jump_effects.remove(effect)
