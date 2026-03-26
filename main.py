import pygame, sys, subprocess, time
from pathlib import Path
from pygame.display import flip
from sfx import musiquemenu, sfxboutton
import settings


pygame.init()
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))

# Icon
icon = pygame.image.load("images/logo.png").convert_alpha()
pygame.display.set_icon(icon)
# Titre
titre = pygame.image.load("images/titre.png").convert_alpha()
titre_rect = titre.get_rect(center=(width // 2, height // 2))
# BG
BG = pygame.image.load("images/fondmenu.jpeg").convert_alpha()
BG = pygame.transform.scale(BG, (1280, 720))
pygame.display.set_caption("Galileo 2D")
# Couleurs
Blanc = (255, 255, 255)
bleu_transparent = (0, 80, 200, 180)
bleu_selection = (0, 140, 255, 220)
shadow = (0, 0, 0)
# Parametres
parametre_gui = pygame.image.load("images/parametre.png").convert_alpha()
parametre_gui_rect = parametre_gui.get_rect(center=(width // 2, height // 2))
fermer = pygame.transform.scale(
    pygame.image.load("images/fermer_fenetre.png").convert_alpha(), (50, 50)
)
fermer_rect = fermer.get_rect(topleft=(1200, 30))

activer = pygame.transform.scale(
    pygame.image.load("images/activer.png").convert_alpha(), (150, 75)
)
activer2 = pygame.transform.scale(
    pygame.image.load("images/activer.png").convert_alpha(), (150, 75)
)
activer3 = pygame.transform.scale(
    pygame.image.load("images/activer.png").convert_alpha(), (150, 75)
)
desactiver = pygame.transform.scale(
    pygame.image.load("images/desactiver.png").convert_alpha(), (150, 75)
)
desactiver2 = pygame.transform.scale(
    pygame.image.load("images/desactiver.png").convert_alpha(), (150, 75)
)
desactiver3 = pygame.transform.scale(
    pygame.image.load("images/desactiver.png").convert_alpha(), (150, 75)
)

toggle_rect_1 = desactiver.get_rect(topleft=(100, 150))
toggle_rect_2 = desactiver2.get_rect(topleft=(100, 250))
toggle_rect_3 = desactiver3.get_rect(topleft=(100, 350))
SETTINGS_PATH = Path(__file__).with_name("settings.py")

# Polices d'ecritures
try:
    Police_titre = pygame.font.Font("asset/polices/Coolvetica Rg.otf", 72)
    Police_bouton = pygame.font.Font("asset/polices/Coolvetica Rg.otf", 36)
except:
    Police_titre = pygame.font.SysFont(None, 72)
    Police_bouton = pygame.font.SysFont(None, 36)

Police_parametre = pygame.font.Font("asset/polices/Coolvetica Rg.otf", 34)


def sauvegarder_settings():
    SETTINGS_PATH.write_text(
        "musique = " + str(settings.musique) + "\n"
        + "speedrun = " + str(settings.speedrun) + "\n"
        + "option_3 = " + str(settings.option_3) + "\n",
        encoding="utf-8",
    )


class Button:
    def __init__(self, text, center_y, action):
        self.text = text
        self.action = action
        self.center_y = center_y
        self.width, self.height = 320, 70
        self.rect = pygame.Rect((0, 0, self.width, self.height))
        self.rect.center = (width // 2, center_y)

    def draw(self, win, mouse_pos):
        is_hover = self.rect.collidepoint(mouse_pos)
        color = bleu_selection if is_hover else bleu_transparent
        button_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(
            button_surface, color, (0, 0, self.width, self.height), border_radius=16
        )
        win.blit(button_surface, self.rect)

        text_surf = Police_bouton.render(self.text, True, Blanc)
        text_rect = text_surf.get_rect(center=self.rect.center)
        win.blit(text_surf, text_rect)

    def is_clicked(self, mouse_pos, mouse_pressed):
        return self.rect.collidepoint(mouse_pos) and mouse_pressed[0]


# Logo
LOGO = pygame.image.load("images/logo.png").convert_alpha()
LOGO = pygame.transform.scale(LOGO, (300, 300))
logo_rect = LOGO.get_rect(center=(width // 2, 150))


# Listes des boutons
buttons = [
    Button("Jouer", 360, "play"),
    Button("Parametres", 440, "settings"),
    Button("Sauvegarde", 520, "code"),
    Button("Quitter", 600, "quit"),
]
# Musique et son
musique_menu = musiquemenu
son_bouton = sfxboutton

if settings.musique:
    musique_menu.play(-1, 0, 3000)
    musique_menu.set_volume(0.5)
else:
    musique_menu.set_volume(0)


def appliquer_parametre(param_name, enabled):
    if param_name == "musique":
        settings.musique = enabled
        if enabled:
            musique_menu.set_volume(0.5)
            if not musique_menu.get_num_channels():
                musique_menu.play(-1, 0, 3000)
        else:
            musique_menu.set_volume(0)
    elif param_name == "speedrun":
        settings.speedrun = enabled
    elif param_name == "option_3":
        settings.option_3 = enabled

    sauvegarder_settings()


parametres_toggles = [
    {
        "name": "musique",
        "enabled": settings.musique,
        "rect": toggle_rect_1,
        "image_on": activer,
        "image_off": desactiver,
    },
    {
        "name": "speedrun",
        "enabled": settings.speedrun,
        "rect": toggle_rect_2,
        "image_on": activer2,
        "image_off": desactiver2,
    },
    {
        "name": "option_3",
        "enabled": settings.option_3,
        "rect": toggle_rect_3,
        "image_on": activer3,
        "image_off": desactiver3,
    },
]

running = True
clock = pygame.time.Clock()
INTRO_DURATION = 4500
intro_start = pygame.time.get_ticks()
intro = True
afficher_parametres = False

while running:
    clock.tick(60)

    current_time = pygame.time.get_ticks()
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if intro:
                running = False
            else:
                afficher_parametres = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if intro and fermer_rect.collidepoint(event.pos):
                running = False
            elif afficher_parametres:
                if fermer_rect.collidepoint(event.pos):
                    afficher_parametres = False
                    son_bouton.play()
                else:
                    toggle_clicked = False
                    for parametre in parametres_toggles:
                        if parametre["rect"].collidepoint(event.pos):
                            parametre["enabled"] = not parametre["enabled"]
                            appliquer_parametre(parametre["name"], parametre["enabled"])
                            son_bouton.play()
                            toggle_clicked = True
                            break
                    if not toggle_clicked and not parametre_gui_rect.collidepoint(event.pos):
                        afficher_parametres = False

    if intro:
        screen.fill((0, 0, 0))
        screen.blit(titre, titre_rect)
        if current_time - intro_start >= INTRO_DURATION:
            intro = False
        pygame.display.flip()
        continue

    screen.fill((0, 0, 0))
    screen.blit(BG, (0, 0))
    screen.blit(BG, (0, 0))
    screen.blit(LOGO, logo_rect)

    for btn in buttons:
        btn.draw(screen, mouse_pos)
        if not afficher_parametres and btn.is_clicked(mouse_pos, mouse_pressed):
            pygame.time.delay(200)

            if btn.action == "play":
                print("nouvelle partie")
                son_bouton.play(0, 0, 0)
                son_bouton.set_volume(1.0)
                time.sleep(0.3)
                pygame.quit()
                subprocess.run(["python", "general.py"])
                sys.exit()
            elif btn.action == "code":
                son_bouton.play(0, 0, 0)
                son_bouton.set_volume(0.5)
                print("interface code")
                time.sleep(0.3)
                pygame.quit()
                subprocess.run(["python", "codesauv.py"])
                sys.exit()
            elif btn.action == "settings":
                son_bouton.play(0, 0, 0)
                son_bouton.set_volume(0.5)
                afficher_parametres = True
            elif btn.action == "quit":
                son_bouton.play(0, 0, 0)
                son_bouton.set_volume(0.5)
                time.sleep(0.3)
                running = False

    if afficher_parametres:
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))
        screen.blit(parametre_gui, parametre_gui_rect)
        screen.blit(fermer, fermer_rect)
        texte_musique = Police_parametre.render("musique", True, Blanc)
        texte_speedrun = Police_parametre.render("speedrun", True, Blanc)
        screen.blit(texte_musique, (270, 170))
        screen.blit(texte_speedrun, (270, 270))
        for parametre in parametres_toggles:
            image = parametre["image_on"] if parametre["enabled"] else parametre["image_off"]
            screen.blit(image, parametre["rect"])

    pygame.display.flip()

pygame.quit()
sys.exit()
