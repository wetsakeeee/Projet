import pygame, sys
from sfx import sfxmarche1, sfxmarche2, sfxmarche3, sauter, tombersfx, couteausfx
import random, settings

pygame.mixer.init(44100)

sauter.set_volume(0.2 if settings.sfx else 0)

marche_sons = [sfxmarche1, sfxmarche2, sfxmarche3]
for s in marche_sons:
    s.set_volume(1 if settings.sfx else 0)

tombersfx.set_volume(0)


class Joueur(pygame.sprite.Sprite):
    def __init__(self, x=200, y=6299):
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
        self.rect = pygame.Rect(2350, 3800, 50, 100)        

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
        self.sprites_normal.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur009.png").convert_alpha(),(150,150)))
        self.sprites_normal.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur010.png").convert_alpha(),(150,150)))
        self.sprites_normal.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur011.png").convert_alpha(),(150,150)))
        self.sprites_normal.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/joueur012.png").convert_alpha(),(150,150)))

        # Frame joueur bottes
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
        self.sprites_botte.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte/joueur009botte.png").convert_alpha(),(150,150)))
        self.sprites_botte.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte/joueur010botte.png").convert_alpha(),(150,150)))
        self.sprites_botte.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte/joueur011botte.png").convert_alpha(),(150,150)))
        self.sprites_botte.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte/joueur012botte.png").convert_alpha(),(150,150)))


        # Frame joueur couteau
        self.sprites_couteau = []
        self.sprites_couteau.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_couteau/joueur_couteau0.png").convert_alpha(),(150,150)))
        self.sprites_couteau.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_couteau/joueur_couteau1.png").convert_alpha(),(150,150)))
        self.sprites_couteau.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_couteau/joueur_couteau2.png").convert_alpha(),(150,150)))
        self.sprites_couteau.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_couteau/joueur_couteau3.png").convert_alpha(),(150,150)))
        self.sprites_couteau.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_couteau/joueur_couteau4.png").convert_alpha(),(150,150)))
        self.sprites_couteau.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_couteau/joueur_couteau5.png").convert_alpha(),(150,150)))
        self.sprites_couteau.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_couteau/joueur_couteau6.png").convert_alpha(),(150,150)))
        self.sprites_couteau.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_couteau/joueur_couteau7.png").convert_alpha(),(150,150)))
        self.sprites_couteau.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_couteau/joueur_couteau8.png").convert_alpha(),(150,150)))
        self.sprites_couteau.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_couteau/joueur_couteau9.png").convert_alpha(),(150,150)))
        self.sprites_couteau.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_couteau/joueur_couteau10.png").convert_alpha(),(150,150)))
        self.sprites_couteau.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_couteau/joueur_couteau11.png").convert_alpha(),(150,150)))
        self.sprites_couteau.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_couteau/joueur_couteau12.png").convert_alpha(),(150,150)))

        # Frame joueur couteau et bottes
        self.sprites_botte_couteau = []
        self.sprites_botte_couteau.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte_couteau/botte_couteau0.png").convert_alpha(),(150,150)))
        self.sprites_botte_couteau.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte_couteau/botte_couteau1.png").convert_alpha(),(150,150)))
        self.sprites_botte_couteau.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte_couteau/botte_couteau2.png").convert_alpha(),(150,150)))
        self.sprites_botte_couteau.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte_couteau/botte_couteau3.png").convert_alpha(),(150,150)))
        self.sprites_botte_couteau.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte_couteau/botte_couteau4.png").convert_alpha(),(150,150)))
        self.sprites_botte_couteau.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte_couteau/botte_couteau5.png").convert_alpha(),(150,150)))
        self.sprites_botte_couteau.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte_couteau/botte_couteau6.png").convert_alpha(),(150,150)))
        self.sprites_botte_couteau.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte_couteau/botte_couteau7.png").convert_alpha(),(150,150)))
        self.sprites_botte_couteau.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte_couteau/botte_couteau8.png").convert_alpha(),(150,150)))
        self.sprites_botte_couteau.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte_couteau/botte_couteau9.png").convert_alpha(),(150,150)))
        self.sprites_botte_couteau.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte_couteau/botte_couteau10.png").convert_alpha(),(150,150)))
        self.sprites_botte_couteau.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte_couteau/botte_couteau11.png").convert_alpha(),(150,150)))
        self.sprites_botte_couteau.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_botte_couteau/botte_couteau12.png").convert_alpha(),(150,150)))
        
        # Frame d'attaque du joueur
        self.attaque = []
        self.attaque.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/Attack/attaque_couteau.png").convert_alpha(),(150,150)))
        self.attaque.append(pygame.transform.scale(pygame.image.load("images/frame_joueur/Attack/attaque_couteau_botte.png").convert_alpha(),(150,150)))
        self.current_sprite = 0


        self.is_animating = False
        self.jump_sprite = 9
        self.jump_animating = False
        self.jump_animation_speed = 0.3

        # Mouvement
        self.vx = 0
        self.friction = 0.6
        self.vitesse = 5
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_force = -15
        self.facing_left = False
        self.peut_bouger = False
        self.au_sol = False

        # Inventaire
        self.double_saut     =  False
        self.couteau_equipee = False

        # Double saut
        self.nb_sauts = 0
        self.double_jump_effects = []

        # Sons de marche
        self.marche_timer = 0
        self.marche_intervalle = 350  # ms entre chaque pas

        # Son de chute
        self.timer_chute    = 0
        self.chute_son_joue = False
        self.en_chute       = False
        self.chute_fadeout  = False

        # Attaque
        self.is_attacking = False
        self.hitbox_couteau = pygame.Rect(0, 0, 50, 20)
        self.attack_duration = 500  # 0.5 seconde en ms

        # Frame joueur allongé
        self.sprite_allonger = pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_allonger/allonger.png").convert_alpha(), (150, 150))
        self.sprite_allonger_bottes = pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_allonger/allonger_bottes.png").convert_alpha(), (150, 150))
        self.sprite_allonger_couteau = pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_allonger/allonger_couteau.png").convert_alpha(), (150, 150))
        self.sprite_allonger_bottes_couteau = pygame.transform.scale(pygame.image.load("images/frame_joueur/frame_allonger/allonger_bottes_couteau.png").convert_alpha(), (150, 150))

        self.est_allonge = False
        self.rect_hauteur_normale = 100  # hauteur originale
        self.rect_hauteur_allonge = 40   # hauteur réduite

        self.cooldown_attaque = -10000  # au lieu de 0

    # ------------------------------------------------------------------
    def get_sprites(self):
        if self.double_saut and self.couteau_equipee:
            return self.sprites_botte_couteau
        if self.couteau_equipee:
            return self.sprites_couteau
        if self.double_saut:
            return self.sprites_botte
        return self.sprites_normal

    # ------------------------------------------------------------------
    def update(self):
        sprites = self.get_sprites()
        # Image allongé
        if self.est_allonge:
            if self.double_saut and self.couteau_equipee:
                img = self.sprite_allonger_bottes_couteau
            elif self.couteau_equipee:
                img = self.sprite_allonger_couteau
            elif self.double_saut:
                img = self.sprite_allonger_bottes
            else:
                img = self.sprite_allonger
            if self.facing_left:
                self.image = pygame.transform.flip(img, True, False)
            else:
                self.image = img
            return

        if not self.au_sol:
            if self.jump_animating:
                self.jump_sprite += self.jump_animation_speed
                if self.jump_sprite >= 12:
                    self.jump_sprite = 12
                    self.jump_animating = False

            img = sprites[int(self.jump_sprite)]
            if self.facing_left and self.peut_bouger:
                self.image = pygame.transform.flip(img, True, False)
            else:
                self.image = img
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

        if self.is_attacking:
            attack_img = self.attaque[0 if not self.double_saut else 1]
            if self.facing_left:
                self.image = pygame.transform.flip(attack_img, True, False)
            else:
                self.image = attack_img

    # ------------------------------------------------------------------
    def deplacement(self, plateformes):
        if not self.peut_bouger:
            self.is_animating = False
            return

        touches = pygame.key.get_pressed()

        # Allongement
        if touches[pygame.K_c] and self.au_sol:
            if not self.est_allonge:
                self.est_allonge = True
                ancienne_bottom = self.rect.bottom
                self.rect.height = self.rect_hauteur_allonge
                self.rect.bottom = ancienne_bottom
            self.vx = 0
            self.is_animating = False
            return
        else:
            if self.est_allonge:
                self.est_allonge = False
                ancienne_bottom = self.rect.bottom
                self.rect.height = self.rect_hauteur_normale
                self.rect.bottom = ancienne_bottom
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

        current_time = pygame.time.get_ticks()

        if touches[pygame.K_a] and self.couteau_equipee and not self.is_attacking:
            if current_time - self.cooldown_attaque >= 2500:  # réutilise self.cooldown_attaque comme cooldown attaque
                self.is_attacking = True
                self.cooldown_attaque = current_time
                couteausfx.play()

        if self.is_attacking:
            if current_time - self.cooldown_attaque >= 1000:
                self.is_attacking = False
            else:
                if self.facing_left:
                    self.hitbox_couteau.center = (self.rect.centerx - 65, self.rect.centery)
                else:
                    self.hitbox_couteau.center = (self.rect.centerx + 65, self.rect.centery)

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

        current_time = pygame.time.get_ticks()
        # Sons de marche
        if (touches[pygame.K_q] or touches[pygame.K_LEFT] or
                touches[pygame.K_d] or touches[pygame.K_RIGHT]):
            if self.est_au_sol(plateformes) and self.is_animating:
                if current_time - self.marche_timer >= self.marche_intervalle:
                    random.choice(marche_sons).play()
                    self.marche_timer = current_time

    # ------------------------------------------------------------------
    def est_au_sol(self, plateformes):
        return self.au_sol

    # ------------------------------------------------------------------
    def demarrer_animation_saut(self):
        self.jump_sprite = 9
        self.jump_animating = True

    # ------------------------------------------------------------------
    def appliquer_gravite(self, plateformes, murs=None):
        etait_au_sol = self.au_sol
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
                    self.jump_sprite = 9
                    self.jump_animating = False
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

        current_time = pygame.time.get_ticks()

        # --- Son de chute ---
        if not self.est_au_sol(plateformes):
            if not self.en_chute:
                self.en_chute = True
                self.timer_chute = current_time
                self.chute_son_joue = False

            temps_en_air = current_time - self.timer_chute

            if temps_en_air >= 500 and not self.chute_son_joue:
                tombersfx.set_volume(0)
                tombersfx.play()
                self.chute_son_joue = True

            if self.chute_son_joue:
                progression = min((temps_en_air - 500) / 2000, 1.0)
                tombersfx.set_volume((progression * 0.5) if settings.sfx else 0)

        else:
            if self.en_chute:
                tombersfx.stop()
                tombersfx.set_volume(0)
            self.en_chute = False
            self.chute_son_joue = False

        if etait_au_sol and not self.au_sol and self.vel_y > 0:
            self.jump_sprite = 12
            self.jump_animating = False
        # Fadeout progressif au sol
        if self.chute_fadeout:
            vol_actuel = tombersfx.get_volume()
            if vol_actuel > 0.02:
                tombersfx.set_volume(vol_actuel - 0.03)
            else:
                tombersfx.stop()
                tombersfx.set_volume(0)
                self.chute_fadeout = False

    # ------------------------------------------------------------------
    def update_double_jump_effects(self):
        for effect in self.double_jump_effects[:]:
            effect['alpha'] -= 15
            if effect['alpha'] <= 0:
                self.double_jump_effects.remove(effect)

    # ------------------------------------------------------------------
    def mettre_en_pause(self, current_time):
        self._pause_vel_y = self.vel_y
        self._pause_vx = self.vx
        self.vel_y = 0
        self.vx = 0
        self._pause_marche_timer = self.marche_timer
        self._pause_timer_chute = self.timer_chute
        self.pause_start = current_time

    # ------------------------------------------------------------------
    def reprendre_apres_pause(self, current_time):
        self.vel_y = getattr(self, '_pause_vel_y', self.vel_y)
        self.vx = getattr(self, '_pause_vx', self.vx)
        # Décale les timers pour éviter des glitches audio/animation
        duree_pause = current_time - getattr(self, '_pause_marche_timer', current_time)
        self.marche_timer = current_time - duree_pause
        self.timer_chute = getattr(self, '_pause_timer_chute', current_time)
        tombersfx.stop()
        tombersfx.set_volume(0)
        self.en_chute = False
        self.chute_son_joue = False
        pause_duree = current_time - self.pause_start
        self.cooldown_attaque += pause_duree
        if self.is_attacking and current_time - self.cooldown_attaque >= 1000:
            self.is_attacking = False