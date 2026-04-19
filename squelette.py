import math
import pygame
import random
from sfx import fireballsfx
class BouleDefeu:
    """Projectile lancé par le squelette."""
    def __init__(self, x, y, direction):
        self.vitesse = 8
        self.vx = self.vitesse * direction
        self.rect = pygame.Rect(x, y, 140, 78)
        self.vivant = True

        # Animation
        self.frames = []
        for i in range(1, 5):
            frame = pygame.transform.scale(pygame.image.load(f"images/frame_squelette/frame_fireball/fireball{i}.png").convert_alpha(), (282, 78))
            self.frames.append(pygame.transform.flip(frame, direction == -1, False))
        self.current_frame = 0
        self.anim_timer = 0
        self.VITESSE_ANIM_MS = 80  # ms par frame

    def update(self, joueur_rect, vies, invincible, current_time, invincibilite_temps):
        self.rect.x += self.vx

        # Avancer l'animation
        now = pygame.time.get_ticks()
        if now - self.anim_timer > self.VITESSE_ANIM_MS:
            self.anim_timer = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)

        if self.rect.x < -500 or self.rect.x > 8000:
            self.vivant = False
            return vies, invincible, invincibilite_temps

        if self.rect.colliderect(joueur_rect):
            self.vivant = False
            if not invincible:
                vies -= 1
                invincible = True
                invincibilite_temps = current_time

        return vies, invincible, invincibilite_temps

    def draw(self, screen, camera_x, camera_y):
        if self.vivant:
            img = self.frames[self.current_frame]
            if self.vx < 0:
                img = pygame.transform.flip(img, True, False)
            screen.blit(img, (self.rect.x - camera_x, self.rect.y - camera_y))


