import math
import pygame


class Monstre(pygame.sprite.Sprite):
    def __init__(self, x=1700, y=3280):
        super().__init__()

        self.frames = []
        self.frames.append(
            pygame.transform.scale(
                pygame.image.load("images/frame_monstre/monstre1.png").convert_alpha(),
                (250, 250),
            )
        )
        self.frames.append(
            pygame.transform.scale(
                pygame.image.load("images/frame_monstre/monstre2.png").convert_alpha(),
                (250, 250),
            )
        )
        self.frames.append(
            pygame.transform.scale(
                pygame.image.load("images/frame_monstre/monstre3.png").convert_alpha(),
                (250, 250),
            )
        )
        self.frames.append(
            pygame.transform.scale(
                pygame.image.load("images/frame_monstre/monstre4.png").convert_alpha(),
                (250, 250),
            )
        )

        self.image = self.frames[0]
        self.rect = pygame.Rect(x, y, 100, 250)
        self.vitesse = 4
        self.vel_y = 0
        self.gravity = 0.5
        self.distance_activation = 800
        self.distance_perte_agro = 1000

        self.actif = False
        self.vivant = True
        self.current_frame = 0
        self.anim_timer = 0
        self.facing_left = False

    def update(self, joueur_rect, plateformes):
        if not self.vivant:
            return

        distance_x = joueur_rect.centerx - self.rect.centerx
        distance_y = joueur_rect.centery - self.rect.centery
        distance = math.hypot(distance_x, distance_y)

        if not self.actif:
            if distance < self.distance_activation:
                self.actif = True
        elif distance > self.distance_perte_agro:
            self.actif = False

        deplacement_x = 0
        if self.actif:
            if joueur_rect.centerx < self.rect.centerx:
                deplacement_x = -self.vitesse
                self.facing_left = True
            else:
                deplacement_x = self.vitesse
                self.facing_left = False

        self.rect.x += deplacement_x
        for plat in plateformes:
            if self.rect.colliderect(plat):
                if deplacement_x > 0:
                    self.rect.right = plat.left
                elif deplacement_x < 0:
                    self.rect.left = plat.right

        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        for plat in plateformes:
            if self.rect.colliderect(plat):
                if self.vel_y >= 0:
                    self.rect.bottom = plat.top
                    self.vel_y = 0
                elif self.vel_y < 0:
                    self.rect.top = plat.bottom
                    self.vel_y = 0

        now = pygame.time.get_ticks()
        if now - self.anim_timer > 150:
            self.anim_timer = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)

        img = self.frames[self.current_frame]
        if self.facing_left:
            self.image = pygame.transform.flip(img, True, False)
        else:
            self.image = img

    def verifier_collision_joueur(
        self,
        joueur_rect,
        vies,
        invincible,
        current_time,
        invincibilite_temps,
        duree_invincibilite,
    ):
        if not self.vivant or not self.actif:
            return vies, invincible, invincibilite_temps, False

        if self.rect.colliderect(joueur_rect):
            if joueur_rect.bottom <= self.rect.centery and joueur_rect.bottom >= self.rect.top - 15:
                self.vivant = False
                return vies, invincible, invincibilite_temps, True

            if not invincible:
                vies -= 1
                invincible = True
                invincibilite_temps = current_time

        return vies, invincible, invincibilite_temps, False

    def update_and_collide(
        self,
        joueur,
        plateformes,
        vies,
        invincible,
        current_time,
        invincibilite_temps,
        duree_invincibilite,
    ):
        self.update(joueur.rect, plateformes)
        return self.verifier_collision_joueur(
            joueur.rect,
            vies,
            invincible,
            current_time,
            invincibilite_temps,
            duree_invincibilite,
        )

    def draw(self, screen, camera_x, camera_y):
        if self.vivant:
            screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
