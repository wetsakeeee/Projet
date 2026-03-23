import pygame
import subprocess
import math
from joueur import Joueur
from niveau1 import get_plateforme_prison, get_plateformes, plateforme_pic, plateforme_pic2, get_sol, get_plateformeshaute
import sfx
import random
import sys

# ----------------------------
# Initialisation Pygame
# ----------------------------
pygame.init()
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
icon = pygame.image.load("images/logo.png").convert_alpha()
pygame.display.set_icon(icon)
pygame.display.set_caption("Galileo Galilei")
clock = pygame.time.Clock()

etat = "jeu"
vies = 3
chute_y = 7000
zoom_factor = 1.5

coeur       = pygame.transform.scale(pygame.image.load("images/coeur.png").convert_alpha(), (100, 100))
vie_text    = pygame.transform.scale(pygame.image.load("images/vie.png").convert_alpha(), (186, 72))
double_jump = pygame.transform.scale(pygame.image.load("images/icone_double_jump.png").convert_alpha(), (100, 100))

police       = pygame.font.Font("asset/polices/ari-w9500-bold.ttf", 24)
police_titre = pygame.font.Font("asset/polices/Dungeon Depths.otf", 50)

# Joueur
if len(sys.argv) == 3:
    joueur = Joueur(int(sys.argv[1]), int(sys.argv[2]))
else:
    joueur = Joueur()
moving_sprites = pygame.sprite.Group()
moving_sprites.add(joueur)

# Système d'invincibilité
invincible          = False
invincibilite_temps = 0
duree_invincibilite = 2000

# TITRE DEBUT DE JEU
dialogue_sfx = sfx.sfxdialogue
dialogue_sfx.set_volume(0.5)
titre       = "L'Enfer"
titre_index = 0
titre_fin   = 0
titre_sfx   = sfx.fin
titre_sfx.set_volume(0.5)

# Pancarte
panneau = pygame.image.load("images/panneau.png").convert_alpha()
panneau = pygame.transform.scale(panneau, (96, 150))
panneau_rect = panneau.get_rect()
panneau_rect.topleft = (800, 6270)
pancarte_active        = False
panneau_button_hidden  = False
panneau_button_timer   = 0
pancarte = pygame.transform.scale(pygame.image.load("images/pancarte.png").convert_alpha(), (850, 500))
lire_pancarte          = False
pancarte_timer         = 0
show_button_e_pancarte = False

liresfx = sfx.liresfx
liresfx.set_volume(0.5)
stoplire = sfx.stoplire
stoplire.set_volume(0.5)

# --- INVENTAIRE ---
icone_inventaire         = pygame.transform.scale(pygame.image.load("images/icone_inventaire.png").convert_alpha(), (100, 100))
inventaire_img           = pygame.transform.scale(pygame.image.load("images/inventaire.png").convert_alpha(), (560, 630))
inventaire_affiche       = False
inventaire_timer         = 0
show_button_e_inventaire = False

# NPC 1 — Giordano (animation 3 frames)
npcsfx = sfx.sfxnpc
npcsfx.set_volume(0.1)

giordano  = pygame.transform.scale(pygame.image.load("images/giordano.png").convert_alpha(),  (160, 105))
giordano2 = pygame.transform.scale(pygame.image.load("images/giordano2.png").convert_alpha(), (160, 105))
giordano3 = pygame.transform.scale(pygame.image.load("images/giordano3.png").convert_alpha(), (160, 105))
giordano_images    = [giordano, giordano2, giordano3]
current_giordano   = 0
giordano_anim_timer = 0
giordano_forward   = True
giordano_pause     = False
giordano_pause_timer = 0

giordano_rect = giordano.get_rect()
giordano_rect.topleft = (1600, 6300)

bouton_e      = pygame.image.load("images/bouton_e.png").convert_alpha()
bouton_e_rect = bouton_e.get_rect(topleft=(1600, 6250))
bouton_e      = pygame.transform.scale(bouton_e, (50, 50))
dialogue_g    = False
cadre_g       = pygame.image.load("images/cadre_dialogue1.png").convert_alpha()
cadre_g_rect  = cadre_g.get_rect(center=(640, 550))
messages      = ["GALILEO !!", "C'EST UN ENFER !"]

