import pygame
import subprocess
import math
from joueur import Joueur
from niveau1 import get_plateforme_prison, get_plateformes, plateforme_pic, plateforme_pic2, get_sol, get_plateformeshaute, get_sol2
import sfx, random, sys
from sfx import sauter, sfxmarche1, sfxmarche2, sfxmarche3, tombersfx
import settings
from pathlib import Path
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

debug_hitboxes = False

death_animation_start = None
death_sound_stage = 0
DEATH_ANIMATION_SPEEDUP_MS = 300
DEATH_HEART_ON_PLAYER_MS = 1000
DEATH_HEART_TRAVEL_MS = 2000
DEATH_HEART_CENTER_HOLD_MS = 2200
DEATH_HAND_DELAY_MS = 3050
DEATH_HAND_ENTER_MS = 2000
DEATH_HAND_GRAB_MS = 500
DEATH_HAND_EXIT_MS = 1700
DEATH_SATAN_ENTER_MS = 1200
DEATH_GAME_OVER_DELAY_MS = (
    DEATH_HEART_ON_PLAYER_MS
    + DEATH_HEART_TRAVEL_MS
    + DEATH_HEART_CENTER_HOLD_MS
    + DEATH_HAND_GRAB_MS
    + DEATH_HAND_EXIT_MS
    + DEATH_SATAN_ENTER_MS
    + 4000
    - DEATH_ANIMATION_SPEEDUP_MS
)
titre_logo = pygame.image.load("images/titre.png").convert_alpha()
titre_rect = titre_logo.get_rect(midtop=(screen_width // 2, 100))

vies = 3
# NIVEAU 1 ET 2
niveau1 = pygame.Rect(0,0,2000,4000)
niveau2 = pygame.Rect(2000,0,2000,4000)

# --- SPEEDRUN TIMER ---
speedrun = settings.speedrun
speedrun_started = False
speedrun_start_time = 0
speedrun_elapsed = 0
speedrun_pause_start = None
# --- SPEEDRUN BLOCK
speedrun_finish_rect = pygame.Rect(1875,1240, 80, 200)
speedrun_finished = False
speedrun_final_time = 0

def ajouter_vie():
    global vies
    if vies < 3:
        vies += 1
        sfx.viesfx.play()
# Porte de l'enfer
porte = pygame.image.load("images/porte_enfer.png").convert_alpha()
porte = pygame.transform.scale(porte, (380, 530)) 
porte_rect = porte.get_rect(topleft=(300, 320))

def mettre_speedrun_en_pause(temps_actuel):
    global speedrun_pause_start
    if speedrun and speedrun_started and not speedrun_finished and speedrun_pause_start is None:
        speedrun_pause_start = temps_actuel

def reprendre_speedrun_apres_pause(temps_actuel):
    global speedrun_start_time, speedrun_pause_start
    if speedrun_pause_start is None:
        return
    speedrun_start_time += temps_actuel - speedrun_pause_start
    speedrun_pause_start = None

def couper_sons_pour_mort():
    # Coupe tous les sons du jeu pour laisser uniquement ceux de la sequence de mort.
    for son in (
        ambient, sfx.degat, sfx.viesfx, sfx.sfxdialogue, sfx.fin, sfx.liresfx, sfx.stoplire,
        sfx.ouvrir_inv, sfx.fermer_inv, sfx.selectsfx, sfx.pausesfxouvrir, sfx.pausesfxfermer,
        sfx.pausesfxbutton, sfx.sfxnpc, sfx.dialogue_csfx, sfxmarche1, sfxmarche2, sfxmarche3,
        sauter, tombersfx
    ):
        son.stop()

# --- PARAMETRES ---
SETTINGS_PATH = Path(__file__).with_name("settings.py")

def sauvegarder_settings():
    SETTINGS_PATH.write_text(
        "musique = " + str(settings.musique) + "\n"
        + "speedrun = " + str(settings.speedrun) + "\n"
        + "option_3 = " + str(settings.option_3) + "\n",
        encoding="utf-8",
    )

def appliquer_parametre_jeu(param_name, enabled):
    if param_name == "musique":
        settings.musique = enabled
        if enabled:
            ambient.set_volume(0.2)
        else:
            ambient.set_volume(0)
    elif param_name == "speedrun":
        settings.speedrun = enabled
    elif param_name == "option_3":
        settings.option_3 = enabled
        vol = 0 if not enabled else 1.0
        sfx.viesfx.set_volume(vol)
        sfx.sfxdialogue.set_volume(0.5 if enabled else 0)
        sfx.fin.set_volume(0.5 if enabled else 0)
        sfx.liresfx.set_volume(0.5 if enabled else 0)
        sfx.stoplire.set_volume(0.5 if enabled else 0)
        sfx.ouvrir_inv.set_volume(vol)
        sfx.fermer_inv.set_volume(vol)
        sfx.selectsfx.set_volume(vol)
        sfx.pausesfxouvrir.set_volume(vol)
        sfx.pausesfxfermer.set_volume(vol)
        sfx.pausesfxbutton.set_volume(vol)
        sfx.sfxnpc.set_volume(0.1 if enabled else 0)
        sfx.dialogue_csfx.set_volume(vol)
        sfx.degat.set_volume(vol)
        sfx.mortsfx.set_volume(vol)
        sfx.satan.set_volume(vol)
        sfxmarche1.set_volume(vol)
        sfxmarche2.set_volume(vol)
        sfxmarche3.set_volume(vol)
        sauter.set_volume(0.2 if enabled else 0)
        for s in [sfxmarche1, sfxmarche2, sfxmarche3]:
            s.set_volume(0.5 if enabled else 0)

        
    sauvegarder_settings()

chute_y = 7000
zoom_factor = 3
camera_y_offset = -100

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

# SystÃ¨me d'invincibilité
invincible          = False
invincibilite_temps = 0
duree_invincibilite = 2000

# TITRE DEBUT DE JEU
dialogue_sfx = sfx.sfxdialogue
dialogue_sfx.set_volume(0.5)
titre       = "L'Enfer"
titre_index = 0
titre_fin   = 0


# Pancarte
panneau = pygame.image.load("images/panneau.png").convert_alpha()
panneau = pygame.transform.scale(panneau, (96, 150))
panneau_rect = panneau.get_rect()
panneau_rect.topleft = (800, 6150)
pancarte_active        = False
panneau_button_hidden  = False
panneau_button_timer   = 0
pancarte = pygame.transform.scale(pygame.image.load("images/pancarte.png").convert_alpha(), (850, 500))
lire_pancarte          = False
pancarte_timer         = 0
show_button_e_pancarte = False
liresfx                = sfx.liresfx
stoplire               = sfx.stoplire
stoplire.set_volume(0.5)
liresfx.set_volume(0.5)

# --- INVENTAIRE ---
frame_inventaire           = pygame.transform.scale(pygame.image.load("images/frame_inventaire.png").convert_alpha(), (80, 80))
objet_dans_inventaire      = False
bottes                     = pygame.transform.scale(pygame.image.load("images/botte.png").convert_alpha(), (80, 80))
bottes_dans_inventaire     = False
potion_vie_dans_inventaire = False
potion_vie                 = pygame.transform.scale(pygame.image.load("images/potion_vie.png").convert_alpha(), (100, 100))
icone_inventaire           = pygame.transform.scale(pygame.image.load("images/icone_inventaire.png").convert_alpha(), (100, 100))
inventaire_img             = pygame.transform.scale(pygame.image.load("images/inventaire.png").convert_alpha(), (560, 630))
inventaire_affiche         = False
inventaire_timer           = 0
show_button_f_inventaire   = False
ouvrir_inv = sfx.ouvrir_inv
fermer_inv = sfx.fermer_inv
select     = sfx.selectsfx
pause_ouvrir_sfx = sfx.pausesfxouvrir
pause_fermer_sfx = sfx.pausesfxfermer
pause_button_sfx = sfx.pausesfxbutton
inventaire_vide_text       = police.render("Vous n'avez rien dans", True, "#7a371b")
inventaire_vide_text2      = police.render("votre inventaire !", True, "#7a371b")
lettre_f                   = police.render("F", True, "#ffffff")
# Ã‰quipement bottes
bottes_equipees        = False
tooltip_bottes_visible = False

# Bruit/sfx dialogue de npc
npcsfx = sfx.sfxnpc
npcsfx.set_volume(0.1)
# NPC 1  Giordano (animation 3 frames)
giordano  = pygame.transform.scale(pygame.image.load("images/giordano.png").convert_alpha(),  (160, 105))
giordano2 = pygame.transform.scale(pygame.image.load("images/giordano2.png").convert_alpha(), (160, 105))
giordano3 = pygame.transform.scale(pygame.image.load("images/giordano3.png").convert_alpha(), (160, 105))
giordano_images      = [giordano, giordano2, giordano3]
current_giordano     = 0
giordano_anim_timer  = 0
giordano_forward     = True
giordano_pause       = False
giordano_pause_timer = 0

giordano_rect = giordano.get_rect()
giordano_rect.topleft = (1600, 6190)

bouton_e      = pygame.image.load("images/bouton_e.png").convert_alpha()
bouton_e_rect = bouton_e.get_rect(topleft=(1600, 6150))
bouton_e      = pygame.transform.scale(bouton_e, (50, 50))
bouton_f      = pygame.image.load("images/bouton_f.png").convert_alpha()
bouton_f      = pygame.transform.scale(bouton_f, (50, 50))
dialogue_g    = False
cadre_g       = pygame.image.load("images/cadre_dialogue1.png").convert_alpha()
cadre_g_rect  = cadre_g.get_rect(center=(640, 550))
messages      = ["GALILEO !!", "C'EST UN ENFER !"]

# Animation fin
coeurt_mort = pygame.transform.scale(pygame.image.load("images/animation_fin/coeur_mort.png").convert_alpha(), (60, 60))
main1 = pygame.transform.scale(pygame.image.load("images/animation_fin/main1.png").convert_alpha(), (1300, 600))
main2 = pygame.transform.scale(pygame.image.load("images/animation_fin/main2.png").convert_alpha(), (1300, 600))
satan1 = pygame.transform.scale(pygame.image.load("images/animation_fin/satan1.png").convert_alpha(), (1300, 600))
satan1.set_colorkey((0, 0, 0))
satan2 = pygame.transform.scale(pygame.image.load("images/animation_fin/satan2.png").convert_alpha(), (1300, 600))
satan2.set_colorkey((0, 0, 0))

coeursfx = sfx.coeursfx
mortsfx = sfx.mortsfx
mortsfx.set_volume(1.0 if settings.option_3 else 0)


# --- Cooldowns NPC ---
giordano_cooldown = -30000
virgilio_cooldown = -30000
duree_cooldown    = 30000
giordano_dialogue_cooldown = -3000
virgilio_dialogue_cooldown = -3000
condamne1_dialogue_cooldown = -3000
duree_dialogue_cooldown = 3000

# NPC 2  Virgilio
virgilio      = pygame.transform.scale(pygame.image.load("images/virgilio.png").convert_alpha(), (60, 120))
virgilio_rect = virgilio.get_rect()
virgilio_rect.topleft = (700, 4080)
dialogue_v    = False
cadre_v       = pygame.image.load("images/cadre_dialogue2.png").convert_alpha()
cadre_v_rect  = cadre_v.get_rect(center=(640, 550))

counter         = 0
speed           = 5
active_message  = 0
message         = messages[active_message]
done            = False
message_v       = ["Salut Giordano !", "Fais attention car les plateformes deviennent hautes !","Prends ces bottes pour sauter deux fois."]
active_message2 = 0
message2        = message_v[active_message2]

# NPC 3 -- Condamnés
condamnesfx = sfx.dialogue_csfx
condamne1 = pygame.transform.scale(pygame.image.load("images/condamne1.png").convert_alpha(), (112, 112))
condamne1_rect = condamne1.get_rect()
condamne1_rect.topleft = (300, 5737)
dialogue_c1 = False
cadre_c1 = pygame.image.load("images/cadre_dialogue_c1.png").convert_alpha()
cadre_c1_rect  = cadre_c1.get_rect(center=(640, 550))

message_c1 = ["...", "...", "Aide mo-", "...", "*ne bouge plus*"]
active_message_c1 = 0
message3 = message_c1[active_message_c1]

# MURS
plateformes_haute = get_plateformeshaute()

# Music
pygame.mixer.init(44100)
ambient = sfx.musiquefond
if settings.musique:
    ambient.set_volume(0.2)
    ambient.play(-1)
else:
    ambient.set_volume(0)

# Appliquer sfx au démarrage
if not settings.option_3:
    _vol = 0
    sfx.viesfx.set_volume(_vol)
    sfx.sfxdialogue.set_volume(_vol)
    sfx.fin.set_volume(_vol)
    sfx.liresfx.set_volume(_vol)
    sfx.stoplire.set_volume(_vol)
    sfx.ouvrir_inv.set_volume(_vol)
    sfx.fermer_inv.set_volume(_vol)
    sfx.selectsfx.set_volume(_vol)
    sfx.pausesfxouvrir.set_volume(_vol)
    sfx.pausesfxfermer.set_volume(_vol)
    sfx.pausesfxbutton.set_volume(_vol)
    sfx.sfxnpc.set_volume(_vol)
    sfx.dialogue_csfx.set_volume(_vol)
    sfx.degat.set_volume(_vol)
    sfx.mortsfx.set_volume(_vol)
    sfx.satan.set_volume(_vol)

# Plateformes
plateformes_prison = get_plateforme_prison()
plateformes_niveau = get_plateformes()
plateformes        = plateformes_niveau
sol                = get_sol()
niveau_largeur     = 4000
sol2 = get_sol2()

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

sol2_image_orig = pygame.image.load("images/sol_niveau2.png").convert_alpha()
sol2_images = []
for s in sol2:
    img = pygame.transform.scale(sol2_image_orig, (s.width, s.height))
    sol2_images.append(img)

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

# ---- Variables pour la transition quand on recommence le niveau
# Transition recommencer
transition_recommencer = False
transition_start = 0
transition_duree_fondu = 500   # ms pour devenir noir
transition_pause_noire = 2000   # ms d'attente écran noir avant reset
transition_porte_enfer_start = 0
transition_porte_teleporte = False
# Pause
en_pause = False
police_pause  = pygame.font.Font("asset/polices/Dungeon Depths.otf", 80)
police_bouton = pygame.font.Font("asset/polices/ari-w9500-bold.ttf", 32)

boutons_pause = [
    {"texte": "Reprendre",  "action": "reprendre"},
    {"texte": "Recommencer",  "action": "recommencer"},
    {"texte": "Menu",       "action": "menu"},
    {"texte": "Parametres", "action": "parametres"},
    {"texte": "Quitter",    "action": "quitter"},
]
pause_selected    = 0
pause_hover_index = -1
pause_button_width  = 280
pause_button_height = 56

# --- Menu paramÃ¨tres en pause ---
afficher_parametres_pause = False
parametre_gui_pause  = pygame.transform.scale(pygame.image.load("images/parametre.png").convert_alpha(), (screen_width, screen_height))
parametre_gui_rect_p = parametre_gui_pause.get_rect(center=(screen_width // 2, screen_height // 2))
fermer_pause         = pygame.transform.scale(pygame.image.load("images/fermer_fenetre.png").convert_alpha(), (50, 50))
fermer_pause_rect    = fermer_pause.get_rect(topleft=(1200, 30))
activer_p            = pygame.transform.scale(pygame.image.load("images/activer.png").convert_alpha(), (150, 75))
desactiver_p         = pygame.transform.scale(pygame.image.load("images/desactiver.png").convert_alpha(), (150, 75))
police_param_pause   = pygame.font.Font("asset/polices/ari-w9500-bold.ttf", 34)
parametres_toggles_pause = [
    {"name": "musique",  "enabled": settings.musique,  "rect": pygame.Rect(100, 150, 150, 75)},
    {"name": "speedrun", "enabled": settings.speedrun, "rect": pygame.Rect(100, 250, 150, 75)},
    {"name": "option_3", "enabled": settings.option_3, "rect": pygame.Rect(100, 350, 150, 75)},
]

# Sert comme reset de progression quand le joueur veut
# recommencer la partie
def reset():
    global vies, etat, invincible, invincibilite_temps
    global death_animation_start, death_sound_stage
    global speedrun, speedrun_started, speedrun_start_time, speedrun_elapsed, speedrun_pause_start, speedrun_finished, speedrun_final_time
    global dialogue_g, dialogue_v, dialogue_c1
    global active_message, active_message2, active_message_c1
    global message, message2, message3
    global counter, done
    global giordano_cooldown, virgilio_cooldown
    global giordano_dialogue_cooldown, virgilio_dialogue_cooldown, condamne1_dialogue_cooldown
    global objet_dans_inventaire, bottes_dans_inventaire, bottes_equipees, tooltip_bottes_visible
    global inventaire_affiche, lire_pancarte, pancarte_active, panneau_button_hidden
    global titre_index, titre_fin
    global en_pause, afficher_parametres_pause
    global transition_porte_teleporte
    tombersfx.stop()
    sfx.mortsfx.stop()
    sfx.coeursfx.stop()
    sfx.coeurmort.stop()
    sfx.satan.stop()
    tombersfx.set_volume(0)
    joueur.en_chute = False
    joueur.chute_son_joue = False
    joueur.chute_fadeout = False

    vies = 3
    etat = "jeu"
    death_animation_start = None
    death_sound_stage = 0
    invincible = False
    invincibilite_temps = 0

    speedrun = settings.speedrun
    speedrun_started = False
    speedrun_start_time = 0
    speedrun_elapsed = 0
    speedrun_pause_start = None
    speedrun_finished = False
    speedrun_final_time = 0

    dialogue_g = False
    dialogue_v = False
    dialogue_c1 = False
    active_message = 0
    active_message2 = 0
    active_message_c1 = 0
    message = messages[0]
    message2 = message_v[0]
    message3 = message_c1[0]
    counter = 0
    done = False

    giordano_cooldown = -30000
    virgilio_cooldown = -30000
    giordano_dialogue_cooldown = -3000
    virgilio_dialogue_cooldown = -3000
    condamne1_dialogue_cooldown = -3000

    objet_dans_inventaire = False
    bottes_dans_inventaire = False
    bottes_equipees = False
    tooltip_bottes_visible = False
    inventaire_affiche = False
    lire_pancarte = False
    pancarte_active = False
    panneau_button_hidden = False

    titre_index = 0
    titre_fin = 0

    en_pause = False
    afficher_parametres_pause = False

    joueur.rect.center = (100, 6299)
    joueur.vel_y = 0
    joueur.vx = 0
    joueur.nb_sauts = 0
    joueur.double_saut = False
    joueur.au_sol = False
    joueur.double_jump_effects = []
    joueur.peut_bouger = True
    joueur.en_chute = False
    joueur.chute_son_joue = False
    joueur.facing_left = False

    pygame.mixer.unpause()

# -------------------------------------------------------------------------------------------------#
# Boucle principale
# -------------------------------------------------------------------------------------------------#
running = True
jump_key_held = False
ground_jump_consumed = False
while running:
    clock.tick(60)
    current_time  = pygame.time.get_ticks()
    button_offset = int(math.sin(current_time * 0.01) * 3)
    active_porte = joueur.rect.colliderect(porte_rect)

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

    # ---- Ã‰vÃ¨nements ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if transition_recommencer or transition_porte_enfer_start:
            continue

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if joueur.peut_bouger and joueur.double_saut and joueur.nb_sauts == 1 and not jump_key_held:
                    jump_key_held = True
                    joueur.vel_y = joueur.jump_force
                    joueur.nb_sauts = 2
                    sauter.play()
                    joueur.timer_chute = pygame.time.get_ticks()
                    joueur.chute_son_joue = False
                    tombersfx.stop()
                    tombersfx.set_volume(0)
                    joueur.double_jump_effects.append({
                        'x': joueur.rect.centerx,
                        'y': joueur.rect.y + 150,
                        'alpha': 255,
                        'width': 120,
                        'height': 7
                    })
            if event.key == pygame.K_ESCAPE:
                if afficher_parametres_pause:
                    # Ferme les paramÃ¨tres, retour au menu pause
                    afficher_parametres_pause = False
                    pause_button_sfx.play()
                else:
                    en_pause = not en_pause
                    joueur.peut_bouger = not (en_pause or lire_pancarte or inventaire_affiche or dialogue_g or dialogue_v or dialogue_c1)
                    if en_pause:
                        mettre_speedrun_en_pause(current_time)
                        joueur.mettre_en_pause(current_time)
                        pause_ouvrir_sfx.play()
                        pygame.mixer.pause()
                        pause_hover_index = pause_selected
                    else:
                        reprendre_speedrun_apres_pause(current_time)
                        joueur.reprendre_apres_pause(current_time)
                        pygame.mixer.unpause()
                        pause_fermer_sfx.play()

            if en_pause and not afficher_parametres_pause:
                if event.key == pygame.K_DOWN:
                    ancien_pause_selected = pause_selected
                    pause_selected = (pause_selected + 1) % len(boutons_pause)
                    if pause_selected != ancien_pause_selected:
                        pause_button_sfx.play()
                        pause_hover_index = pause_selected
                if event.key == pygame.K_UP:
                    ancien_pause_selected = pause_selected
                    pause_selected = (pause_selected - 1) % len(boutons_pause)
                    if pause_selected != ancien_pause_selected:
                        pause_button_sfx.play()
                        pause_hover_index = pause_selected
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    action = boutons_pause[pause_selected]["action"]
                    if action == "reprendre":
                        en_pause = False
                        joueur.peut_bouger = not (lire_pancarte or inventaire_affiche or dialogue_g or dialogue_v or dialogue_c1)
                        reprendre_speedrun_apres_pause(current_time)
                        joueur.reprendre_apres_pause(current_time)
                        pygame.mixer.unpause()
                        pause_fermer_sfx.play()
                    elif action == "menu":
                        pygame.quit()
                        subprocess.run(['python', 'main.py'])
                        running = False
                    elif action == "quitter":
                        running = False
                    elif action == "parametres":
                        afficher_parametres_pause = True
                        pause_button_sfx.play()
                    elif action == "recommencer":
                        transition_recommencer = True
                        transition_start = current_time
                        pause_button_sfx.play()
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            jump_key_held = False
        if event.type not in (pygame.KEYDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            continue
        if event.type == pygame.KEYDOWN and en_pause:
            continue
        if event.type == pygame.KEYDOWN and inventaire_affiche and event.key != pygame.K_f:
            continue
        if event.type == pygame.KEYDOWN:
            #---Giordano
            if event.key == pygame.K_e and dialogue_g:
                if not done:
                    counter = speed * len(message)
                    npcsfx.stop()
                else:
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
                        giordano_dialogue_cooldown = current_time
                        if current_time - giordano_cooldown > duree_cooldown:
                            giordano_cooldown = current_time
                            ajouter_vie()
            elif event.key == pygame.K_e and active and not dialogue_g:
                if current_time - giordano_dialogue_cooldown > duree_dialogue_cooldown:
                    dialogue_g = True
                    joueur.peut_bouger = False
                    counter = 0
                    active_message = 0
                    message = messages[0]
            #---Virgilio
            elif event.key == pygame.K_e and dialogue_v:
                if not done:
                    counter = speed * len(message2)
                    npcsfx.stop()
                else:
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
                        virgilio_dialogue_cooldown = current_time
                        objet_dans_inventaire = True
                        bottes_dans_inventaire = True
                        if current_time - virgilio_cooldown > duree_cooldown:
                            virgilio_cooldown = current_time
                            ajouter_vie()
            elif event.key == pygame.K_e and active2 and not dialogue_v:
                if current_time - virgilio_dialogue_cooldown > duree_dialogue_cooldown:
                    dialogue_v = True
                    joueur.peut_bouger = False
                    counter = 0
                    active_message2 = 0
                    message2 = message_v[0]
            #---Condamné 1
            elif event.key == pygame.K_e and dialogue_c1:
                if not done:
                    counter = speed * len(message3)
                    condamnesfx.stop()
                else:
                    if active_message_c1 < len(message_c1) - 1:
                        active_message_c1 += 1
                        message3 = message_c1[active_message_c1]
                        counter = 0
                        done = False
                    else:
                        dialogue_c1 = False
                        done = False
                        active_message_c1 = 0
                        counter = 0
                        joueur.peut_bouger = True
                        condamne1_dialogue_cooldown = current_time
            elif event.key == pygame.K_e and active3 and not dialogue_c1:
                if current_time - condamne1_dialogue_cooldown > duree_dialogue_cooldown:
                    dialogue_c1 = True
                    joueur.peut_bouger = False
                    counter = 0
                    active_message_c1 = 0
                    message3 = message_c1[0]
            elif event.key == pygame.K_e and pancarte_active and not lire_pancarte:
                lire_pancarte = True
                joueur.peut_bouger = False
                pancarte_timer = current_time
                if titre_index >= speed * len(titre) and titre_fin == 0:
                    titre_fin = current_time
                liresfx.play()
            elif event.key == pygame.K_e and show_button_e_pancarte:
                lire_pancarte = False
                show_button_e_pancarte = False
                joueur.peut_bouger = True
                panneau_button_hidden = True
                panneau_button_timer = current_time
                stoplire.play()
            elif event.key == pygame.K_e and active_porte:
                transition_porte_enfer_start = current_time
                joueur.peut_bouger = False
            elif event.key == pygame.K_f and not inventaire_affiche and not lire_pancarte and not dialogue_g and not dialogue_v and not dialogue_c1:
                ouvrir_inv.play()
                inventaire_affiche = True
                joueur.peut_bouger = False
                inventaire_timer = current_time
                show_button_f_inventaire = False
            elif event.key == pygame.K_f and inventaire_affiche:
                fermer_inv.play()
                inventaire_affiche = False
                show_button_f_inventaire = False
                tooltip_bottes_visible = False
                joueur.peut_bouger = True

        if event.type == pygame.MOUSEMOTION and en_pause and not afficher_parametres_pause:
            mx, my = event.pos
            for i, bouton in enumerate(boutons_pause):
                y_bouton = 280 + i * 80
                x_bouton = screen_width // 2 - pause_button_width // 2
                rect_bouton = pygame.Rect(x_bouton, y_bouton, pause_button_width, pause_button_height)
                if rect_bouton.collidepoint(mx, my):
                    if pause_hover_index != i:
                        pause_button_sfx.play()
                    pause_selected = i
                    pause_hover_index = i

        if event.type == pygame.MOUSEBUTTONDOWN:
            if afficher_parametres_pause:
                if fermer_pause_rect.collidepoint(event.pos):
                    afficher_parametres_pause = False
                    pause_button_sfx.play()
                else:
                    for parametre in parametres_toggles_pause:
                        if parametre["rect"].collidepoint(event.pos):
                            parametre["enabled"] = not parametre["enabled"]
                            appliquer_parametre_jeu(parametre["name"], parametre["enabled"])
                            pause_button_sfx.play()
                            break
            elif en_pause:
                mx, my = event.pos
                for i, bouton in enumerate(boutons_pause):
                    y_bouton = 280 + i * 80
                    x_bouton = screen_width // 2 - pause_button_width // 2
                    rect_bouton = pygame.Rect(x_bouton, y_bouton, pause_button_width, pause_button_height)
                    if rect_bouton.collidepoint(mx, my):
                        action = bouton["action"]
                        if action == "reprendre":
                            en_pause = False
                            joueur.peut_bouger = not (lire_pancarte or inventaire_affiche or dialogue_g or dialogue_v or dialogue_c1)
                            reprendre_speedrun_apres_pause(current_time)
                            joueur.reprendre_apres_pause(current_time)
                            pygame.mixer.unpause()
                            pause_fermer_sfx.play()
                        elif action == "menu":
                            pygame.quit()
                            subprocess.run(['python', 'main.py'])
                            running = False
                        elif action == "quitter":
                            running = False
                        elif action == "parametres":
                            afficher_parametres_pause = True
                            pause_button_sfx.play()
                        elif action == "recommencer":
                            transition_recommencer = True
                            transition_start = current_time
                            pause_button_sfx.play()
            else:
                if inventaire_affiche and bottes_dans_inventaire:
                    bottes_rect_inv = pygame.Rect(400, 250, 80, 80)
                    if bottes_rect_inv.collidepoint(event.pos):
                        select.play()
                        tooltip_bottes_visible = not tooltip_bottes_visible
                if inventaire_affiche and tooltip_bottes_visible:
                    tooltip_equiper_rect = pygame.Rect(490, 250, 130, 40)
                    if tooltip_equiper_rect.collidepoint(event.pos):
                        select.play()
                        if bottes_equipees:
                            joueur.double_saut = False
                            bottes_equipees = False
                        else:
                            joueur.double_saut = True
                            bottes_equipees = True
                        tooltip_bottes_visible = False

    keys = pygame.key.get_pressed()

    # ---- Touches maintenues ----
    if not transition_recommencer and not transition_porte_enfer_start:
        if not joueur.peut_bouger:
            joueur.is_animating = False
            joueur.vx = 0
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            joueur.is_animating = True
            joueur.facing_left  = False
            if speedrun and not speedrun_started:
                speedrun_started = True
                speedrun_start_time = current_time
        elif keys[pygame.K_q] or keys[pygame.K_LEFT]:
            joueur.is_animating = True
            joueur.facing_left  = True
            if speedrun and not speedrun_started:
                speedrun_started = True
                speedrun_start_time = current_time
        else:
            joueur.is_animating = False

    if joueur.peut_bouger and joueur.est_au_sol(plateformes + plateformes_prison + sol):
        if keys[pygame.K_SPACE] and not ground_jump_consumed:
            ground_jump_consumed = True
            jump_key_held = True
            joueur.vel_y = joueur.jump_force
            joueur.nb_sauts = 1
            sauter.play()
        elif not keys[pygame.K_SPACE]:
            ground_jump_consumed = False
            jump_key_held = False
    else:
        ground_jump_consumed = False

    # ---- Timers ----
    if inventaire_affiche and not show_button_f_inventaire:
        show_button_f_inventaire = True

    if lire_pancarte and not show_button_e_pancarte and current_time - pancarte_timer > 3000:
        show_button_e_pancarte = True

    if panneau_button_hidden and current_time - panneau_button_timer > 2000:
        panneau_button_hidden = False

    # ---- Physique ----
    if not en_pause and not transition_recommencer and not transition_porte_enfer_start and etat != "mort":
        joueur.deplacement(plateformes + plateformes_prison + sol + sol2)
        joueur.appliquer_gravite(plateformes + plateformes_prison + sol + sol2, murs=plateformes_haute)
        joueur.update_double_jump_effects()

        if not invincible:
            for plat_danger in plateformes_danger + plateformes_danger2:
                if joueur.rect.colliderect(plat_danger):
                    vies -= 1
                    sfx.degat.play()
                    invincible = True
                    invincibilite_temps = current_time
                    if vies <= 0:
                        etat = "mort"
                        death_animation_start = current_time
                        death_sound_stage = 0
                        joueur.peut_bouger = False
                        joueur.is_animating = False
                        couper_sons_pour_mort()
                        break

        if invincible and current_time - invincibilite_temps > duree_invincibilite:
            invincible = False

        if joueur.rect.top > chute_y:
            vies = 0
            etat = "mort"
            death_animation_start = current_time
            death_sound_stage = 0
            joueur.peut_bouger = False
            joueur.is_animating = False
            couper_sons_pour_mort()

    if speedrun and speedrun_started and not speedrun_finished:
        if joueur.rect.colliderect(speedrun_finish_rect):
            speedrun_finished = True
            speedrun_final_time = speedrun_elapsed

    if etat == "mort" and death_animation_start is not None:
        if current_time - death_animation_start >= DEATH_GAME_OVER_DELAY_MS:
            etat = "game_over"

    if etat == "game_over":
        pygame.quit()
        subprocess.run(['python', 'menu_de_fin.py'])
        running = False
        break

    # ---- Caméra ----
    camera_x = joueur.rect.centerx - screen_width // 2
    if joueur.rect.centerx < 2000:
        camera_x = max(0, min(camera_x, 2000 - screen_width))
    else:
        camera_x = max(2000, min(camera_x, 4000 - screen_width))
    camera_y = joueur.rect.centery - screen_height // 2 + camera_y_offset
    camera_y = max(0, camera_y)

    if joueur.rect.centerx >= 2000:
        bg_x = -(camera_x - 2000) * parallax_factor + bg_offset_x - bg_width // 2
    else:
        bg_x = -camera_x * parallax_factor + bg_offset_x
    bg_y = -camera_y * parallax_factor + bg_offset_y

    if etat == "mort":
        death_elapsed = current_time - death_animation_start
        heart_travel_end = DEATH_HEART_ON_PLAYER_MS + DEATH_HEART_TRAVEL_MS
        heart_hold_end = heart_travel_end + DEATH_HEART_CENTER_HOLD_MS - DEATH_ANIMATION_SPEEDUP_MS
        hand_grab_end = heart_hold_end + DEATH_HAND_GRAB_MS
        satan_enter_start = hand_grab_end + DEATH_HAND_EXIT_MS
        # Joue chaque son de la sequence de mort une seule fois.
        if death_sound_stage == 0:
            mortsfx.play()
            death_sound_stage = 1
        elif death_sound_stage == 1 and death_elapsed >= heart_travel_end:
            coeursfx.play()
            death_sound_stage = 2
        screen.fill((0, 0, 0))
        # Mort: coeur sur le joueur, trajet vers le centre, pause, puis main depuis la droite.

        if death_elapsed < DEATH_HEART_ON_PLAYER_MS:
            screen.blit(
                coeurt_mort,
                coeurt_mort.get_rect(center=(joueur.rect.centerx - camera_x, joueur.rect.centery - camera_y))
            )
        elif death_elapsed < heart_travel_end:
            t = min((death_elapsed - DEATH_HEART_ON_PLAYER_MS) / DEATH_HEART_TRAVEL_MS, 1)
            # Courbe douce avec une sortie lente, proche d'un ease-out type Bezier.
            t = 1 - (1 - t) ** 3
            screen.blit(
                coeurt_mort,
                coeurt_mort.get_rect(
                    center=(
                        (joueur.rect.centerx - camera_x) + ((screen_width // 2) - (joueur.rect.centerx - camera_x)) * t,
                        (joueur.rect.centery - camera_y) + ((screen_height // 2) - (joueur.rect.centery - camera_y)) * t,
                        )
                )
            )
        elif death_elapsed < heart_hold_end:
            screen.blit(
                coeurt_mort,
                coeurt_mort.get_rect(center=(screen_width // 2, screen_height // 2))
            )

        if death_elapsed >= DEATH_HAND_DELAY_MS:
            # La main entre, change d'image, attend un peu, puis repart avec un depart doux.
            if death_elapsed < heart_hold_end:

                screen.blit(
                    main1,
                    main1.get_rect(
                        center=(
                            (screen_width + main1.get_width() // 2)
                            + ((screen_width // 2) - (screen_width + main1.get_width() // 2)) * (1 - (1 - min((death_elapsed - DEATH_HAND_DELAY_MS) / DEATH_HAND_ENTER_MS, 1)) ** 3),
                            screen_height // 2 - 50,
                        )
                    )
                )
            elif death_elapsed < hand_grab_end:
                if death_sound_stage == 2:
                    sfx.coeursfx.stop()
                    sfx.coeurmort.set_volume(1.0)
                    sfx.coeurmort.play()
                    death_sound_stage = 3
                screen.blit(
                    main2,
                    main2.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
                )
            else:
                screen.blit(
                    main2,
                    main2.get_rect(
                        center=(
                            (screen_width // 2)
                            + ((screen_width + main2.get_width() // 2) - (screen_width // 2)) * min((death_elapsed - hand_grab_end) / DEATH_HAND_EXIT_MS, 1) ** 3,
                            screen_height // 2 - 50,
                        )
                    )
                )
                if death_elapsed >= satan_enter_start:
                    t = min((death_elapsed - satan_enter_start) / DEATH_SATAN_ENTER_MS, 1)
                    t = 1 - (1 - t) ** 3
                    img = satan1
                    if death_elapsed >= satan_enter_start + DEATH_SATAN_ENTER_MS:
                        if death_sound_stage == 3:
                            sfx.satan.set_volume(1.0)
                            sfx.satan.play()
                            death_sound_stage = 4
                        img = satan1 if ((death_elapsed - satan_enter_start - DEATH_SATAN_ENTER_MS) // 120) % 2 == 0 else satan2
                    screen.blit(
                        img,
                        img.get_rect(
                            center=(
                                screen_width // 2,
                                (-img.get_height() // 2) + (220 + img.get_height() // 2) * t - (15 if img == satan2 else 0),
                            )
                        )
                    )
        pygame.display.flip()
        continue

    # ========================
    # RENDU
    # ========================
    screen.blit(background, (bg_x, bg_y + 100))
    screen.blit(porte, (porte_rect.x - camera_x, porte_rect.y - camera_y))
    screen.blit(panneau, (panneau_rect.x - camera_x, panneau_rect.y - camera_y))
    screen.blit(giordano_images[current_giordano], (giordano_rect.x - camera_x, giordano_rect.y - camera_y))
    screen.blit(virgilio, (virgilio_rect.x - camera_x, virgilio_rect.y - camera_y))
    screen.blit(condamne1, (condamne1_rect.x - camera_x, condamne1_rect.y - camera_y))


    # Joueur
    afficher_joueur = True
    if invincible:
        afficher_joueur = (current_time // 100) % 2 == 0
    if afficher_joueur:
        sprite_offset_x = joueur.draw_offset_x_left if joueur.facing_left else joueur.draw_offset_x
        sprite_x = joueur.rect.centerx - camera_x - joueur.image.get_width() // 2 + sprite_offset_x
        sprite_y = joueur.rect.bottom - camera_y - joueur.image.get_height() + joueur.draw_offset_y
        screen.blit(joueur.image, (sprite_x, sprite_y))



    # Murs prison
    for mur, img in zip(plateformes_prison, mur_prison_images):
        screen.blit(img, (mur.x - camera_x, mur.y - camera_y))
    if debug_hitboxes:
        for mur in plateformes_prison:
            debug_surface = pygame.Surface((mur.width, mur.height), pygame.SRCALPHA)
            debug_surface.fill((0, 0, 255, 100))
            screen.blit(debug_surface, (mur.x - camera_x, mur.y - camera_y))

    # Plateformes normales
    for plat, img in zip(plateformes, platform_images):
        if img:
            screen.blit(img, (plat.x - camera_x, plat.y - camera_y))
    if debug_hitboxes:
        for plat in plateformes:
            debug_surface = pygame.Surface((plat.width, plat.height), pygame.SRCALPHA)
            debug_surface.fill((255, 0, 0, 100))
            screen.blit(debug_surface, (plat.x - camera_x, plat.y - camera_y))

    # Sol
    for s, img in zip(sol, sol_images):
        screen.blit(img, (s.x - camera_x, s.y - camera_y - 15))
    if debug_hitboxes:
        for s in sol:
            debug_surface = pygame.Surface((s.width, s.height), pygame.SRCALPHA)
            debug_surface.fill((255, 128, 0, 100))
            screen.blit(debug_surface, (s.x - camera_x, s.y - camera_y))
    # Sol2
    for s, img in zip(sol2, sol2_images):
        screen.blit(img, (s.x - camera_x, s.y - camera_y))

    # Pics sol
    for plat, img in zip(plateformes_danger, pic_sol_images):
        screen.blit(img, (plat.x - camera_x, plat.y - camera_y))

    # Pics plafond
    for plat, img in zip(plateformes_danger2, pic_plafond_images):
        screen.blit(img, (plat.x - camera_x, plat.y - camera_y))

    if debug_hitboxes:
        for plat in plateformes_danger + plateformes_danger2:
            debug_surface = pygame.Surface((plat.width, plat.height), pygame.SRCALPHA)
            debug_surface.fill((0, 255, 0, 100))
            screen.blit(debug_surface, (plat.x - camera_x, plat.y - camera_y))

    # Plateformes hautes (murs invisibles)
    for plat_haute in plateformes_haute:
        pygame.draw.rect(screen, (0, 0, 0),
                         (plat_haute.x - camera_x, plat_haute.y - camera_y,
                          plat_haute.width, plat_haute.height))

    # Panneau
    pancarte_active = joueur.rect.colliderect(panneau_rect) and not panneau_button_hidden
    if pancarte_active:
        screen.blit(bouton_e, (bouton_e_rect.x - camera_x - 700, bouton_e_rect.y - camera_y + button_offset))

    if debug_hitboxes:
        debug_surface = pygame.Surface((joueur.rect.width, joueur.rect.height), pygame.SRCALPHA)
        debug_surface.fill((0, 255, 0, 100))
        screen.blit(debug_surface, (joueur.rect.x - camera_x, joueur.rect.y - camera_y))

    # Effets double saut
    for effect in joueur.double_jump_effects:
        effect_surface = pygame.Surface((effect['width'], effect['height']), pygame.SRCALPHA)
        effect_surface.fill((255, 255, 255, effect['alpha']))
        screen.blit(effect_surface, (effect['x'] - camera_x - effect['width'] // 2, effect['y'] - camera_y))


    # HUD  Vies
    if not lire_pancarte:
        screen.blit(vie_text, (20, 20))
        for i in range(vies):
            screen.blit(coeur, (230 + i * 110, 5))

    # HUD  Icône double saut
    if joueur.double_saut and not lire_pancarte:
        screen.blit(double_jump, (screen_width - 150, screen_height - 260))

    # HUD  Icône inventaire
    if not lire_pancarte and not dialogue_g and not dialogue_v and not dialogue_c1:
        screen.blit(icone_inventaire, (screen_width - 150, screen_height - 150))
        screen.blit(lettre_f, (screen_width - 107, screen_height - 175))

    joueur.update()

    # Zone de détection joueur pour les NPC
    player_visual_rect = joueur.rect
    active = player_visual_rect.colliderect(giordano_rect)

    # Giordano  bouton E + dialogue
    if active and not dialogue_g:
        screen.blit(bouton_e, (bouton_e_rect.x - camera_x, bouton_e_rect.y - camera_y + button_offset))
    if dialogue_g:
        snip = police.render(message[0:counter // speed], True, '#4f2310')
        joueur.peut_bouger = False
        joueur.is_animating = False
        screen.blit(cadre_g, cadre_g_rect)
        screen.blit(snip, (480, 470))
        if not en_pause and counter < speed * len(message):
            counter += 1
            if counter % speed == 0:
                npcsfx.play()
        elif counter >= speed * len(message):
            npcsfx.stop()
            done = True
            screen.blit(bouton_e, (1000, 600 + button_offset))

    # Virgilio  bouton E + dialogue
    active2 = player_visual_rect.colliderect(virgilio_rect)
    if active2 and not dialogue_v:
        screen.blit(bouton_e, ((bouton_e_rect.x - 900) - camera_x, (bouton_e_rect.y - 2110) - camera_y + button_offset))
    if dialogue_v:
        snip = police.render(message2[0:counter // speed], True, '#4f2310')
        joueur.peut_bouger = False
        joueur.is_animating = False
        screen.blit(cadre_v, cadre_v_rect)
        screen.blit(snip, (480, 470))
        if not en_pause and counter < speed * len(message2):
            counter += 1
            if counter % speed == 0:
                npcsfx.play()
        elif counter >= speed * len(message2):
            npcsfx.stop()
            done = True
            screen.blit(bouton_e, (1020, 550 + button_offset))

    # Condamné1  bouton E + dialogue
    active3 = player_visual_rect.colliderect(condamne1_rect)
    if active3 and not dialogue_c1:
        screen.blit(bouton_e, (
            (280) - camera_x,
            (5730) - camera_y + button_offset
        ))
    if dialogue_c1:
        snip = police.render(message3[0:counter // speed], True, '#4f2310')
        joueur.peut_bouger = False
        joueur.is_animating = False
        screen.blit(cadre_c1, cadre_c1_rect)
        screen.blit(snip, (480, 470))
        if not en_pause and counter < speed * len(message3):
            counter += 1
            if counter % speed == 0:
                condamnesfx.play()
        elif counter >= speed * len(message3):
            condamnesfx.stop()
            done = True
            screen.blit(bouton_e, (1020, 550 + button_offset))

    # Titre "L'Enfer"
    if not en_pause and titre_index < speed * len(titre):
        titre_index += 1
        if titre_index % speed == 0:
            dialogue_sfx.play()
    elif not en_pause and titre_index >= speed * len(titre) and titre_fin == 0:
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
        if show_button_f_inventaire:
            screen.blit(bouton_f, (850, 600 + button_offset))
        if objet_dans_inventaire:
            screen.blit(frame_inventaire, (400, 250))

        if bottes_dans_inventaire:
            screen.blit(bottes, (400, 250))
            if bottes_equipees:
                pygame.draw.rect(screen, (255, 215, 0), (400, 250, 80, 80), 3)
            if tooltip_bottes_visible:
                tooltip_rect = pygame.Rect(490, 250, 130, 40)
                pygame.draw.rect(screen, (40, 40, 40), tooltip_rect)
                pygame.draw.rect(screen, (200, 200, 200), tooltip_rect, 2)
                texte_tooltip = "Déséquiper" if bottes_equipees else "Ã‰quiper"
                label = police.render(texte_tooltip, True, (255, 255, 255))
                screen.blit(label, (497, 260))
        if not objet_dans_inventaire:
            screen.blit(inventaire_vide_text, (500, 380))
            screen.blit(inventaire_vide_text2, (530, 400))

    # Menu pause
    if en_pause:
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        screen.blit(titre_logo, titre_rect)

        for i, bouton in enumerate(boutons_pause):
            y_bouton = 280 + i * 80
            x_bouton = screen_width // 2 - pause_button_width // 2
            rect_bouton = pygame.Rect(x_bouton, y_bouton, pause_button_width, pause_button_height)
            couleur_texte = "#f5c542" if i == pause_selected else "white"
            texte = police_bouton.render(bouton["texte"], True, couleur_texte)
            pygame.draw.rect(screen, "#521010", rect_bouton, border_radius=12)
            pygame.draw.rect(screen, "#B65252", rect_bouton, 3, border_radius=12)
            screen.blit(texte, (rect_bouton.centerx - texte.get_width() // 2, rect_bouton.centery - texte.get_height() // 2))
            if i == pause_selected:
                fleche = police_bouton.render(">", True, "#f5c542")
                screen.blit(fleche, (rect_bouton.x - 35, rect_bouton.centery - fleche.get_height() // 2))

    # Menu paramÃ¨tres (par-dessus la pause)
    if en_pause and afficher_parametres_pause:
        screen.blit(parametre_gui_pause, parametre_gui_rect_p)
        screen.blit(fermer_pause, fermer_pause_rect)
        screen.blit(police_param_pause.render("musique",  True, (255, 255, 255)), (270, 170))
        screen.blit(police_param_pause.render("speedrun (recommencer pour prendre effet)", True, (255, 255, 255)), (270, 270))
        screen.blit(police_param_pause.render("sfx", True, (255, 255, 255)), (270, 370))        
        for parametre in parametres_toggles_pause:
            img = activer_p if parametre["enabled"] else desactiver_p
            screen.blit(img, parametre["rect"])

    # HUD - Timer Speedrun
    if speedrun and not en_pause:
        if speedrun_started and not en_pause and not speedrun_finished:
            speedrun_elapsed = current_time - speedrun_start_time

        ms   = speedrun_elapsed % 1000
        sec  = (speedrun_elapsed // 1000) % 60
        mins = (speedrun_elapsed // 60000)
        timer_str = f"{mins:02d}:{sec:02d}.{ms // 10:02d}"

        couleur_timer = (255, 215, 0) if speedrun_finished else (255, 255, 255)
        timer_surf = police.render(timer_str, True, couleur_timer)
        screen.blit(timer_surf, (screen_width - timer_surf.get_width() - 20, 20))

        if not speedrun_finished:
            pygame.draw.rect(screen, (255, 215, 0),
                            (speedrun_finish_rect.x - camera_x,
                            speedrun_finish_rect.y - camera_y,
                            speedrun_finish_rect.width,
                            speedrun_finish_rect.height), 3)
            fin_label = police.render("FIN", True, (255, 215, 0))
            screen.blit(fin_label, (
                speedrun_finish_rect.x - camera_x + speedrun_finish_rect.width // 2 - fin_label.get_width() // 2,
                speedrun_finish_rect.y - camera_y - 30
            ))
        else:
            fini_surf = police.render("TERMINE !", True, (255, 215, 0))
            screen.blit(fini_surf, (screen_width - fini_surf.get_width() - 20, 50))
    # Porte enfer - affiche e si on collide
    if active_porte:
        screen.blit(
            bouton_e,
            (
                porte_rect.x - camera_x + porte_rect.width // 2 + 250,
                porte_rect.y - camera_y + button_offset + 350
            )
        )
    if transition_recommencer:
        temps_transition = current_time - transition_start
        if temps_transition <= transition_duree_fondu:
            alpha = int((temps_transition / transition_duree_fondu) * 255)
        else:
            alpha = 255
            if temps_transition >= transition_duree_fondu + transition_pause_noire:
                transition_recommencer = False
                reset()
        fondu = pygame.Surface((screen_width, screen_height))
        fondu.fill((0, 0, 0))
        fondu.set_alpha(alpha)
        screen.blit(fondu, (0, 0))
        titre_centre_img = titre_logo.copy()
        titre_centre_img.set_alpha(alpha)
        titre_centre = titre_centre_img.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(titre_centre_img, titre_centre)
    if transition_porte_enfer_start:
        temps_transition_porte = current_time - transition_porte_enfer_start
        if temps_transition_porte < 500:
            alpha = int((temps_transition_porte / 500) * 255)
        elif temps_transition_porte < 4500:
            alpha = 255
            if not transition_porte_teleporte:
                joueur.rect.center = (2100,6400) # coordonnée de destination, où il se teleporte
                joueur.vel_y = 0
                joueur.vx = 0
            transition_porte_teleporte = True
        elif temps_transition_porte < 5000:
            alpha = int((1 - ((temps_transition_porte - 4500) / 500)) * 255)
        else:
            transition_porte_enfer_start = 0
            joueur.peut_bouger = not (en_pause or lire_pancarte or inventaire_affiche or dialogue_g or dialogue_v or dialogue_c1)
            alpha = 0

        if alpha > 0:
            fondu = pygame.Surface((screen_width, screen_height))
            fondu.fill((0, 0, 0))
            fondu.set_alpha(alpha)
            screen.blit(fondu, (0, 0))
    pygame.display.flip()

pygame.quit()


