from tkinter.font import Font
import pygame
import subprocess
from joueur import Joueur
from niveau1 import get_plateformes, get_plateforme_danger
from sfx import musiquefond, degat, sfxdialogue

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
coeur = pygame.transform.scale(pygame.image.load("images/coeur.png").convert_alpha(), (100,100))
vie_text = pygame.transform.scale(pygame.image.load("images/vie.png").convert_alpha(), (186,72))
police = pygame.font.Font("asset/polices/Coolvetica Rg.otf", 24)
police_titre = pygame.font.Font("asset/polices/Dungeon Depths.otf", 50)
dialogue_sfx = sfxdialogue
dialogue_sfx.set_volume(0.5)
# Joueur
joueur = Joueur()
moving_sprites = pygame.sprite.Group()
moving_sprites.add(joueur)

# Système d'invincibilité
invincible = False
invincibilite_temps = 0
duree_invincibilite = 2000

# TITRE DEBUT DE JEU
titre = "L'Enfer"

# Npc
active = False
messages = ["dodue et dodue",
            "j'aime les dodue",
            "galileo 2d"]
snip = police.render(' ', True, 'white')
counter = 0
speed =  5
active_message = 0
message = messages[active_message]
done = False

# Music
pygame.mixer.pre_init(44100)
ambient = musiquefond
ambient.set_volume(0.2)
ambient.play(-1)  # -1 = boucle infinie

# Plateformes normales
plateformes = get_plateformes()
niveau_largeur = 2000  # largeur totale du niveau

try:
    platform_image_orig = pygame.image.load("images/plateforme.png").convert_alpha()
except:
    platform_image_orig = None

platform_images = []
for plateforme in plateformes:
    if platform_image_orig:
        img = pygame.transform.scale(platform_image_orig, (plateforme.width, plateforme.height))
        platform_images.append(img)
    else:
        platform_images.append(None)

# plateformes de danger
plateformes_danger = get_plateforme_danger() 

# Background zoomé
background_orig = pygame.image.load("images/background.png").convert_alpha()
img_w, img_h = background_orig.get_size()

# garder les proportions
ratio = max(screen_width / img_w, screen_height / img_h)
bg_width = int(img_w * ratio * zoom_factor)
bg_height = int(img_h * ratio * zoom_factor)
background = pygame.transform.smoothscale(background_orig, (bg_width, bg_height))
bg_offset_x = -200
bg_offset_y = -300
parallax_factor = 0.5

# Ajustement initial du joueur
for plat in plateformes:
    if joueur.rect.colliderect(plat):
        joueur.rect.bottom = plat.top
        joueur.vel_y = 0
# -------------------------------------------------------------------------------------------------#
#                                       Boucle principale                                          #
# -------------------------------------------------------------------------------------------------#
running = True
while running:
    clock.tick(60)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and done and active_message <   len(messages) - 1:
                active_message += 1
                done = False
                message = messages[active_message]
                counter=0
    keys = pygame.key.get_pressed() # quand une touche est pressée
    if keys[pygame.K_d]:
        joueur.is_animating = True
        joueur.facing_left = False
    elif keys[pygame.K_q]:
        joueur.is_animating = True
        joueur.facing_left = True
    else:
        joueur.is_animating = False

    # Déplacement et gravité
    joueur.deplacement(plateformes)
    joueur.appliquer_gravite(plateformes)

    # Collision avec plateformes de danger
    if not invincible:
        for plat_danger in plateformes_danger:
            if joueur.rect.colliderect(plat_danger):
                vies -= 1
                degat.play()
                invincible = True
                invincibilite_temps = current_time
                if vies <= 0:
                    etat = "game_over"
                break

    # Gestion de l'invincibilité
    if invincible:
        if current_time - invincibilite_temps > duree_invincibilite:
            invincible = False

    # Chute mortelle
    if joueur.rect.top > chute_y:
        vies = 0
        etat = "game_over"
    if etat == "game_over":
        pygame.quit()
        subprocess.run(['python', 'menu_de_fin.py'])
        running = False

    # Scrolling
    camera_x = joueur.rect.centerx - screen_width // 2
    camera_x = max(0, min(camera_x, niveau_largeur - screen_width))

    camera_y = joueur.rect.centery - screen_height // 2
    camera_y = max(0, camera_y)

    bg_x = -camera_x * parallax_factor + bg_offset_x
    bg_y = -camera_y * parallax_factor + bg_offset_y
    screen.blit(background, (bg_x, bg_y))

    # Affichage du joueur avec effet de clignotement si invincible
    afficher_joueur = True
    if invincible:
        # Clignotement : visible/invisible toutes les 100ms
        afficher_joueur = (current_time // 100) % 2 == 0
    if afficher_joueur:screen.blit(joueur.image,(joueur.rect.x - camera_x, joueur.rect.y - camera_y))
    
    # Affichage des plateformes normales
    for plat, img in zip(plateformes, platform_images):
        if img:
            screen.blit(img,(plat.x - camera_x + 55,plat.y - camera_y + 95))

    # Affichage des plateformes de danger (rouges)
    for plat_danger in plateformes_danger:
        pygame.draw.rect(
            screen,
            (255, 0, 0),(plat_danger.x - camera_x,plat_danger.y - camera_y,plat_danger.width,plat_danger.height))
    
    # Affichage des vies 
    screen.blit(vie_text, (20,20)) # image + coordonnées
    joueur.update()        
    for i in range(vies):
        screen.blit(coeur, (230 + i * 110, 5))
    moving_sprites.update()

    # NPC
    if active == True:
        if counter < speed * len(message):
            counter += 1
            if counter % speed == 0:
                dialogue_sfx.play()
        elif counter >= speed*len(message):
            dialogue_sfx.stop()
            one = True
        snip = police.render(message[0:counter//speed], True, 'white')

    if counter < speed * len(titre):
        counter += 1
        if counter % speed == 0:
            dialogue_sfx.play()
    elif counter >= speed*len(titre):
        dialogue_sfx.stop()
        done = True
    titre_texte = police_titre.render(titre[0:counter//speed], True, 'white')


    screen.blit(titre_texte, (20, 100))
    screen.blit(snip, (10,310))
    pygame.display.flip()
pygame.quit()