# --- Cooldowns NPC ---
giordano_cooldown = -30000
virgilio_cooldown = -30000
duree_cooldown    = 30000  # 30 secondes

# NPC 2 — Virgilio
virgilio      = pygame.transform.scale(pygame.image.load("images/virgilio.png").convert_alpha(), (56, 112))
virgilio_rect = virgilio.get_rect()
virgilio_rect.topleft = (700, 4190)
dialogue_v    = False
cadre_v       = pygame.image.load("images/cadre_dialogue2.png").convert_alpha()
cadre_v_rect  = cadre_v.get_rect(center=(640, 550))

counter         = 0
speed           = 5
active_message  = 0
message         = messages[active_message]
done            = False
message_v       = ["Prends cette potion pour sauter deux fois."]
active_message2 = 0
message2        = message_v[active_message2]

# MURS
plateformes_haute = get_plateformeshaute()

# Music
pygame.mixer.init(44100)
ambient = sfx.musiquefond
ambient.set_volume(0.2)
ambient.play(-1)

# Plateformes
plateformes_prison = get_plateforme_prison()
plateformes_niveau = get_plateformes()
plateformes        = plateformes_niveau
sol                = get_sol()
niveau_largeur     = 2000

try:
    platform_image_orig  = pygame.image.load("images/plateforme_moyenne.png").convert_alpha()
    platform_petite_orig = pygame.image.load("images/plateforme_petite.png").convert_alpha()
except:
    platform_image_orig  = None
    platform_petite_orig = None

platform_images = []
for plateforme in plateformes:
    if plateforme.width == 100 and plateforme.height == 40:
        orig = platform_petite_orig
    else:
        orig = platform_image_orig
    if orig:
        img = pygame.transform.scale(orig, (plateforme.width, plateforme.height))
        platform_images.append(img)
    else:
        platform_images.append(None)

sol_image_orig = pygame.image.load("images/sol.png").convert_alpha()
sol_images = []
for s in sol:
    img = pygame.transform.scale(sol_image_orig, (s.width, s.height))
    sol_images.append(img)

# Plateformes de danger
plateformes_danger  = plateforme_pic()
plateformes_danger2 = plateforme_pic2()

pic_sol_orig     = pygame.image.load("images/pic_sol.png").convert_alpha()
pic_plafond_orig = pygame.image.load("images/pic_plafond.png").convert_alpha()

pic_sol_images = []
for plat in plateformes_danger:
    img = pygame.transform.scale(pic_sol_orig, (plat.width, plat.height))
    pic_sol_images.append(img)

pic_plafond_images = []
for plat in plateformes_danger2:
    img = pygame.transform.scale(pic_plafond_orig, (plat.width, plat.height))
    pic_plafond_images.append(img)

# Murs prison
mur_prison_orig   = pygame.image.load("images/murprison.png").convert_alpha()
mur_prison_images = []
for mur in plateformes_prison:
    img = pygame.transform.scale(mur_prison_orig, (mur.width, mur.height))
    mur_prison_images.append(img)

# Background
background_orig = pygame.image.load("images/background.png").convert_alpha()
img_w, img_h    = background_orig.get_size()
ratio           = max(screen_width / img_w, screen_height / img_h)
bg_width        = int(img_w * ratio * zoom_factor)
bg_height       = int(img_h * ratio * zoom_factor)
background      = pygame.transform.smoothscale(background_orig, (bg_width, bg_height))
bg_offset_x     = -200
bg_offset_y     = -300
parallax_factor = 0.5

# Ajustement initial du joueur
for plat in plateformes:
    if joueur.rect.colliderect(plat):
        joueur.rect.bottom = plat.top
        joueur.vel_y = 0

