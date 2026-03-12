import pygame
import subprocess
from joueur import Joueur
from niveau1 import get_plateforme_prison, get_plateformes, get_plateforme_danger, get_sol
import sfx
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
police = pygame.font.Font("asset/polices/ari-w9500-bold.ttf", 24)
police_titre = pygame.font.Font("asset/polices/Dungeon Depths.otf", 50)
# Joueur
joueur = Joueur()
moving_sprites = pygame.sprite.Group()
moving_sprites.add(joueur)

# Système d'invincibilité
invincible = False
invincibilite_temps = 0
duree_invincibilite = 2000

# TITRE DEBUT DE JEU
dialogue_sfx = sfx.sfxdialogue
dialogue_sfx.set_volume(0.5)
titre = "L'Enfer"
titre_index = 0
titre_fin = 0  # servira à savoir quand le titre a fini
titre_sfx = sfx.fin
titre_sfx.set_volume(0.5)

# Npc
#npc 1
npcsfx = sfx.sfxnpc
npcsfx.set_volume(0.1)
giordano = pygame.image.load("images/giordano.png").convert_alpha()
giordano = pygame.transform.scale(giordano, (160, 105))
giordano_rect = giordano.get_rect()  
giordano_rect.topleft = (1600, 6300)
# dialogue avec giordano
bouton_e = pygame.image.load("images/bouton_e.png").convert_alpha()
bouton_e_rect = bouton_e.get_rect(topleft = (1600, 6250))
bouton_e = pygame.transform.scale(bouton_e, (50, 50))
dialogue_g = False
cadre_g = pygame.image.load("images/cadre_dialogue1.png").convert_alpha()
cadre_g_rect = cadre_g.get_rect(center=(640, 550))
# message avec giordano
messages = ["GALILEO !!",
            "C'EST UN ENFER !",]
counter = 0
speed =  5
active_message = 0
message = messages[active_message]
done = False

# Music
pygame.mixer.init(44100)
ambient = sfx.musiquefond
ambient.set_volume(0.2)
ambient.play(-1)  # -1 = boucle infinie

# Plateformes normales
plateformes_prison = get_plateforme_prison()
plateformes_niveau = get_plateformes()

plateformes = plateformes_prison + plateformes_niveau
sol = get_sol()

niveau_largeur = 2000  # largeur totale du niveau
try:
    platform_image_orig = pygame.image.load("images/plateforme_moyenne.png").convert_alpha()
except:
    platform_image_orig = None
platform_images = []
for plateforme in plateformes:
    if platform_image_orig:
        img = pygame.transform.scale(platform_image_orig, (plateforme.width, plateforme.height))
        platform_images.append(img)
    else:
        platform_images.append(None)
sol_image_orig = pygame.image.load("images/sol.png").convert_alpha()
sol_images = []
for s in sol:
    img = pygame.transform.scale(sol_image_orig, (s.width, s.height))
    sol_images.append(img)
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
            if event.key == pygame.K_e and dialogue_g and done:
                if active_message < len(messages) - 1:
                    active_message += 1
                    message = messages[active_message]
                    counter = 0
                    done = False
                else:
                    # FIN DU DIALOGUE
                    dialogue_g = False
                    done = False
                    active_message = 0
                    counter = 0
                    joueur.peut_bouger = True
            elif event.key == pygame.K_e and active and not dialogue_g:
                # OUVERTURE DU DIALOGUE
                dialogue_g = True
                joueur.peut_bouger = False
                counter = 0
                active_message = 0
                message = messages[0]
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
    joueur.deplacement(plateformes + sol)
    joueur.appliquer_gravite(plateformes + sol)

    # Collision avec plateformes de danger
    if not invincible:
        for plat_danger in plateformes_danger:
            if joueur.rect.colliderect(plat_danger):
                vies -= 1
                sfx.degat.play()
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
    if afficher_joueur:
        screen.blit(joueur.image,(joueur.rect.x - camera_x - 59, joueur.rect.y - camera_y))
    
    # Affichage des plateformes normales
    for plat, img in zip(plateformes, platform_images):
        if img:
            screen.blit(img,(plat.x - camera_x ,plat.y - camera_y + 95))
    # Affichage du sol
    for s, img in zip(sol, sol_images):
        screen.blit(img, (s.x - camera_x, s.y - camera_y + 100))

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
    # NPC
    player_visual_rect = pygame.Rect(joueur.rect.x - (150-32)//2,  # décalage à gauche
        joueur.rect.y - (150-32)//2,  # décalage en haut
        150,  # largeur du sprite
        150)   # hauteur du sprite)
    # Collision avec Giordano
    screen.blit(giordano, (giordano_rect.x - camera_x, giordano_rect.y - camera_y))
    active = player_visual_rect.colliderect(giordano_rect)
    # dialogue quand le joueur est proche de giordano
    if active and not dialogue_g:
        screen.blit(bouton_e, (bouton_e_rect.x - camera_x, bouton_e_rect.y - camera_y))
    if dialogue_g == True:
        snip = police.render(message[0:counter//speed], True, '#4f2310')
        joueur.peut_bouger = False
        joueur.is_animating = False
        screen.blit(cadre_g, cadre_g_rect)
        screen.blit(snip, (480,470))
        if counter < speed * len(message):
            counter += 1
            if counter % speed == 0:
                npcsfx.play()
        elif counter >= speed * len(message):
            npcsfx.stop()
            done = True
            screen.blit(bouton_e,(1000, 600))
        else:
            pass
    else:
        pass
    # titre L'enfer au début du jeu
    if titre_index < speed * len(titre):
        titre_index += 1
        dialogue_sfx.play()
    elif titre_index >= speed * len(titre) and titre_fin == 0:
        dialogue_sfx.stop()
        titre_fin = pygame.time.get_ticks()  # on note le moment de fin
        
    titre_texte = police_titre.render(titre[0:titre_index // speed], True, 'white')
    if titre_index < speed * len(titre) or (pygame.time.get_ticks() - titre_fin < 3000):
        screen.blit(titre_texte, (20, 100))
    else:
        if titre_fin > 0:
            sfx.fin.play(loops=0)
            titre_fin = -1
    pygame.display.flip()
pygame.quit()