import math
import pygame


class Esprit(pygame.sprite.Sprite):
    """ Esprit qui poursuit lentement le joueur sur le bateau """

    def __init__(self, x=1000, y=550):
        super().__init__()

        # Physique
        self.vel_y = 0
        self.gravity = 0.5
        self.on_ground = False

        self.frames = []
        self.frames.append(
            pygame.transform.scale(
                pygame.image.load("images/frame_esprit/esprit1.png").convert_alpha(),
                (76, 200),
            )
        )
        self.frames.append(
            pygame.transform.scale(
                pygame.image.load("images/frame_esprit/esprit2.png").convert_alpha(),
                (76, 200),
            ))

        self.image = self.frames[0]
        self.rect = pygame.Rect(x, y, 76, 200)
        self.type_monstre = "esprit"
        self.vitesse = 2

        self.distance_activation = 1500
        self.actif = False
        self.vivant = True

        self.current_frame = 0
        self.anim_timer = 0
        self.facing_left = False

    def update(self, joueur_rect, plateforme_bateau):
        if not self.vivant:
            return

        # Activation
        distance = math.hypot(
            joueur_rect.centerx - self.rect.centerx,
            joueur_rect.centery - self.rect.centery
        )

        if not self.actif and distance < self.distance_activation:
            self.actif = True

        # Déplacement horizontal
        deplacement_x = 0
        if self.actif:
            if joueur_rect.centerx < self.rect.centerx:
                deplacement_x = -self.vitesse
                self.facing_left = True
            else:
                deplacement_x = self.vitesse
                self.facing_left = False

        self.rect.x += deplacement_x

        # Animation
        now = pygame.time.get_ticks()
        if now - self.anim_timer > 600:  # plus grand = plus rapide
            if self.actif:
                self.anim_timer = now
                self.current_frame = (self.current_frame + 1) % len(self.frames)
            else:
                self.current_frame = 0

        img = self.frames[self.current_frame]
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        self.on_ground = False

        for p in plateforme_bateau:
            if self.rect.colliderect(p):
                if self.vel_y > 0:
                    self.rect.bottom = p.top
                    self.vel_y = 0
                    self.on_ground = True
                break
    def verifier_collision_joueur(
        self,
        joueur_rect,
        vies,
        invincible,
        current_time,
        invincibilite_temps,
        duree_invincibilite,
        hitbox_couteau=None,
        is_attacking=False,
    ):
        if not self.vivant:
            return vies, invincible, invincibilite_temps, False
        if is_attacking and hitbox_couteau and hitbox_couteau.colliderect(self.rect):
            self.vivant = False
            return vies, invincible, invincibilite_temps, True

        if not self.actif:
            return vies, invincible, invincibilite_temps, False

        if self.rect.colliderect(joueur_rect):
            if not invincible:
                vies -= 1
                invincible = True
                invincibilite_temps = current_time

        return vies, invincible, invincibilite_temps, False

    def update_and_collide(
    self,
    joueur,
    plateforme_bateau,
    vies,
    invincible,
    current_time,
    invincibilite_temps,
    duree_invincibilite,
):
        self.update(joueur.rect, plateforme_bateau)

        return self.verifier_collision_joueur(
            joueur.rect,
            vies,
            invincible,
            current_time,
            invincibilite_temps,
            duree_invincibilite,
            hitbox_couteau=joueur.hitbox_couteau,
            is_attacking=joueur.is_attacking
        )
    def draw(self, screen, camera_x, camera_y):
        if self.vivant:
            screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))