class Squelette(pygame.sprite.Sprite):
    """Squelette qui marche vers le joueur puis lance une boule de feu."""

    DUREE_ANIMATION_ATTAQUE_MS = 500  # Modifier ici pour changer la vitesse d'attaque

    def __init__(self, x=1000, y=430):
        super().__init__()

        # Physique
        self.vel_y = 0
        self.gravity = 0.5
        self.on_ground = False

        # Vitesse de déplacement (entre Esprit=2 et Monstre=3)
        self.vitesse = 2.5

        # ---- Frames de marche ----
        self.frames_marche = []
        self.frames_marche.append(
            pygame.transform.scale(
                pygame.image.load("images/frame_squelette/frame_squelette0.png").convert_alpha(),
                (100, 220),
            )
        )
        self.frames_marche.append(
            pygame.transform.scale(
                pygame.image.load("images/frame_squelette/frame_squelette1.png").convert_alpha(),
                (100, 220),
            )
        )
        self.frames_marche.append(
            pygame.transform.scale(
                pygame.image.load("images/frame_squelette/frame_squelette2.png").convert_alpha(),
                (100, 220),
            )
        )
        self.frames_marche.append(
            pygame.transform.scale(
                pygame.image.load("images/frame_squelette/frame_squelette3.png").convert_alpha(),
                (100, 220),
            )
        )
        self.frames_marche.append(
            pygame.transform.scale(
                pygame.image.load("images/frame_squelette/frame_squelette4.png").convert_alpha(),
                (100, 220),
            )
        )

        # ---- Frames d'attaque ----
        self.frames_attaque = []
        self.frames_attaque.append(
            pygame.transform.scale(
                pygame.image.load("images/frame_squelette/frame_attack/frame_squelette_attack1.png").convert_alpha(),
                (140, 224),
            )
        )
        self.frames_attaque.append(
            pygame.transform.scale(
                pygame.image.load("images/frame_squelette/frame_attack/frame_squelette_attack2.png").convert_alpha(),
                (140, 224),
            )
        )
        self.frames_attaque.append(
            pygame.transform.scale(
                pygame.image.load("images/frame_squelette/frame_attack/frame_squelette_attack3.png").convert_alpha(),
                (140, 224),
            )
        )
        self.frames_attaque.append(
            pygame.transform.scale(
                pygame.image.load("images/frame_squelette/frame_attack/frame_squelette_attack4.png").convert_alpha(),
                (140, 224),
            )
        )
        self.frames_attaque.append(
            pygame.transform.scale(
                pygame.image.load("images/frame_squelette/frame_attack/frame_squelette_attack5.png").convert_alpha(),
                (146, 224),
            )
        )
        self.frames_attaque.append(
            pygame.transform.scale(
                pygame.image.load("images/frame_squelette/frame_attack/frame_squelette_attack6.png").convert_alpha(),
                (140, 224),
            )
        )

        self.image = self.frames_marche[0]
        self.rect = pygame.Rect(x, y, 60, 150)
        self.type_monstre = "squelette"
        # ---- États ----
        self.distance_activation = 1500
        self.actif = False
        self.vivant = True
        self.facing_left = False

        # ---- Animation de marche ----
        self.current_frame_marche = 0
        self.anim_marche_timer = 0
        self.VITESSE_ANIM_MARCHE_MS = 180

        # ---- Cycle attaque ----
        self.TEMPS_MARCHE_AVANT_ATTAQUE_MS = 1300

        self.en_attaque = False
        self.attaque_timer = 0
        self.current_frame_attaque = 0
        self.boule_tiree = False

        self.timer_debut_marche = 0
        self.cycle_actif = False

        # ---- Projectiles ----
        self.boules = []

    # ------------------------------------------------------------------
    def update(self, joueur_rect, plateforme):
        if not self.vivant:
            return

        now = pygame.time.get_ticks()

        distance = math.hypot(
            joueur_rect.centerx - self.rect.centerx,
            joueur_rect.centery - self.rect.centery,
        )
        if not self.actif and distance < self.distance_activation:
            self.actif = True
            self.cycle_actif = True
            self.timer_debut_marche = now
            self.en_attaque = False

        if not self.actif:
            self.image = self.frames_marche[0]
            self._appliquer_gravite(plateforme)
            return

        # ---- Phase attaque ----
        if self.en_attaque:
            temps_attaque = now - self.attaque_timer
            nb_frames = len(self.frames_attaque)
            ms_par_frame = self.DUREE_ANIMATION_ATTAQUE_MS / nb_frames
            frame_idx = int(temps_attaque / ms_par_frame)

            if frame_idx >= nb_frames:
                frame_idx = nb_frames - 1

            # Tir à la dernière frame
            if frame_idx == nb_frames - 1 and not self.boule_tiree:
                self.boule_tiree = True
                direction = -1 if self.facing_left else 1
                bx = self.rect.left - 25 if self.facing_left else self.rect.right + 5
                by = self.rect.centery - random.choice([50, 130, 250])
                self.boules.append(BouleDefeu(bx, by, direction))
                fireballsfx.play()  # ← ici

            # Assigner l'image d'attaque
            self.image = self.frames_attaque[frame_idx]

            if temps_attaque >= self.DUREE_ANIMATION_ATTAQUE_MS:
                self.en_attaque = False
                self.boule_tiree = False
                self.timer_debut_marche = now

        # ---- Phase marche ----
        else:
            temps_marche = now - self.timer_debut_marche

            if joueur_rect.centerx < self.rect.centerx:
                self.rect.x -= self.vitesse
                self.facing_left = True
            else:
                self.rect.x += self.vitesse
                self.facing_left = False

            # Avancer la frame de marche
            if now - self.anim_marche_timer > self.VITESSE_ANIM_MARCHE_MS:
                self.anim_marche_timer = now
                self.current_frame_marche = (self.current_frame_marche % 4) + 1

            # Assigner l'image de marche
            self.image = self.frames_marche[self.current_frame_marche]

            if temps_marche >= self.TEMPS_MARCHE_AVANT_ATTAQUE_MS:
                self.en_attaque = True
                self.attaque_timer = now
                self.current_frame_attaque = 0
                self.boule_tiree = False

        self._appliquer_gravite(plateforme)
        self.boules = [b for b in self.boules if b.vivant]

    # ------------------------------------------------------------------
    def _appliquer_gravite(self, plateforme):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y
        self.on_ground = False

        plateformes = plateforme if isinstance(plateforme, list) else [plateforme]
        for p in plateformes:
            if self.rect.colliderect(p):
                if self.vel_y > 0:
                    self.rect.bottom = p.top
                    self.vel_y = 0
                    self.on_ground = True
                break

    # ------------------------------------------------------------------
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

        for boule in self.boules:
            vies, invincible, invincibilite_temps = boule.update(
                joueur_rect, vies, invincible, current_time, invincibilite_temps
            )

        return vies, invincible, invincibilite_temps, False

    # ------------------------------------------------------------------
    def update_and_collide(
        self,
        joueur,
        plateforme,
        vies,
        invincible,
        current_time,
        invincibilite_temps,
        duree_invincibilite,
    ):
        self.update(joueur.rect, plateforme)
        return self.verifier_collision_joueur(
            joueur.rect,
            vies,
            invincible,
            current_time,
            invincibilite_temps,
            duree_invincibilite,
            hitbox_couteau=joueur.hitbox_couteau,
            is_attacking=joueur.is_attacking,
        )

    # ------------------------------------------------------------------
    def draw(self, screen, camera_x, camera_y):
        if self.vivant:
            screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y- 80))
            for boule in self.boules:
                boule.draw(screen, camera_x, camera_y)