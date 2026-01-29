import pygame
import subprocess
from joueur import Joueur
from niveau1 import get_plateformes


# ----------------------------
# Initialisation Pygame
# ----------------------------
pygame.init()
screen_width, screen_height = 1280, 720
ecran = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Galileo Galilei")
clock = pygame.time.Clock()
etat = "jeu"
vies = 3
chute_y = 7000

# ----------------------------
# Joueur
# ----------------------------
joueur = Joueur()

# ----------------------------
# Music
# ----------------------------
pygame.mixer.init()
sound = pygame.mixer.Sound("jump.mp3")
ambient = pygame.mixer.Sound("music_enfer.mp3")

ambient.set_volume(0.4)
ambient.play(-1)  # -1 = boucle infinie



# ----------------------------
# Plateformes
# ----------------------------
plateformes = get_plateformes()
niveau_largeur = 2000  # largeur totale du niveau

try:
    platform_image_orig = pygame.image.load("images/platforme.jpg").convert_alpha()
except:
    platform_image_orig = None

platform_images = []
for plateforme in plateformes:
    if platform_image_orig:
        img = pygame.transform.scale(platform_image_orig, (plateforme.width, plateforme.height))
        platform_images.append(img)
    else:
        platform_images.append(None)

# ----------------------------
# Background zoomé
# ----------------------------
background_orig = pygame.image.load("images/background.png").convert_alpha()

img_w, img_h = background_orig.get_size()

zoom_factor = 1.5

# garder les proportions
ratio = max(screen_width / img_w, screen_height / img_h)
bg_width = int(img_w * ratio * zoom_factor)
bg_height = int(img_h * ratio * zoom_factor)

background = pygame.transform.smoothscale(background_orig, (bg_width, bg_height))

bg_offset_x = -200
bg_offset_y = -300
parallax_factor = 0.5


# ----------------------------
# Ajustement initial du joueur si il commence sur une plateforme
# ----------------------------
for plat in plateformes:
    if joueur.rect.colliderect(plat):
        joueur.rect.bottom = plat.top
        joueur.vel_y = 0

# ----------------------------
# Boucle principale
# ----------------------------
running = True
while running:
    clock.tick(60)




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                sound.play()
                sound.set_volume(0.4)

    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        pygame.draw.circle(ecran, (255, 0, 0), (x, y), 5)
        print(f"Click → X:{x} Y:{y}")


 

    # Déplacement et gravité
    joueur.deplacement(plateformes)
    joueur.appliquer_gravite(plateformes)


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
    ecran.blit(background, (bg_x, bg_y))


    # Plateformes
    for plat, img in zip(plateformes, platform_images):
        if img:
            ecran.blit(img, (plat.x - camera_x, plat.y - camera_y))
        else:
            pygame.draw.rect(ecran, (0, 200, 0),
                             (plat.x - camera_x, plat.y - camera_y, plat.width, plat.height))

    # Joueur
    ecran.blit(joueur.image, (joueur.rect.x - camera_x, joueur.rect.y - camera_y))

    pygame.display.flip()
    
pygame.quit()
