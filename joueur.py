import pygame, sys
from sfx import sfxmarche1, sfxmarche2, sfxmarche3, sauter, tombersfx
import random, settings

pygame.mixer.init(44100)

sauter.set_volume(0.2 if settings.option_3 else 0)

marche_sons = [sfxmarche1, sfxmarche2, sfxmarche3]
for s in marche_sons:
    s.set_volume(1 if settings.option_3 else 0)

tombersfx.set_volume(0)


class Joueur(pygame.sprite.Sprite):
    def __init__(self, x=100, y=6299):
        super().__init__()

        self.idle_image = pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur000.png").convert_alpha(), (30,30))
        self.image = self.idle_image
        self.rect = pygame.Rect(0, 0, 50, 100)
        self.rect.center = (x,y)
        self.draw_offset_x = 8
        self.draw_offset_x_left = -8
        self.draw_offset_y = 15
        # vvvv Enlever le commentaire pour le mettre en haut vvvv
        #self.rect = pygame.Rect(1900, 3000, 50, 100)
        # vvv Enlever le commentaire pour le mettre à côté de Virgilio
        #self.rect = pygame.Rect(700,4090, 50 ,100)
        #vvv Enlever le commentaire pour le mettre à côté de la porte enfer
        #self.rect = pygame.Rect(285, 840, 50, 100)
        #vvv Enlever le commentaire pour le mettre à côté de Caronte
        #self.rect = pygame.Rect(3850, 5380, 50, 100)

        # Frame joueur normal
        self.sprites_normal = []
        self.sprites_normal.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur000.png").convert_alpha(),(150,150)))
        self.sprites_normal.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur001.png").convert_alpha(),(150,150)))
        self.sprites_normal.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur002.png").convert_alpha(),(150,150)))
        self.sprites_normal.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur003.png").convert_alpha(),(150,150)))
        self.sprites_normal.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur004.png").convert_alpha(),(150,150)))
        self.sprites_normal.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur005.png").convert_alpha(),(150,150)))
        self.sprites_normal.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur006.png").convert_alpha(),(150,150)))
        self.sprites_normal.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur007.png").convert_alpha(),(150,150)))
        self.sprites_normal.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur008.png").convert_alpha(),(150,150)))
        self.sprites_normal.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur012.png").convert_alpha(),(150,150)))

        # Frame joueur botte
        self.sprites_botte = []
        self.sprites_botte.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte/joueur000botte.png").convert_alpha(),(150,150)))
        self.sprites_botte.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte/joueur001botte.png").convert_alpha(),(150,150)))
        self.sprites_botte.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte/joueur002botte.png").convert_alpha(),(150,150)))
        self.sprites_botte.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte/joueur003botte.png").convert_alpha(),(150,150)))
        self.sprites_botte.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte/joueur004botte.png").convert_alpha(),(150,150)))
        self.sprites_botte.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte/joueur005botte.png").convert_alpha(),(150,150)))
        self.sprites_botte.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte/joueur006botte.png").convert_alpha(),(150,150)))
        self.sprites_botte.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte/joueur007botte.png").convert_alpha(),(150,150)))
        self.sprites_botte.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte/joueur008botte.png").convert_alpha(),(150,150)))
        self.sprites_botte.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte/joueur012botte.png").convert_alpha(),(150,150)))

        self.current_sprite = 0
        self.is_animating = False

        # Mouvement
        self.vx = 0
        self.friction = 0.6
        self.vitesse = 5
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_force = -15
        self.facing_left = False
        self.peut_bouger = True
        self.au_sol = False

        # Double saut
        self.double_saut =  True
        self.nb_sauts = 0
        self.dernier_saut = 0
        self.double_jump_effects = []

        # Sons de marche
        self.marche_timer = 0
        self.marche_intervalle = 350  # ms entre chaque pas

        # Son de chute
        self.timer_chute    = 0
        self.chute_son_joue = False
        self.en_chute       = False
        self.chute_fadeout  = False

    # ------------------------------------------------------------------
    def get_sprites(self):
        return self.sprites_botte if self.double_saut else self.sprites_normal

    # ------------------------------------------------------------------
    def update(self):
        sprites = self.get_sprites()

        if self.vel_y != 0:
            return

        if self.is_animating and self.peut_bouger:
            self.current_sprite += 0.2
            if self.current_sprite > 7:
                self.current_sprite = 1
            img = sprites[int(self.current_sprite)]
        else:
            img = sprites[0]

        if self.facing_left and self.peut_bouger:
            self.image = pygame.transform.flip(img, True, False)
        else:
            self.image = img

    # ------------------------------------------------------------------
    def deplacement(self, plateformes):
        if not self.peut_bouger:
            return

        touches = pygame.key.get_pressed()

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
            self.current_sprite = 1
            self.vx *= self.friction
            if abs(self.vx) < 0.1:
                self.vx = 0

        # Déplacement horizontal
        self.rect.x += self.vx

        # Collisions horizontales
        for plat in plateformes:
            if self.rect.colliderect(plat):
                if self.vx > 0:
                    self.rect.right = plat.left
                    self.vx = 0
                    self.is_animating = False  # stop animation si mur à droite
                elif self.vx < 0:
                    self.rect.left = plat.right
                    self.vx = 0
                    self.is_animating = False  # stop animation si mur à gauche

        temps_actuel = pygame.time.get_ticks()
        # Sons de marche
        if (touches[pygame.K_q] or touches[pygame.K_LEFT] or
                touches[pygame.K_d] or touches[pygame.K_RIGHT]):
            if self.est_au_sol(plateformes) and self.is_animating:
                if temps_actuel - self.marche_timer >= self.marche_intervalle:
                    random.choice(marche_sons).play()
                    self.marche_timer = temps_actuel

    # ------------------------------------------------------------------
    def est_au_sol(self, plateformes):
        return self.au_sol

    # ------------------------------------------------------------------
    def appliquer_gravite(self, plateformes, murs=None):
        sprites = self.get_sprites()
        self.au_sol = False

        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # Collisions verticales
        for plat in plateformes:
            if self.rect.colliderect(plat):
                if self.vel_y >= 0:
                    self.rect.bottom = plat.top
                    self.vel_y = 0
                    self.nb_sauts = 0
                    self.au_sol = True
                elif self.vel_y < 0:
                    self.rect.top = plat.bottom
                    self.vel_y = 0

        # Murs
        if murs:
            for mur in murs:
                if self.rect.colliderect(mur):
                    if self.rect.centerx < mur.centerx:
                        self.rect.right = mur.left
                    else:
                        self.rect.left = mur.right

        temps_actuel = pygame.time.get_ticks()

        # --- Son de chute ---
        if not self.est_au_sol(plateformes):
            if not self.en_chute:
                self.en_chute = True
                self.timer_chute = temps_actuel
                self.chute_son_joue = False

            temps_en_air = temps_actuel - self.timer_chute

            if temps_en_air >= 500 and not self.chute_son_joue:
                tombersfx.set_volume(0)
                tombersfx.play()
                self.chute_son_joue = True

            if self.chute_son_joue:
                progression = min((temps_en_air - 500) / 2000, 1.0)
                tombersfx.set_volume((progression * 0.5) if settings.option_3 else 0)

        else:
            if self.en_chute:
                tombersfx.stop()
                tombersfx.set_volume(0)
            self.en_chute = False
            self.chute_son_joue = False
        # Fadeout progressif au sol
        if self.chute_fadeout:
            vol_actuel = tombersfx.get_volume()
            if vol_actuel > 0.02:
                tombersfx.set_volume(vol_actuel - 0.03)
            else:
                tombersfx.stop()
                tombersfx.set_volume(0)
                self.chute_fadeout = False

        # Image de saut si en l'air
        if not self.est_au_sol(plateformes):
            if self.facing_left:
                self.image = pygame.transform.flip(sprites[9], True, False)
            else:
                self.image = sprites[9]

    # ------------------------------------------------------------------
    def update_double_jump_effects(self):
        for effect in self.double_jump_effects[:]:
            effect['alpha'] -= 15
            if effect['alpha'] <= 0:
                self.double_jump_effects.remove(effect)

    # ------------------------------------------------------------------
    def mettre_en_pause(self, temps_actuel):
        self._pause_vel_y = self.vel_y
        self._pause_vx = self.vx
        self.vel_y = 0
        self.vx = 0
        self._pause_marche_timer = self.marche_timer
        self._pause_timer_chute = self.timer_chute

    # ------------------------------------------------------------------
    def reprendre_apres_pause(self, temps_actuel):
        self.vel_y = getattr(self, '_pause_vel_y', self.vel_y)
        self.vx = getattr(self, '_pause_vx', self.vx)
        # Décale les timers pour éviter des glitches audio/animation
        duree_pause = temps_actuel - getattr(self, '_pause_marche_timer', temps_actuel)
        self.marche_timer = temps_actuel - duree_pause
        self.timer_chute = getattr(self, '_pause_timer_chute', temps_actuel)
        tombersfx.stop()
        tombersfx.set_volume(0)
        self.en_chute = False
        self.chute_son_joue = False