# -------------------------------------------------------------------------------------------------#
# Boucle principale
# -------------------------------------------------------------------------------------------------#
running = True
while running:
    clock.tick(60)
    current_time  = pygame.time.get_ticks()
    button_offset = int(math.sin(current_time * 0.01) * 3)

    # Animation de Giordano
    if not giordano_pause:
        if giordano_forward:
            if current_giordano == 0 and current_time - giordano_anim_timer > 500:
                current_giordano = 1
                giordano_anim_timer = current_time
            elif current_giordano == 1 and current_time - giordano_anim_timer > 500:
                current_giordano = 2
                giordano_anim_timer = current_time
            elif current_giordano == 2 and current_time - giordano_anim_timer > 500:
                giordano_pause = True
                giordano_pause_timer = current_time
        else:
            if current_giordano == 1 and current_time - giordano_anim_timer > 500:
                current_giordano = 0
                giordano_anim_timer = current_time
            elif current_giordano == 0 and current_time - giordano_anim_timer > 500:
                giordano_pause = True
                giordano_pause_timer = current_time
    else:
        if current_time - giordano_pause_timer > 500:
            if giordano_forward and current_giordano == 2:
                giordano_forward = False
                current_giordano = 1
                giordano_anim_timer = current_time
            elif not giordano_forward and current_giordano == 0:
                giordano_forward = True
                current_giordano = 1
                giordano_anim_timer = current_time
            giordano_pause = False

    # ---- Événements ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Dialogue Giordano — avancer / fermer
            if event.key == pygame.K_e and dialogue_g and done:
                if active_message < len(messages) - 1:
                    active_message += 1
                    message = messages[active_message]
                    counter = 0
                    done = False
                else:
                    dialogue_g = False
                    done = False
                    active_message = 0
                    counter = 0
                    joueur.peut_bouger = True
                    if current_time - giordano_cooldown > duree_cooldown:
                        vies += 1
                        giordano_cooldown = current_time

            # Dialogue Giordano — ouvrir
            elif event.key == pygame.K_e and active and not dialogue_g:
                dialogue_g = True
                joueur.peut_bouger = False
                counter = 0
                active_message = 0
                message = messages[0]

            # Dialogue Virgilio — avancer / fermer
            elif event.key == pygame.K_e and dialogue_v and done:
                if active_message2 < len(message_v) - 1:
                    active_message2 += 1
                    message2 = message_v[active_message2]
                    counter = 0
                    done = False
                else:
                    dialogue_v = False
                    done = False
                    active_message2 = 0
                    counter = 0
                    joueur.peut_bouger = True
                    joueur.double_saut = True
                    if current_time - virgilio_cooldown > duree_cooldown:
                        vies += 1
                        virgilio_cooldown = current_time

            # Dialogue Virgilio — ouvrir
            elif event.key == pygame.K_e and active2 and not dialogue_v:
                dialogue_v = True
                joueur.peut_bouger = False
                counter = 0
                active_message2 = 0
                message2 = message_v[0]

            # Pancarte — ouvrir
            elif event.key == pygame.K_e and pancarte_active and not lire_pancarte:
                lire_pancarte = True
                joueur.peut_bouger = False
                pancarte_timer = current_time
                if titre_index >= speed * len(titre) and titre_fin == 0:
                    titre_fin = current_time
                liresfx.play()

            # Pancarte — fermer
            elif event.key == pygame.K_e and show_button_e_pancarte:
                lire_pancarte = False
                show_button_e_pancarte = False
                joueur.peut_bouger = True
                panneau_button_hidden = True
                panneau_button_timer = current_time
                stoplire.play()

            # Inventaire — fermer avec E
            elif event.key == pygame.K_e and inventaire_affiche and show_button_e_inventaire:
                inventaire_affiche = False
                show_button_e_inventaire = False
                joueur.peut_bouger = True

        # Inventaire — ouvrir au clic sur l'icône
        if event.type == pygame.MOUSEBUTTONDOWN:
            icone_inv_rect = pygame.Rect(screen_width - 150, screen_height - 150, 100, 100)
            if icone_inv_rect.collidepoint(event.pos) and not inventaire_affiche:
                inventaire_affiche = True
                joueur.peut_bouger = False
                inventaire_timer = current_time
                show_button_e_inventaire = False

    # ---- Touches maintenues ----
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        joueur.is_animating = True
        joueur.facing_left  = False
    elif keys[pygame.K_q]:
        joueur.is_animating = True
        joueur.facing_left  = True
    else:
        joueur.is_animating = False

    # ---- Timers ----
    if inventaire_affiche and not show_button_e_inventaire and current_time - inventaire_timer > 3000:
        show_button_e_inventaire = True

    if lire_pancarte and not show_button_e_pancarte and current_time - pancarte_timer > 3000:
        show_button_e_pancarte = True

    if panneau_button_hidden and current_time - panneau_button_timer > 2000:
        panneau_button_hidden = False

    # ---- Physique ----
    joueur.deplacement(plateformes + plateformes_prison + sol)
    joueur.appliquer_gravite(plateformes + plateformes_prison + sol, murs=plateformes_haute)
    joueur.update_double_jump_effects()

    # Collisions danger
    if not invincible:
        for plat_danger in plateformes_danger + plateformes_danger2:
            if joueur.rect.colliderect(plat_danger):
                vies -= 1
                sfx.degat.play()
                invincible = True
                invincibilite_temps = current_time
                if vies <= 0:
                    etat = "game_over"
                break

    if invincible and current_time - invincibilite_temps > duree_invincibilite:
        invincible = False

    if joueur.rect.top > chute_y:
        vies = 0
        etat = "game_over"

    if etat == "game_over":
        pygame.quit()
        subprocess.run(['python', 'menu_de_fin.py'])
        running = False
        break

    # ---- Caméra ----
    camera_x = joueur.rect.centerx - screen_width // 2
    camera_x = max(0, min(camera_x, niveau_largeur - screen_width))
    camera_y = joueur.rect.centery - screen_height // 2
    camera_y = max(0, camera_y)

    bg_x = -camera_x * parallax_factor + bg_offset_x
    bg_y = -camera_y * parallax_factor + bg_offset_y

    # ========================
    # RENDU
    # ========================
    screen.blit(background, (bg_x, bg_y + 100))

    # Murs prison
    for mur, img in zip(plateformes_prison, mur_prison_images):
        screen.blit(img, (mur.x - camera_x, mur.y - camera_y))

    # Plateformes normales
    for plat, img in zip(plateformes, platform_images):
        if img:
            screen.blit(img, (plat.x - camera_x, plat.y - camera_y + 100))

    # Sol
    for s, img in zip(sol, sol_images):
        screen.blit(img, (s.x - camera_x, s.y - camera_y + 87))

    # Pics sol
    for plat, img in zip(plateformes_danger, pic_sol_images):
        screen.blit(img, (plat.x - camera_x, plat.y - camera_y))

    # Pics plafond
    for plat, img in zip(plateformes_danger2, pic_plafond_images):
        screen.blit(img, (plat.x - camera_x, plat.y - camera_y))

    # Plateformes hautes (murs invisibles)
    for plat_haute in plateformes_haute:
        pygame.draw.rect(screen, (0, 0, 0),
                         (plat_haute.x - camera_x, plat_haute.y - camera_y,
                          plat_haute.width, plat_haute.height))

    # Panneau
    screen.blit(panneau, (panneau_rect.x - camera_x, panneau_rect.y - camera_y - 20))
    pancarte_active = joueur.rect.colliderect(panneau_rect) and not panneau_button_hidden
    if pancarte_active:
        screen.blit(bouton_e, (bouton_e_rect.x - camera_x - 700, bouton_e_rect.y - camera_y + button_offset))

    # Joueur (clignotement si invincible)
    afficher_joueur = True
    if invincible:
        afficher_joueur = (current_time // 100) % 2 == 0
    if afficher_joueur:
        screen.blit(joueur.image, (joueur.rect.x - camera_x - 59, joueur.rect.y - camera_y))

    # Effets double saut
    for effect in joueur.double_jump_effects:
        effect_surface = pygame.Surface((effect['width'], effect['height']), pygame.SRCALPHA)
        effect_surface.fill((255, 255, 255, effect['alpha']))
        screen.blit(effect_surface, (effect['x'] - camera_x - effect['width'] // 2, effect['y'] - camera_y))

    # Giordano animé
    screen.blit(giordano_images[current_giordano], (giordano_rect.x - camera_x, giordano_rect.y - camera_y))

    # Virgilio
    screen.blit(virgilio, (virgilio_rect.x - camera_x, virgilio_rect.y - camera_y))

    # Vies HUD
    if not lire_pancarte:
        screen.blit(vie_text, (20, 20))
    for i in range(vies):
        screen.blit(coeur, (230 + i * 110, 5))

    # Icône double saut HUD (visible seulement si le double saut est débloqué)
    if joueur.double_saut:
        screen.blit(double_jump, (screen_width - 150, screen_height - 260))

    # Icône inventaire HUD
    screen.blit(icone_inventaire, (screen_width - 150, screen_height - 150))

    joueur.update()

    # Zone de détection joueur pour les NPC
    player_visual_rect = pygame.Rect(
        joueur.rect.x - (150 - 32) // 2,
        joueur.rect.y - (150 - 32) // 2,
        150, 150
    )

    # Giordano — bouton E + dialogue
    active = player_visual_rect.colliderect(giordano_rect)
    if active and not dialogue_g:
        screen.blit(bouton_e, (bouton_e_rect.x - camera_x, bouton_e_rect.y - camera_y + button_offset))
    if dialogue_g:
        snip = police.render(message[0:counter // speed], True, '#4f2310')
        joueur.peut_bouger = False
        joueur.is_animating = False
        screen.blit(cadre_g, cadre_g_rect)
        screen.blit(snip, (480, 470))
        if counter < speed * len(message):
            counter += 1
            if counter % speed == 0:
                npcsfx.play()
        elif counter >= speed * len(message):
            npcsfx.stop()
            done = True
            screen.blit(bouton_e, (1000, 600 + button_offset))

    # Virgilio — bouton E + dialogue
    active2 = player_visual_rect.colliderect(virgilio_rect)
    if active2 and not dialogue_v:
        screen.blit(bouton_e, ((bouton_e_rect.x - 900) - camera_x, (bouton_e_rect.y - 2110) - camera_y + button_offset))
    if dialogue_v:
        snip = police.render(message2[0:counter // speed], True, '#4f2310')
        joueur.peut_bouger = False
        joueur.is_animating = False
        screen.blit(cadre_v, cadre_v_rect)
        screen.blit(snip, (480, 470))
        if counter < speed * len(message2):
            counter += 1
            if counter % speed == 0:
                npcsfx.play()
        elif counter >= speed * len(message2):
            npcsfx.stop()
            done = True
            screen.blit(bouton_e, (1020, 550 + button_offset))

    # Titre "L'Enfer"
    if titre_index < speed * len(titre):
        titre_index += 1
        dialogue_sfx.play()
    elif titre_index >= speed * len(titre) and titre_fin == 0:
        dialogue_sfx.stop()
        titre_fin = pygame.time.get_ticks()

    titre_texte = police_titre.render(titre[0:titre_index // speed], True, 'white')
    if (titre_index < speed * len(titre) or (pygame.time.get_ticks() - titre_fin < 3000)) and not lire_pancarte:
        screen.blit(titre_texte, (20, 100))
    else:
        if titre_fin > 0:
            sfx.fin.play(loops=0)
            titre_fin = -1

    # Pancarte
    if lire_pancarte:
        pancarte_x = screen_width // 2 - pancarte.get_width() // 2
        pancarte_y = screen_height // 2 - pancarte.get_height() // 2
        screen.blit(pancarte, (pancarte_x, pancarte_y))
        if show_button_e_pancarte:
            screen.blit(bouton_e, (950, 500 + button_offset))

    # Inventaire
    if inventaire_affiche:
        inv_x = screen_width // 2 - inventaire_img.get_width() // 2
        inv_y = screen_height // 2 - inventaire_img.get_height() // 2
        screen.blit(inventaire_img, (inv_x, inv_y))
        if show_button_e_inventaire:
            screen.blit(bouton_e, (850, 600 + button_offset))

    pygame.display.flip()

pygame.quit()