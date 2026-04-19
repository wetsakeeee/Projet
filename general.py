import pygame, sys, subprocess, time, random, math
from pathlib import Path
from joueur import Joueur
from monstre import Monstre
from plateformes import (get_plateforme_prison, get_plateformes, plateforme_pic, plateforme_pic2,
                         get_sol, get_plateformeshaute, get_sol2, mur2, plateforme_2,
                         get_bateau, get_plateformes_mobiles, get_niveau2, caronte_niveau2)
import sfx
from sfx import sauter, sfxmarche1, sfxmarche2, sfxmarche3, tombersfx, musiquefond, sfxboutton, choisirsfx, retoursfx
import settings
from esprit import Esprit
from squelette import Squelette

# ----------------------------
# Initialisation Pygame (une seule fois)
# ----------------------------
pygame.init()
pygame.mixer.init(48200)
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
icon = pygame.image.load("images/logo.png").convert_alpha()
pygame.display.set_icon(icon)
pygame.display.set_caption("Galileo Galilei : Across the afterlife")
clock = pygame.time.Clock()

# ============================================================
# PARAMÈTRES / SFX (partagés menu + jeu)
# ============================================================
SETTINGS_PATH = Path(__file__).with_name("settings.py")

def sauvegarder_settings():
    SETTINGS_PATH.write_text(
        "musique = " + str(settings.musique) + "\n"
        + "speedrun = " + str(settings.speedrun) + "\n"
        + "sfx = " + str(settings.sfx) + "\n",
        encoding="utf-8",
    )

def appliquer_parametre_jeu(param_name, enabled):
    if param_name == "musique":
        settings.musique = enabled
        sfx.musiquefond.set_volume(0.1 if enabled else 0)
        sfx.niveau_2caronte.set_volume(0.3 if enabled else 0)
        sfx.paradis.set_volume(0.3 if enabled else 0)
    elif param_name == "speedrun":
        settings.speedrun = enabled
    # Remplace tout le bloc elif param_name == "sfx": par :
    elif param_name == "sfx":
        settings.sfx = enabled
        vol = 0.5 if enabled else 0
        sfx.carontesfx.set_volume(vol)
        sfx.choisirsfx.set_volume(vol)
        sfx.coeurmort.set_volume(vol)
        sfx.coeursfx.set_volume(vol)
        sfx.couteausfx.set_volume(vol)
        sfx.debloquer_porte.set_volume(vol)
        sfx.degat.set_volume(vol)
        sfx.degat1.set_volume(vol)
        sfx.degat2.set_volume(vol)
        sfx.dialogue_csfx.set_volume(vol)
        sfx.fermer_inv.set_volume(vol)
        sfx.fin.set_volume(vol)
        sfx.fireballsfx.set_volume(vol)
        sfx.indicesfx.set_volume(vol)
        sfx.liresfx.set_volume(vol)
        sfx.mortsfx.set_volume(vol)
        sfx.objetsfx.set_volume(vol)
        sfx.ouvrir_inv.set_volume(vol)
        sfx.pausesfxbutton.set_volume(vol)
        sfx.pausesfxfermer.set_volume(vol)
        sfx.pausesfxouvrir.set_volume(vol)
        sfx.porte_entrer.set_volume(vol)
        sfx.porte_sortir.set_volume(vol)
        sfx.retoursfx.set_volume(vol)
        sfx.satan.set_volume(vol)
        sfx.sauter.set_volume(0.3 if enabled else 0)
        sfx.selectsfx.set_volume(vol)
        sfx.sfxboutton.set_volume(vol)
        sfx.sfxmarche1.set_volume(vol)
        sfx.sfxmarche2.set_volume(vol)
        sfx.sfxmarche3.set_volume(vol)
        sfx.sfxnpc.set_volume(vol)
        sfx.sfxtitre.set_volume(vol)
        sfx.squelette1.set_volume(vol)
        sfx.squelette2.set_volume(vol)
        sfx.squelette3.set_volume(vol)
        sfx.stoplire.set_volume(vol)
        sfx.tombersfx.set_volume(vol)
        sfx.viesfx.set_volume(vol)
    sauvegarder_settings()

# Appliquer les volumes au démarrage
appliquer_parametre_jeu("musique", settings.musique)
appliquer_parametre_jeu("sfx", settings.sfx)

# ============================================================
# ÉTAT GLOBAL : "menu" ou "jeu"
# ============================================================
etat_global = "menu"

# ============================================================
# RESSOURCES MENU
# ============================================================
Blanc = (255, 255, 255)
texte_bouton_col = (248, 236, 214)
brun_ombre = (24, 10, 8)
rouge_braise = (82, 16, 16, 210)
rouge_selection = (150, 45, 28, 235)
contour_bouton = (182, 122, 72)
contour_selection = (244, 197, 90)

BG = pygame.transform.scale(pygame.image.load("images/Fonds/fondmenu.png").convert_alpha(), (screen_width, screen_height))
titre_logo_menu = pygame.image.load("images/titre.png").convert_alpha()
titre_menu_rect = titre_logo_menu.get_rect(center=(screen_width // 2, screen_height // 2))
LOGO = pygame.transform.scale(pygame.image.load("images/logo.png").convert_alpha(), (300, 300))
logo_rect = LOGO.get_rect(center=(screen_width // 2, 150))

parametre_gui_menu = pygame.transform.scale(pygame.image.load("images/Paramètre/parametre.png").convert_alpha(), (screen_width, screen_height))
parametre_gui_menu_rect = parametre_gui_menu.get_rect(center=(screen_width // 2, screen_height // 2))
fermer_menu = pygame.transform.scale(pygame.image.load("images/Paramètre/fermer_fenetre.png").convert_alpha(), (50, 50))
fermer_menu_rect = fermer_menu.get_rect(topleft=(1200, 30))
activer_menu   = pygame.transform.scale(pygame.image.load("images/Paramètre/activer.png").convert_alpha(), (150, 75))
desactiver_menu = pygame.transform.scale(pygame.image.load("images/Paramètre/desactiver.png").convert_alpha(), (150, 75))

Police_bouton_menu = pygame.font.Font("asset/polices/Coolvetica Rg.otf", 36)
Police_parametre_menu = pygame.font.Font("asset/polices/ari-w9500-bold.ttf", 34)

curseur_img = pygame.transform.scale(pygame.image.load("images/GUI/curseur.png").convert_alpha(), (30, 30))
pygame.mouse.set_visible(False)

bouton_menu_img = pygame.transform.scale(pygame.image.load("images/GUI/Menu/bouton_menu.png").convert_alpha(),(450, 500))
bouton_menu_img_rect = bouton_menu_img.get_rect(topleft=((screen_width // 2) - 224, 285))
class Button:
    def __init__(self, text, center_y, action, image=None):
        self.text = text
        self.action = action
        self.image = image
        self.width, self.height = 320, 70
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (screen_width // 2, center_y)

    def draw(self, win, mouse_pos):
        is_hover = self.rect.collidepoint(mouse_pos)
        if self.image:
            # Dessiner l'image à la place du rectangle coloré
            win.blit(self.image, self.rect)
        else:
            surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(surf, rouge_selection if is_hover else rouge_braise, (0, 0, self.width, self.height), border_radius=16)
            pygame.draw.rect(surf, contour_selection if is_hover else contour_bouton, (0, 0, self.width, self.height), width=3, border_radius=16)
            win.blit(surf, self.rect)
            ombre = Police_bouton_menu.render(self.text, True, brun_ombre)
            win.blit(ombre, ombre.get_rect(center=(self.rect.centerx + 2, self.rect.centery + 2)))
            txt = Police_bouton_menu.render(self.text, True, texte_bouton_col)
            win.blit(txt, txt.get_rect(center=self.rect.center))

    def is_clicked(self, mouse_pos, mouse_pressed):
        return self.rect.collidepoint(mouse_pos) and mouse_pressed[0]
    
buttons_menu = [
    Button("Jouer",       360, "play"),
    Button("Parametres",  470, "settings"),
    Button("Quitter",     600, "quit"),
]

parametres_toggles_menu = [
    {"name": "musique",  "enabled": settings.musique,  "rect": pygame.Rect(100, 150, 150, 75)},
    {"name": "speedrun", "enabled": settings.speedrun, "rect": pygame.Rect(100, 250, 150, 75)},
    {"name": "sfx",      "enabled": settings.sfx,      "rect": pygame.Rect(100, 350, 150, 75)},
]

# Musique menu
if settings.musique:
    sfx.musiquemenu.set_volume(0.5)
    sfx.musiquemenu.play(-1, 0, 3000)
else:
    sfx.musiquemenu.set_volume(0)

afficher_parametres_menu = False
intro = True
intro_start = pygame.time.get_ticks()
INTRO_DURATION = 4500

# ============================================================
# RESSOURCES JEU (chargées une seule fois quand on lance le jeu)
# ============================================================
jeu_initialise = False

# Variables jeu — déclarées ici pour que reset() y ait accès via global
joueur = None
monstre = None
sons_squelette = None
sons_monstre = None
vies = 3
etat = "jeu"
niveau_actuel = 1

# (toutes les autres variables jeu sont initialisées dans initialiser_jeu())

def initialiser_jeu():
    """Charge toutes les ressources du jeu. Appelée une seule fois au clic Jouer."""
    global message_caronte_post_niveau2
    global icone_bulle_monstre, icone_bulle_esprit, icone_bulle_squelette
    global jeu_initialise, joueur, monstre, sons_squelette, sons_monstre
    global vies, etat, niveau_actuel
    global debug_hitboxes, coordonne_active
    global death_animation_start, death_sound_stage, death_animation_done
    global DEATH_ANIMATION_SPEEDUP_MS, DEATH_HEART_ON_PLAYER_MS, DEATH_HEART_TRAVEL_MS
    global DEATH_HEART_CENTER_HOLD_MS, DEATH_HAND_DELAY_MS, DEATH_HAND_ENTER_MS
    global DEATH_HAND_GRAB_MS, DEATH_HAND_EXIT_MS, DEATH_SATAN_ENTER_MS, DEATH_GAME_OVER_DELAY_MS
    global titre_logo_jeu, titre_rect_jeu
    global speedrun, speedrun_started, speedrun_start_time, speedrun_elapsed
    global speedrun_pause_start, speedrun_finish_rect, speedrun_finished, speedrun_final_time
    global porte, porte_rect, message_porte_fermee_timer
    global porte_enfer_ouverte, porte_enfer_img_ouverte
    global porte_finale_bloquee, porte_finale_rouge, porte_finale_noir, porte_finale_ouverte_img
    global PORTE_FINALE_X, PORTE_FINALE_Y, porte_finale_rect, active_porte_finale, porte_finale_prete
    global porte_cle_caronte_utilisee, porte_cle_enfer_utilisee
    global pause_active
    global coeur, vie_text, double_jump_img
    global police, police_titre
    global invincible, invincibilite_temps, duree_invincibilite
    global titre_jeu, titre_index, titre_fin
    global panneau, panneau_rect, pancarte_active, panneau_button_hidden, panneau_button_timer
    global pancarte, lire_pancarte, pancarte_timer, show_button_e_pancarte
    global active, active2, active3, active4, active_porte
    global inventaire_active, frame_inventaire, bottes_img, potion_vie_img, couteau_img
    global cooldown_imgs, cle_caronte_img, cle_enfer_img
    global icone_inventaire, inventaire_img, inventaire_affiche, inventaire_timer
    global show_button_f_inventaire, inventaire_vide_text, inventaire_vide_text2, lettre_f
    global bottes_equipees, couteau_equipee, cle_caronte_equipee, cle_enfer_equipee
    global inventaire, inventaire_index_selectionne, tooltip_inventaire_visible
    global bouton_e, bouton_e_rect, bouton_f
    global giordano, giordano2, giordano3, giordano_images
    global current_giordano, giordano_anim_timer, giordano_forward, giordano_pause, giordano_pause_timer
    global giordano_rect
    global MESSAGES_GIORDANO_NORMAL, MESSAGES_GIORDANO_POST_CARONTE
    global messages, giordano_post_caronte_fait, caronte_niveau2_termine
    global dialogue_g, cadre_g, cadre_g_rect
    global coeurt_mort, main1, main2, satan1, satan2
    global freeze_bg, niveau2_bg_offset, paliers_bateau, palier_bateau_index, nombre_monstres_tues
    global giordano_cooldown, virgilio_cooldown, duree_cooldown
    global giordano_dialogue_cooldown, virgilio_dialogue_cooldown
    global condamne1_dialogue_cooldown, caronte_dialogue_cooldown, duree_dialogue_cooldown
    global counter, speed, active_message, message, done
    global virgilio, virgilio_rect, dialogue_v, cadre_v, cadre_v_rect
    global message_v, active_message2, message2
    global virgilio2_rect, dialogue_v2, cadre_v2, message_v2, active_message_v2
    global message_v2_actuel, virgilio2_dialogue_cooldown, active_v2, virgilio2_dialogue_fait
    global condamne1, condamne1_rect, dialogue_c1, cadre_c1, cadre_c1_rect
    global message_c1, active_message_c1, message3
    global caronte_npc, caronte_rect, dialogue_caronte, dialogue_caronte_fin
    global cadre_caronte, cadre_caronte_rect, message_caronte, active_message_caronte
    global message4, message_caronte_fin
    global choix_cadre, choix_cadre_rect, message5, choix_active, choix_fait
    global message_reponse_active, message_reponse_index, message_reponse_counter, message_reponse_done
    global transition_caronte_start, transition_caronte_teleporte
    global transition_caronte_fin_start, transition_caronte_fin_teleporte, fin_caronte_declenchee
    global bateau_deco, bateau_rect
    global plateformes_haute, plateformes_haute_m, mur2_rects
    global chute_y, zoom_factor, camera_y_offset, camera_x, camera_y
    global plateformes_prison, plateformes, plateformes2, sol, niveau_largeur, sol2, plateformes_mobiles
    global platform_image_orig, plateforme_petite_orig, plateforme2_img
    global platform_images, sol_images, sol2_images, mur2_images
    global plateformes_danger, plateformes_danger2, pic_sol_images, pic_plafond_images
    global mur_prison_images, plateforme2_images
    global background, bg_width, bg_height, bg_offset_x, bg_offset_y, parallax_factor
    global monstre_spawn
    global transition_recommencer, transition_start, transition_duree_fondu, transition_pause_noire
    global transition_porte_enfer_start, transition_porte_teleporte
    global en_pause, police_pause, police_bouton_pause
    global boutons_pause, pause_selected, pause_hover_index, pause_button_width, pause_button_height
    global afficher_parametres_pause, parametre_gui_pause, parametre_gui_rect_p
    global fermer_pause, fermer_pause_rect, activer_p, desactiver_p
    global police_param_pause, parametres_toggles_pause
    global police_grande, police_petite
    global bouton_rejouer, bouton_menu_go, bouton_quitter
    global background_game_over
    global fond_caronte1, fond_caronte2, fond_caronte3, fond_caronte4, fond_caronte5, fond_caronte_eau
    global bateau_plat, bateau_img1, bateau_img2, bateau_rame_casse, rame_casse
    global rame_casse_plat, rame_interaction_rect, bateau_image, bateau_image2
    global monstres_niveau2, dernier_spawn_monstre, spawn_delay, nombre_de_monstre
    global sol_bateau, caronte_aide, bateau_reparer, rame_ramasser, active_rame, donner_rame
    global message_cle_timer, message_cle_actif
    global caronte_rame_dialogue_fait, message_caronte_rame
    global message_caronte_rame_counter, message_caronte_rame_done, caronte2
    global niveau2_plat, niveau2_images
    global start_time, porte_enfer_origine_x
    global fin_image, transition_fin_active, transition_fin_start, transition_fin_phase, TEXTES_FIN
    global bulle_monstre_actif, bulle_monstre_texte, bulle_monstre_type
    global bulle_monstre_debut, bulle_monstre_timer, bulle_monstre_prochain
    global BULLE_DUREE, BULLES_TEXTES_MONSTRE, BULLES_TEXTES_ESPRIT, BULLES_TEXTES_SQUELETTE, icone_bulle
    global jump_key_held, ground_jump_consumed

    joueur  = Joueur()
    monstre = Monstre()
    sons_squelette = [sfx.squelette1, sfx.squelette2, sfx.squelette3]
    sons_monstre   = [sfx.degat1, sfx.degat2]

    debug_hitboxes   = False

    death_animation_start    = None
    death_sound_stage        = 0
    death_animation_done     = False
    DEATH_ANIMATION_SPEEDUP_MS  = 300
    DEATH_HEART_ON_PLAYER_MS    = 1000
    DEATH_HEART_TRAVEL_MS       = 2000
    DEATH_HEART_CENTER_HOLD_MS  = 2200
    DEATH_HAND_DELAY_MS         = 3050
    DEATH_HAND_ENTER_MS         = 2000
    DEATH_HAND_GRAB_MS          = 500
    DEATH_HAND_EXIT_MS          = 1700
    DEATH_SATAN_ENTER_MS        = 1200
    DEATH_GAME_OVER_DELAY_MS    = (
        DEATH_HEART_ON_PLAYER_MS + DEATH_HEART_TRAVEL_MS + DEATH_HEART_CENTER_HOLD_MS
        + DEATH_HAND_GRAB_MS + DEATH_HAND_EXIT_MS + DEATH_SATAN_ENTER_MS + 4000
        - DEATH_ANIMATION_SPEEDUP_MS
    )

    titre_logo_jeu  = pygame.image.load("images/titre.png").convert_alpha()
    titre_rect_jeu  = titre_logo_jeu.get_rect(midtop=(screen_width // 2, 100))

    vies          = 3
    etat          = "jeu"
    niveau_actuel = 1

    speedrun            = settings.speedrun
    speedrun_started    = False
    speedrun_start_time = 0
    speedrun_elapsed    = 0
    speedrun_pause_start = None
    speedrun_finish_rect = pygame.Rect(1875, 1240, 80, 200)
    speedrun_finished   = False
    speedrun_final_time = 0

    porte = pygame.transform.scale(pygame.image.load("images/Divers/porte_enfer.png").convert_alpha(), (380, 530))
    porte_rect = porte.get_rect(topleft=(300, 320))
    message_porte_fermee_timer = -10000
    porte_enfer_ouverte    = False
    porte_enfer_img_ouverte = pygame.transform.scale(pygame.image.load("images/Divers/porte_enfer_ouverte.png").convert_alpha(), (380, 530))

    porte_finale_bloquee   = pygame.transform.scale(pygame.image.load("images/Divers/porte_finale/porte_finale_bloquer.png").convert_alpha(), (380, 530))
    porte_finale_rouge     = pygame.transform.scale(pygame.image.load("images/Divers/porte_finale/porte_finale_rouge.png").convert_alpha(), (380, 530))
    porte_finale_noir      = pygame.transform.scale(pygame.image.load("images/Divers/porte_finale/porte_finale_noir.png").convert_alpha(), (380, 530))
    porte_finale_ouverte_img = pygame.transform.scale(pygame.image.load("images/Divers/porte_finale/porte_finale.png").convert_alpha(), (380, 530))
    PORTE_FINALE_X     = 2100
    PORTE_FINALE_Y     = 3470
    porte_finale_rect  = pygame.Rect(PORTE_FINALE_X, PORTE_FINALE_Y, 380, 530)
    active_porte_finale = False
    porte_finale_prete  = False
    porte_cle_caronte_utilisee = False
    porte_cle_enfer_utilisee   = False

    pause_active = True

    coeur       = pygame.transform.scale(pygame.image.load("images/GUI/coeur.png").convert_alpha(), (100, 100))
    vie_text    = pygame.transform.scale(pygame.image.load("images/GUI/vie.png").convert_alpha(), (186, 72))
    double_jump_img = pygame.transform.scale(pygame.image.load("images/GUI/icone_double_jump.png").convert_alpha(), (100, 100))
    police      = pygame.font.Font("asset/polices/ari-w9500-bold.ttf", 24)
    police_titre = pygame.font.Font("asset/polices/Dungeon Depths.otf", 50)

    invincible          = False
    invincibilite_temps = 0
    duree_invincibilite = 2000

    titre_jeu   = "L'Enfer"
    titre_index = 0
    titre_fin   = 0

    panneau = pygame.transform.scale(pygame.image.load("images/Divers/panneau.png").convert_alpha(), (96, 150))
    panneau_rect = panneau.get_rect(topleft=(800, 6150))
    pancarte_active       = False
    panneau_button_hidden = False
    panneau_button_timer  = 0
    pancarte = pygame.transform.scale(pygame.image.load("images/GUI/pancarte.png").convert_alpha(), (900, 480))
    lire_pancarte          = False
    pancarte_timer         = 0
    show_button_e_pancarte = False

    active = active2 = active3 = active4 = active_porte = False

    inventaire_active        = True
    frame_inventaire         = pygame.transform.scale(pygame.image.load("images/GUI/Inventaire/frame_inventaire.png").convert_alpha(), (80, 80))
    bottes_img               = pygame.transform.scale(pygame.image.load("images/Objets/botte.png").convert_alpha(), (80, 80))
    potion_vie_img           = pygame.transform.scale(pygame.image.load("images/Objets/potion_vie.png").convert_alpha(), (80, 80))
    couteau_img              = pygame.transform.scale(pygame.image.load("images/Objets/couteau.png").convert_alpha(), (80, 80))
    cooldown_imgs            = [pygame.transform.scale(pygame.image.load(f"images/cooldown/cooldown{i}.png").convert_alpha(), (51, 15)) for i in range(5)]
    cle_caronte_img          = pygame.transform.scale(pygame.image.load("images/Objets/cle_caronte.png").convert_alpha(), (80, 80))
    cle_enfer_img            = pygame.transform.scale(pygame.image.load("images/Objets/cle_enfer.png").convert_alpha(), (80, 80))
    icone_inventaire         = pygame.transform.scale(pygame.image.load("images/GUI/icone_inventaire.png").convert_alpha(), (100, 100))
    inventaire_img           = pygame.transform.scale(pygame.image.load("images/GUI/Inventaire/inventaire.png").convert_alpha(), (560, 630))
    inventaire_affiche       = False
    inventaire_timer         = 0
    show_button_f_inventaire = False
    inventaire_vide_text     = police.render("Vous n'avez rien dans", True, "#7a371b")
    inventaire_vide_text2    = police.render("votre inventaire !", True, "#7a371b")
    lettre_f                 = police.render("F", True, "#ffffff")

    bottes_equipees     = joueur.double_saut
    couteau_equipee     = joueur.couteau_equipee
    cle_caronte_equipee = False
    cle_enfer_equipee   = False

    inventaire                   = []
    inventaire_index_selectionne = None
    tooltip_inventaire_visible   = False

    bouton_e      = pygame.transform.scale(pygame.image.load("images/GUI/bouton_e.png").convert_alpha(), (50, 50))
    bouton_e_rect = bouton_e.get_rect(topleft=(1600, 6150))
    bouton_f      = pygame.transform.scale(pygame.image.load("images/GUI/bouton_f.png").convert_alpha(), (50, 50))

    giordano  = pygame.transform.scale(pygame.image.load("images/Npc/Textures/giordano.png").convert_alpha(), (160, 105))
    giordano2 = pygame.transform.scale(pygame.image.load("images/Npc/Textures/giordano2.png").convert_alpha(), (160, 105))
    giordano3 = pygame.transform.scale(pygame.image.load("images/Npc/Textures/giordano3.png").convert_alpha(), (160, 105))
    giordano_images      = [giordano, giordano2, giordano3]
    current_giordano     = 0
    giordano_anim_timer  = 0
    giordano_forward     = True
    giordano_pause       = False
    giordano_pause_timer = 0
    giordano_rect        = giordano.get_rect(topleft=(1600, 6190))

    MESSAGES_GIORDANO_NORMAL      = ["GALILEO !!", "C'EST UN ENFER !", "T'ES COINCES DANS CETTE PRISON A VIE", "RECOMMENCE DEPUIS LE DEBUT"]
    MESSAGES_GIORDANO_POST_CARONTE = [
        "Ah salut Galileo !", "T'as besoin de ma clé ?",
        "Me dis pas que c'est Virgilio qui t'as dit ça ?",
        "Il pouvait au moins me- me rendre visite..",
        "Tant pis, mais écoute prend cette clé.", "Bonne chance Galileo.",
    ]
    messages                   = list(MESSAGES_GIORDANO_NORMAL)
    giordano_post_caronte_fait = False
    caronte_niveau2_termine    = False
    dialogue_g   = False
    cadre_g      = pygame.image.load("images/Npc/Dialogues/cadre_dialogue_giordano.png").convert_alpha()
    cadre_g_rect = cadre_g.get_rect(center=(640, 550))

    coeurt_mort = pygame.transform.scale(pygame.image.load("images/animation_fin/coeur_mort.png").convert_alpha(), (60, 60))
    main1  = pygame.transform.scale(pygame.image.load("images/animation_fin/main1.png").convert_alpha(), (1300, 600))
    main2  = pygame.transform.scale(pygame.image.load("images/animation_fin/main2.png").convert_alpha(), (1300, 600))
    satan1 = pygame.transform.scale(pygame.image.load("images/animation_fin/satan1.png").convert_alpha(), (1300, 600))
    satan1.set_colorkey((0, 0, 0))
    satan2 = pygame.transform.scale(pygame.image.load("images/animation_fin/satan2.png").convert_alpha(), (1300, 600))
    satan2.set_colorkey((0, 0, 0))

    freeze_bg            = 0
    niveau2_bg_offset    = 0
    paliers_bateau       = [5, 15, 30]
    palier_bateau_index  = 0
    nombre_monstres_tues = 0

    giordano_cooldown           = -30000
    virgilio_cooldown           = -30000
    duree_cooldown              = 30000
    giordano_dialogue_cooldown  = -3000
    virgilio_dialogue_cooldown  = -3000
    condamne1_dialogue_cooldown = -3000
    caronte_dialogue_cooldown   = -3000
    duree_dialogue_cooldown     = 3000

    counter        = 0
    speed          = 3
    active_message = 0
    message        = messages[active_message]
    done           = False

    virgilio      = pygame.transform.scale(pygame.image.load("images/Npc/Textures/virgilio.png").convert_alpha(), (60, 120))
    virgilio_rect = virgilio.get_rect(topleft=(700, 4080))
    dialogue_v    = False
    cadre_v       = pygame.image.load("images/Npc/Dialogues/cadre_dialogue_virgilio.png").convert_alpha()
    cadre_v_rect  = cadre_v.get_rect(center=(640, 550))
    message_v       = ["Salut Galileo !", "Fais attention car les plateformes deviennent\ndifficiles !", "Prends ces bottes pour sauter deux fois."]
    active_message2 = 0
    message2        = message_v[0]

    virgilio2_rect              = virgilio.get_rect(topleft=(930, 720))
    dialogue_v2                 = False
    cadre_v2                    = cadre_v
    message_v2                  = ["Attends, laisse moi ouvrir la porte.", "Et voila, tu peux y aller !", "Ah et aussi, Giordano se trouve tout\n en bas, dans la prison","Je pense qu'il sera utile pour toi.","Mais avant ca, va voir Caronte."]
    active_message_v2           = 0
    message_v2_actuel           = message_v2[0]
    virgilio2_dialogue_cooldown = -3000
    active_v2                   = False
    virgilio2_dialogue_fait     = False

    condamne1      = pygame.transform.scale(pygame.image.load("images/Npc/Textures/condamne1.png").convert_alpha(), (112, 112))
    condamne1_rect = condamne1.get_rect(topleft=(300, 5737))
    dialogue_c1    = False
    cadre_c1       = pygame.image.load("images/Npc/Dialogues/cadre_dialogue_condamne.png").convert_alpha()
    cadre_c1_rect  = cadre_c1.get_rect(center=(640, 550))
    message_c1        = ["...", "...", "Aide m-", "...", "Prends ce couteau, t'en aura besoin...", "C'est trop dangereux ici...", "J'suis pas capable de survivre..."]
    active_message_c1 = 0
    message3          = message_c1[0]

    caronte_npc      = pygame.transform.scale(pygame.image.load("images/Npc/Textures/caronte.png").convert_alpha(), (64, 120))
    caronte_rect     = caronte_npc.get_rect(topleft=(3850, 5380))
    dialogue_caronte     = False
    dialogue_caronte_fin = False
    cadre_caronte        = pygame.image.load("images/Npc/Dialogues/cadre_dialogue_caronte.png").convert_alpha()
    cadre_caronte_rect   = cadre_caronte.get_rect(center=(640, 550))
    message_caronte = [
        "Je suis Caronte, le passeur des Enfers.",
        "Si tu veux sortir d'ici, tu devras m'aider à passer\nsur le fleuve.",
        "Des codamnés y abritent et tentent de nous faire\ncouler moi et mon bateau. ",
        "Aide moi à passer et je te donnerai un cadeau\nen échange."
    ]
    active_message_caronte = 0
    message4               = message_caronte[0]
    message_caronte_fin    = ["Merci de m'avoir aidé, Galileo !", "Comme promis, voici ta récompense."]
    message_caronte_post_niveau2 = ["Merci encore de ton aide, Galileo !", "Tu m'as vraiment sauvé la mise."]


    choix_cadre      = pygame.image.load("images/Npc/Dialogues/cadre_choix.png").convert_alpha()
    choix_cadre_rect = choix_cadre.get_rect(center=(640, 550))
    message5         = ["Merci beaucoup ! Aller viens, monte dans mon\nbateau !", "Aucun problème, passe me voir quand tu\nchangeras d'avis."]
    choix_active            = False
    choix_fait              = None
    message_reponse_active  = False
    message_reponse_index   = None
    message_reponse_counter = 0
    message_reponse_done    = False

    transition_caronte_start         = 0
    transition_caronte_teleporte     = False
    transition_caronte_fin_start     = 0
    transition_caronte_fin_teleporte = False
    fin_caronte_declenchee           = False

    bateau_deco = pygame.transform.scale(pygame.image.load("images/Divers/bateau.png").convert_alpha(), (300, 130))
    bateau_rect = bateau_deco.get_rect(topleft=(3500, 5370))

    plateformes_haute   = get_plateformeshaute()
    plateformes_haute_m = [plateformes_haute[0]]
    mur2_rects          = mur2()

    chute_y        = 7000
    zoom_factor    = 3
    camera_y_offset = -100
    camera_x = joueur.rect.centerx - screen_width // 2
    camera_y = joueur.rect.centery - screen_height // 2

    plateformes_prison  = get_plateforme_prison()
    plateformes         = get_plateformes()
    plateformes2        = plateforme_2()
    sol                 = get_sol()
    niveau_largeur      = 5000
    sol2                = get_sol2()
    plateformes_mobiles = get_plateformes_mobiles()

    try:
        platform_image_orig    = pygame.image.load("images/Plateformes/Niveau1/plateforme_moyenne.png").convert_alpha()
        plateforme_petite_orig = pygame.image.load("images/Plateformes/Niveau1/plateforme_petite.png").convert_alpha()
        plateforme2_img        = pygame.image.load("images/Plateformes/Niveau2/plateforme2.png").convert_alpha()
        mur_prison_orig        = pygame.image.load("images/Plateformes/Niveau1/murprison.png").convert_alpha()
        sol_image_orig         = pygame.image.load("images/Plateformes/Niveau1/sol.png").convert_alpha()
        pic_sol_orig           = pygame.image.load("images/Plateformes/pic_sol.png").convert_alpha()
        pic_plafond_orig       = pygame.image.load("images/Plateformes/pic_plafond.png").convert_alpha()
        sol2_image_orig        = pygame.image.load("images/Plateformes/Niveau2/sol_niveau2.png").convert_alpha()
        mur2_image_orig        = pygame.image.load("images/Plateformes/Niveau2/mur_niveau2.png").convert_alpha()
        mur2_2_image_orig      = pygame.image.load("images/Plateformes/Niveau2/mur2_niveau2.png").convert_alpha()
    except:
        platform_image_orig = plateforme_petite_orig = plateforme2_img = mur_prison_orig = None
        sol_image_orig = pic_sol_orig = pic_plafond_orig = sol2_image_orig = None
        mur2_image_orig = mur2_2_image_orig = None

    platform_images = []
    for pl in plateformes:
        orig = plateforme_petite_orig if (pl.width == 100 and pl.height == 40) else platform_image_orig
        platform_images.append(pygame.transform.scale(orig, (pl.width, pl.height)) if orig else None)

    sol_images  = [pygame.transform.scale(sol_image_orig,  (s.width, s.height)) for s in sol]
    sol2_images = [pygame.transform.scale(sol2_image_orig, (s.width, s.height)) for s in sol2]

    mur2_images = []
    for idx, s in enumerate(mur2_rects):
        orig = mur2_image_orig if idx == 0 else mur2_2_image_orig
        mur2_images.append(pygame.transform.scale(orig, (s.width, s.height)) if orig else None)

    plateformes_danger  = plateforme_pic()
    plateformes_danger2 = plateforme_pic2()
    pic_sol_images     = [pygame.transform.scale(pic_sol_orig,    (p.width, p.height)) for p in plateformes_danger]
    pic_plafond_images = [pygame.transform.scale(pic_plafond_orig,(p.width, p.height)) for p in plateformes_danger2]
    mur_prison_images  = [pygame.transform.scale(mur_prison_orig, (m.width, m.height)) for m in plateformes_prison]
    plateforme2_images = [pygame.transform.scale(plateforme2_img, (p.width, p.height)) for p in plateformes2]

    background_orig = pygame.image.load("images/Fonds/background.png").convert_alpha()
    img_w, img_h    = background_orig.get_size()
    ratio           = max(screen_width / img_w, screen_height / img_h)
    bg_width        = int(img_w * ratio * zoom_factor)
    bg_height       = int(img_h * ratio * zoom_factor)
    background      = pygame.transform.smoothscale(background_orig, (bg_width, bg_height))
    bg_offset_x     = -200
    bg_offset_y     = -300
    parallax_factor = 0.5

    monstre_spawn = Monstre(1500, 3550)

    for pl in plateformes:
        if joueur.rect.colliderect(pl):
            joueur.rect.bottom = pl.top
            joueur.vel_y = 0

    transition_recommencer       = False
    transition_start             = 0
    transition_duree_fondu       = 500
    transition_pause_noire       = 2000
    transition_porte_enfer_start = 0
    transition_porte_teleporte   = False

    en_pause          = False
    police_pause      = pygame.font.Font("asset/polices/Dungeon Depths.otf", 80)
    police_bouton_pause = pygame.font.Font("asset/polices/ari-w9500-bold.ttf", 32)

    boutons_pause = [
        {"texte": "Reprendre",   "action": "reprendre"},
        {"texte": "Recommencer", "action": "recommencer"},
        {"texte": "Menu",        "action": "menu"},
        {"texte": "Parametres",  "action": "parametres"},
        {"texte": "Quitter",     "action": "quitter"},
    ]
    pause_selected      = 0
    pause_hover_index   = -1
    pause_button_width  = 280
    pause_button_height = 56

    afficher_parametres_pause = False
    parametre_gui_pause  = pygame.transform.scale(pygame.image.load("images/Paramètre/parametre.png").convert_alpha(), (screen_width, screen_height))
    parametre_gui_rect_p = parametre_gui_pause.get_rect(center=(screen_width // 2, screen_height // 2))
    fermer_pause         = pygame.transform.scale(pygame.image.load("images/Paramètre/fermer_fenetre.png").convert_alpha(), (50, 50))
    fermer_pause_rect    = fermer_pause.get_rect(topleft=(1200, 30))
    activer_p            = pygame.transform.scale(pygame.image.load("images/Paramètre/activer.png").convert_alpha(), (150, 75))
    desactiver_p         = pygame.transform.scale(pygame.image.load("images/Paramètre/desactiver.png").convert_alpha(), (150, 75))
    police_param_pause   = pygame.font.Font("asset/polices/ari-w9500-bold.ttf", 34)
    parametres_toggles_pause = [
        {"name": "musique",  "enabled": settings.musique,  "rect": pygame.Rect(100, 150, 150, 75)},
        {"name": "speedrun", "enabled": settings.speedrun, "rect": pygame.Rect(100, 250, 150, 75)},
        {"name": "sfx",      "enabled": settings.sfx,      "rect": pygame.Rect(100, 350, 150, 75)},
    ]

    police_grande  = pygame.font.SysFont(None, 80)
    police_petite  = pygame.font.Font("asset/polices/Coolvetica Rg.otf", 36)
    bouton_rejouer = pygame.Rect(490, 350, 300, 50)
    bouton_menu_go = pygame.Rect(490, 420, 300, 50)
    bouton_quitter = pygame.Rect(490, 490, 300, 50)

    background_game_over = pygame.transform.scale(pygame.image.load("images/Fonds/image3.jpg").convert(), (screen_width, screen_height))

    fond_caronte1    = pygame.transform.scale(pygame.image.load("images/Fonds/Niveau_2/fond_caronte1.png").convert_alpha(), (screen_width * 2, screen_height * 2))
    fond_caronte2    = pygame.transform.scale(pygame.image.load("images/Fonds/Niveau_2/fond_caronte2.png").convert_alpha(), (screen_width * 2, screen_height * 2))
    fond_caronte3    = pygame.transform.scale(pygame.image.load("images/Fonds/Niveau_2/fond_caronte3.png").convert_alpha(), (screen_width * 2, screen_height * 2))
    fond_caronte4    = pygame.transform.scale(pygame.image.load("images/Fonds/Niveau_2/fond_caronte4.png").convert_alpha(), (screen_width * 2, screen_height * 2))
    fond_caronte5    = pygame.transform.scale(pygame.image.load("images/Fonds/Niveau_2/fond_caronte5.png").convert_alpha(), (screen_width * 2, screen_height * 2))
    fond_caronte_eau = pygame.transform.scale(pygame.image.load("images/Fonds/Niveau_2/fond_caronte_eau.png").convert_alpha(), (screen_width * 2, screen_height * 2))

    bateau_plat       = get_bateau()
    bateau_img1       = pygame.image.load("images/Divers/bateau_1.png").convert_alpha()
    bateau_img2       = pygame.image.load("images/Divers/bateau_2.png").convert_alpha()
    bateau_rame_casse = pygame.transform.scale(pygame.image.load("images/Divers/bateau_rame_casse.png").convert_alpha(), (bateau_plat[0].width, bateau_plat[0].height))
    rame_casse        = pygame.transform.scale(pygame.image.load("images/Divers/rame_casse.png").convert_alpha(), (63, 36))
    rame_casse_plat   = rame_casse.get_rect(topleft=(2900, 780))
    rame_interaction_rect = rame_casse_plat.inflate(80, 80)
    bateau_image  = [pygame.transform.scale(bateau_img1, (b.width, b.height)) for b in bateau_plat]
    bateau_image2 = [pygame.transform.scale(bateau_img2, (b.width, b.height)) for b in bateau_plat]

    monstres_niveau2      = []
    dernier_spawn_monstre = 0
    spawn_delay           = random.randint(4500, 5500)
    nombre_de_monstre     = 0

    sol_bateau     = bateau_plat[0]
    caronte_aide   = False
    bateau_reparer = True
    rame_ramasser  = True
    active_rame    = False
    donner_rame    = False

    message_cle_timer = 0
    message_cle_actif = False

    caronte_rame_dialogue_fait   = False
    message_caronte_rame         = "Oh non ! La rame s'est cassée. Va la\nramasser !"
    message_caronte_rame_counter = 0
    message_caronte_rame_done    = False
    caronte2      = caronte_niveau2()
    niveau2_plat  = get_niveau2()
    niveau2_images = [pygame.transform.scale(plateforme2_img, (p.width, p.height)) for p in niveau2_plat]

    start_time            = pygame.time.get_ticks()
    porte_enfer_origine_x = 0

    fin_image = pygame.transform.scale(pygame.image.load("images/Fonds/fin.png").convert(), (screen_width, screen_height))
    transition_fin_active = False
    transition_fin_start  = 0
    transition_fin_phase  = 0
    TEXTES_FIN = [
        "Galileo attraversa le Purgatoire en esquivant",
        "de nombreux condamnés...",
        "Il finit par atteindre le Paradis, sain et sauf.",
    ]

    bulle_monstre_actif    = False
    bulle_monstre_texte    = ""
    bulle_monstre_type     = ""
    bulle_monstre_debut    = 0
    bulle_monstre_timer    = 0
    bulle_monstre_prochain = random.randint(12000, 15000)
    BULLE_DUREE             = 3000
    BULLES_TEXTES_MONSTRE   = "laISseR Moi MonTEr sUR lE BAteAU !"
    BULLES_TEXTES_ESPRIT    = "Viens là.."
    BULLES_TEXTES_SQUELETTE = "J'espère que t'as chaud"
    icone_bulle_monstre  = pygame.transform.scale(pygame.image.load("images/GUI/monstre_tete.png").convert_alpha(), (40, 40))
    icone_bulle_esprit   = pygame.transform.scale(pygame.image.load("images/GUI/esprit_tete.png").convert_alpha(), (40, 40))
    icone_bulle_squelette = pygame.transform.scale(pygame.image.load("images/GUI/squelette_tete.png").convert_alpha(), (40, 40))

    jump_key_held        = False
    ground_jump_consumed = False

    jeu_initialise = True

# ============================================================
# FONCTIONS JEU (inventaire, reset, etc.)
# ============================================================
INVENTAIRE_SLOT_DEPART   = (430, 250)
INVENTAIRE_SLOT_TAILLE   = 80
INVENTAIRE_SLOT_COLONNES = 4
INVENTAIRE_SLOT_ECART_X  = 110
INVENTAIRE_SLOT_ECART_Y  = 110

def get_slot_inventaire_rect(index):
    col = index % INVENTAIRE_SLOT_COLONNES
    row = index // INVENTAIRE_SLOT_COLONNES
    x = INVENTAIRE_SLOT_DEPART[0] + col * INVENTAIRE_SLOT_ECART_X
    y = INVENTAIRE_SLOT_DEPART[1] + row * INVENTAIRE_SLOT_ECART_Y
    return pygame.Rect(x, y, INVENTAIRE_SLOT_TAILLE, INVENTAIRE_SLOT_TAILLE)

def trouver_index_inventaire(item_id):
    for index, item in enumerate(inventaire):
        if item["id"] == item_id:
            return index
    return None

def inventaire_contient(item_id):
    return trouver_index_inventaire(item_id) is not None

def ajouter_objet_inventaire(item_id):
    if inventaire_contient(item_id):
        return False
    inventaire.append({"id": item_id})
    return True

def retirer_objet_inventaire(item_id):
    global inventaire_index_selectionne, tooltip_inventaire_visible
    index = trouver_index_inventaire(item_id)
    if index is None:
        return
    del inventaire[index]
    if inventaire_index_selectionne is not None:
        if inventaire_index_selectionne == index:
            inventaire_index_selectionne = None
            tooltip_inventaire_visible = False
        elif inventaire_index_selectionne > index:
            inventaire_index_selectionne -= 1

def ajouter_vie():
    global vies
    if vies < 3:
        vies += 1
        sfx.viesfx.play()

def dessiner_texte_contour(surface, font, texte, x, y, couleur_texte, couleur_contour, epaisseur=3):
    texte_surface   = font.render(texte, True, couleur_texte)
    contour_surface = font.render(texte, True, couleur_contour)
    texte_rect = texte_surface.get_rect(topright=(x, y))
    for ox in range(-epaisseur, epaisseur + 1):
        for oy in range(-epaisseur, epaisseur + 1):
            if ox == 0 and oy == 0:
                continue
            surface.blit(contour_surface, texte_rect.move(ox, oy))
    surface.blit(texte_surface, texte_rect)

def synchroniser_bottes_double_saut():
    global bottes_equipees
    if joueur.double_saut:
        ajouter_objet_inventaire("bottes")
        bottes_equipees = True
    elif bottes_equipees:
        bottes_equipees = False

def synchroniser_couteau():
    global couteau_equipee
    if joueur.couteau_equipee:
        ajouter_objet_inventaire("couteau")
        couteau_equipee = True
    else:
        couteau_equipee = False

def synchroniser_cles_finales():
    global cle_caronte_equipee, cle_enfer_equipee
    if cle_caronte_equipee and not inventaire_contient("cle_caronte"):
        ajouter_objet_inventaire("cle_caronte")
    if cle_enfer_equipee and not inventaire_contient("cle_enfer"):
        ajouter_objet_inventaire("cle_enfer")
    if not cle_caronte_equipee and inventaire_contient("cle_caronte"):
        cle_caronte_equipee = False
    if not cle_enfer_equipee and inventaire_contient("cle_enfer"):
        cle_enfer_equipee = False

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
    for son in (sfx.musiquefond, sfx.degat, sfx.viesfx, sfx.sfxtitre, sfx.fin,
                sfx.liresfx, sfx.stoplire, sfx.ouvrir_inv, sfx.fermer_inv,
                sfx.selectsfx, sfx.pausesfxouvrir, sfx.pausesfxfermer,
                sfx.pausesfxbutton, sfx.sfxnpc, sfx.dialogue_csfx, sfx.carontesfx,
                sfxmarche1, sfxmarche2, sfxmarche3, sauter, tombersfx,
                sfx.musiquefond, sfx.niveau_2caronte):
        son.stop()

def reset():
    global etat_global
    # Relancer l'initialisation complète remet tout à zéro
    initialiser_jeu()
    # Remettre la musique fond si activée
    if settings.musique:
        sfx.musiquefond.set_volume(0.1)
        if sfx.musiquefond.get_num_channels() == 0:
            sfx.musiquefond.play(-1)
    pygame.mixer.unpause()

# ============================================================
# BOUCLE PRINCIPALE UNIQUE
# ============================================================
running = True

while running:
    clock.tick(60)
    current_time = pygame.time.get_ticks()
    mouse_pos    = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    # --------------------------------------------------------
    # ÉTAT : MENU
    # --------------------------------------------------------
    if etat_global == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if not intro:
                    afficher_parametres_menu = False
            elif event.type == pygame.KEYDOWN and intro:
                intro = False  # ← n'importe quelle touche skip l'intro
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if intro:
                    intro = False  # ← clic souris skip aussi
                elif afficher_parametres_menu:
                    if fermer_menu_rect.collidepoint(event.pos):
                        afficher_parametres_menu = False
                        sfxboutton.play()
                    else:
                        for parametre in parametres_toggles_menu:
                            if parametre["rect"].collidepoint(event.pos):
                                parametre["enabled"] = not parametre["enabled"]
                                appliquer_parametre_jeu(parametre["name"], parametre["enabled"])
                                # Synchroniser aussi la musique menu
                                if parametre["name"] == "musique":
                                    if parametre["enabled"]:
                                        sfx.musiquemenu.set_volume(0.5)
                                        if sfx.musiquemenu.get_num_channels() == 0:
                                            sfx.musiquemenu.play(-1, 0, 3000)
                                    else:
                                        sfx.musiquemenu.set_volume(0)
                                sfxboutton.play()
                                break

        if intro:
            screen.fill((0, 0, 0))
            screen.blit(titre_logo_menu, titre_menu_rect)
            if current_time - intro_start >= INTRO_DURATION:
                intro = False
            screen.blit(curseur_img, mouse_pos)
            pygame.display.flip()
            continue

        # Boutons menu (détection clic dans la boucle d'events faite, ici on gère l'action)
        if not afficher_parametres_menu:
            for btn in buttons_menu:
                if btn.is_clicked(mouse_pos, mouse_pressed):
                    pygame.time.delay(200)
                    if btn.action == "play":
                        sfxboutton.play()
                        time.sleep(0.3)
                        sfx.musiquemenu.stop()
                        # Initialiser le jeu et basculer
                        initialiser_jeu()
                        if settings.musique:
                            sfx.musiquefond.set_volume(0.1)
                            sfx.musiquefond.play(-1)
                        etat_global = "jeu"
                    elif btn.action == "code":
                        sfxboutton.play()
                        time.sleep(0.3)
                        pygame.quit()
                        subprocess.run(["python", "codesauv.py"])
                        sys.exit()
                    elif btn.action == "settings":
                        sfxboutton.play()
                        afficher_parametres_menu = True
                    elif btn.action == "quit":
                        sfxboutton.play()
                        time.sleep(0.3)
                        running = False

        # Rendu menu
        screen.fill((0, 0, 0))
        screen.blit(BG, (0, 0))
        screen.blit(LOGO, logo_rect)
        for btn in buttons_menu:
            btn.draw(screen, mouse_pos)
        screen.blit(bouton_menu_img, bouton_menu_img_rect)

        if afficher_parametres_menu:
            overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 0))
            screen.blit(parametre_gui_menu, parametre_gui_menu_rect)
            screen.blit(fermer_menu, fermer_menu_rect)
            screen.blit(Police_parametre_menu.render("musique",  True, Blanc), (270, 170))
            screen.blit(Police_parametre_menu.render("speedrun (recommencer pour prendre effet)", True, Blanc), (270, 270))
            screen.blit(Police_parametre_menu.render("sfx", True, Blanc), (270, 370))
            for p in parametres_toggles_menu:
                screen.blit(activer_menu if p["enabled"] else desactiver_menu, p["rect"])

        screen.blit(curseur_img, mouse_pos)
        pygame.display.flip()
        continue

    # --------------------------------------------------------
    # ÉTAT : JEU
    # --------------------------------------------------------

    # Raccourcis locaux pour les items inventaire (dépendent des images chargées)
    ITEMS_INVENTAIRE = {
        "bottes":     {"image": bottes_img,      "nom": "Bottes",              "utilisable": True,  "action_label": lambda: "Desequiper" if bottes_equipees else "Equiper"},
        "potion_vie": {"image": potion_vie_img,   "nom": "Potion de vie",       "utilisable": False, "action_label": lambda: "Utiliser" if vies < 3 else None},
        "couteau":    {"image": couteau_img,      "nom": "Couteau",             "utilisable": True,  "action_label": lambda: "Desequiper" if couteau_equipee else "Equiper"},
        "cle_caronte":{"image": cle_caronte_img,  "nom": "Cle noire de Caronte","utilisable": True,  "action_label": lambda: "Desequiper" if cle_caronte_equipee else "Equiper"},
        "cle_enfer":  {"image": cle_enfer_img,    "nom": "Cle de l'enfer",      "utilisable": True,  "action_label": lambda: "Desequiper" if cle_enfer_equipee else "Equiper"},
    }

    if not joueur.peut_bouger and current_time - start_time >= 500 and etat == "jeu":
        if not (dialogue_g or dialogue_v or dialogue_v2 or dialogue_c1 or dialogue_caronte or dialogue_caronte_fin
                or choix_active or message_reponse_active or lire_pancarte or inventaire_affiche
                or caronte_aide or fin_caronte_declenchee or transition_caronte_fin_start):
            joueur.peut_bouger = True

    synchroniser_bottes_double_saut()
    synchroniser_couteau()
    synchroniser_cles_finales()

    button_offset = int(math.sin(current_time * 0.01) * 3) if not en_pause else 0

    # Bulles monstres niveau 2
    if (niveau_actuel == 2 and bateau_reparer and not en_pause
            and not fin_caronte_declenchee and len(monstres_niveau2) >= 1 and etat != "mort" and etat != "game_over"):
        if not bulle_monstre_actif:
            if current_time - bulle_monstre_timer > bulle_monstre_prochain:
                types_vivants = [getattr(m, "type_monstre", "monstre") for m in monstres_niveau2]
                if types_vivants:
                    bulle_monstre_type = types_vivants[random.randint(0, len(types_vivants) - 1)]
                    if bulle_monstre_type == "monstre":
                        bulle_monstre_texte = BULLES_TEXTES_MONSTRE
                        sfx.dialogue_csfx.play(0, 0, BULLE_DUREE)
                    elif bulle_monstre_type == "esprit":
                        bulle_monstre_texte = BULLES_TEXTES_ESPRIT
                        sfx.sfxnpc.play(0, 0, BULLE_DUREE)
                    else:
                        bulle_monstre_texte = BULLES_TEXTES_SQUELETTE
                        sfx.carontesfx.play(0, 0, BULLE_DUREE)
                    bulle_monstre_actif    = True
                    bulle_monstre_debut    = current_time
                    bulle_monstre_timer    = current_time
                    bulle_monstre_prochain = random.randint(12000, 15000)
        else:
            if current_time - bulle_monstre_debut > BULLE_DUREE:
                bulle_monstre_actif = False
                sfx.dialogue_csfx.stop(); sfx.sfxnpc.stop(); sfx.carontesfx.stop()

    if niveau_actuel == 1:
        if joueur.rect.x < 2000:
            porte_rect = porte.get_rect(topleft=(300, 320))
        else:
            porte_rect = porte.get_rect(topleft=(2000, 5970))
        active_porte        = joueur.rect.colliderect(porte_rect)
        active              = joueur.rect.colliderect(giordano_rect)
        active2             = joueur.rect.colliderect(virgilio_rect)
        active3             = joueur.rect.colliderect(condamne1_rect)
        active4             = joueur.rect.colliderect(caronte_rect)
        pancarte_active     = joueur.rect.colliderect(panneau_rect) and not panneau_button_hidden
        active_porte_finale = joueur.rect.colliderect(porte_finale_rect)
        active_v2           = joueur.rect.colliderect(virgilio2_rect) and not virgilio2_dialogue_fait
    else:
        active = active2 = active3 = active4 = active_porte = active_porte_finale = False
        pancarte_active = False
        active_rame = joueur.rect.colliderect(rame_interaction_rect)
        donner_rame = joueur.rect.colliderect(caronte2[0])

    # Animation Giordano
    if not giordano_pause:
        if giordano_forward:
            if current_giordano == 0 and current_time - giordano_anim_timer > 500:
                current_giordano = 1; giordano_anim_timer = current_time
            elif current_giordano == 1 and current_time - giordano_anim_timer > 500:
                current_giordano = 2; giordano_anim_timer = current_time
            elif current_giordano == 2 and current_time - giordano_anim_timer > 500:
                giordano_pause = True; giordano_pause_timer = current_time
        else:
            if current_giordano == 1 and current_time - giordano_anim_timer > 500:
                current_giordano = 0; giordano_anim_timer = current_time
            elif current_giordano == 0 and current_time - giordano_anim_timer > 500:
                giordano_pause = True; giordano_pause_timer = current_time
    else:
        if current_time - giordano_pause_timer > 500:
            if giordano_forward and current_giordano == 2:
                giordano_forward = False; current_giordano = 1; giordano_anim_timer = current_time
            elif not giordano_forward and current_giordano == 0:
                giordano_forward = True; current_giordano = 1; giordano_anim_timer = current_time
            giordano_pause = False

    # ---- Événements jeu ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if transition_recommencer or transition_porte_enfer_start or transition_caronte_fin_start or transition_fin_active:
            continue

        if etat == "game_over" and event.type == pygame.MOUSEBUTTONDOWN:
            if bouton_menu_go.collidepoint(event.pos):
                sfxboutton.play()
                sfx.musiquefond.stop()
                sfx.niveau_2caronte.stop()
                # Retour au menu
                etat_global = "menu"
                afficher_parametres_menu = False
                if settings.musique:
                    sfx.musiquemenu.set_volume(0.5)
                    sfx.musiquemenu.play(-1, 0, 3000)
            elif bouton_quitter.collidepoint(event.pos):
                sfxboutton.play(); time.sleep(0.3); running = False
            elif bouton_rejouer.collidepoint(event.pos):
                reset()
            continue

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if en_pause:
                    pass
                if joueur.peut_bouger and joueur.double_saut and joueur.nb_sauts == 1 and not jump_key_held:
                    jump_key_held = True
                    joueur.vel_y  = joueur.jump_force
                    joueur.nb_sauts = 2
                    joueur.demarrer_animation_saut()
                    sauter.play()
                    joueur.timer_chute    = pygame.time.get_ticks()
                    joueur.chute_son_joue = False
                    tombersfx.stop(); tombersfx.set_volume(0)
                    joueur.double_jump_effects.append({'x': joueur.rect.centerx, 'y': joueur.rect.y + 150, 'alpha': 255, 'width': 120, 'height': 7})

            if event.key == pygame.K_ESCAPE and pause_active:
                if afficher_parametres_pause:
                    afficher_parametres_pause = False
                    sfx.retoursfx.play()
                else:
                    en_pause = not en_pause
                    joueur.peut_bouger = not (en_pause or lire_pancarte or inventaire_affiche or dialogue_g or dialogue_v or dialogue_c1 or dialogue_caronte)
                    if en_pause:
                        mettre_speedrun_en_pause(current_time)
                        joueur.mettre_en_pause(current_time)
                        pygame.mixer.pause()
                        sfx.pausesfxouvrir.play()
                        pause_hover_index = pause_selected
                    else:
                        reprendre_speedrun_apres_pause(current_time)
                        joueur.reprendre_apres_pause(current_time)
                        pygame.mixer.unpause()
                        sfx.pausesfxfermer.play()

            if en_pause and not afficher_parametres_pause:
                if event.key == pygame.K_DOWN:
                    ancien = pause_selected
                    pause_selected = (pause_selected + 1) % len(boutons_pause)
                    if pause_selected != ancien: sfx.pausesfxbutton.play(); pause_hover_index = pause_selected
                if event.key == pygame.K_UP:
                    ancien = pause_selected
                    pause_selected = (pause_selected - 1) % len(boutons_pause)
                    if pause_selected != ancien: sfx.pausesfxbutton.play(); pause_hover_index = pause_selected
                if event.key == pygame.K_RETURN:
                    action = boutons_pause[pause_selected]["action"]
                    sfx.choisirsfx.play()
                    if action == "reprendre":
                        en_pause = False
                        joueur.peut_bouger = not (lire_pancarte or inventaire_affiche or dialogue_g or dialogue_v or dialogue_c1 or dialogue_caronte)
                        reprendre_speedrun_apres_pause(current_time)
                        joueur.reprendre_apres_pause(current_time)
                        pygame.mixer.unpause()
                        sfx.pausesfxfermer.play()
                    elif action == "menu":
                        sfx.musiquefond.stop(); sfx.niveau_2caronte.stop()
                        etat_global = "menu"
                        afficher_parametres_menu = False
                        if settings.musique:
                            sfx.musiquemenu.set_volume(0.5)
                            sfx.musiquemenu.play(-1, 0, 3000)
                    elif action == "quitter":
                        running = False
                    elif action == "parametres":
                        afficher_parametres_pause = True
                    elif action == "recommencer":
                        transition_recommencer = True; transition_start = current_time

            if event.key == pygame.K_e and caronte_aide:
                if not message_caronte_rame_done:
                    message_caronte_rame_counter = speed * len(message_caronte_rame)
                    sfx.carontesfx.stop()
                else:
                    caronte_aide = False; caronte_rame_dialogue_fait = True; joueur.peut_bouger = True

            if event.key == pygame.K_e and not rame_ramasser and active_rame:
                rame_ramasser = True; sfx.liresfx.play()
            if event.key == pygame.K_e and rame_ramasser and donner_rame and not bateau_reparer:
                niveau2_bg_offset = current_time - freeze_bg
                bateau_reparer = True; rame_ramasser = False; ajouter_vie()
                if palier_bateau_index >= len(paliers_bateau) - 1 and nombre_de_monstre >= paliers_bateau[-1]:
                    fin_caronte_declenchee = True; joueur.peut_bouger = False
                    inventaire_affiche = False
                    transition_caronte_fin_start = current_time + 1000
                elif palier_bateau_index < len(paliers_bateau):
                    palier_bateau_index += 1

        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            jump_key_held = False

        if event.type not in (pygame.KEYDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            continue
        if event.type == pygame.KEYDOWN and en_pause:
            continue
        if event.type == pygame.KEYDOWN and inventaire_affiche and event.key != pygame.K_f:
            continue

        if event.type == pygame.KEYDOWN:
            if niveau_actuel == 1:
                if event.key == pygame.K_e and dialogue_g:
                    if not done:
                        counter = speed * len(message); sfx.sfxnpc.stop()
                    else:
                        if active_message < len(messages) - 1:
                            active_message += 1; message = messages[active_message]; counter = 0; done = False
                        else:
                            dialogue_g = False; done = False; active_message = 0; counter = 0
                            joueur.peut_bouger = True; giordano_dialogue_cooldown = current_time
                            if messages is MESSAGES_GIORDANO_POST_CARONTE:
                                giordano_post_caronte_fait = True
                                if not inventaire_contient("cle_enfer"):
                                    cle_enfer_equipee = True; ajouter_objet_inventaire("cle_enfer"); sfx.objetsfx.play()
                            else:
                                if current_time - giordano_cooldown > duree_cooldown:
                                    giordano_cooldown = current_time; ajouter_vie()

                elif event.key == pygame.K_e and active and not dialogue_g:
                    if current_time - giordano_dialogue_cooldown > duree_dialogue_cooldown:
                        dialogue_g = True; joueur.peut_bouger = False; counter = 0; active_message = 0
                        if not giordano_post_caronte_fait and not inventaire_contient("cle_enfer") and caronte_niveau2_termine:
                            messages = MESSAGES_GIORDANO_POST_CARONTE
                        else:
                            messages = list(MESSAGES_GIORDANO_NORMAL)
                        message = messages[0]

                elif event.key == pygame.K_e and dialogue_v:
                    if not done:
                        counter = speed * len(message2); sfx.sfxnpc.stop()
                    else:
                        if active_message2 < len(message_v) - 1:
                            active_message2 += 1; message2 = message_v[active_message2]; counter = 0; done = False
                        else:
                            dialogue_v = False; done = False; active_message2 = 0; counter = 0
                            joueur.peut_bouger = True; virgilio_dialogue_cooldown = current_time
                            if not inventaire_contient("bottes"):
                                ajouter_objet_inventaire("bottes"); sfx.objetsfx.play()
                            if current_time - virgilio_cooldown > duree_cooldown and vies < 3:
                                virgilio_cooldown = current_time; ajouter_vie()

                elif event.key == pygame.K_e and active2 and not dialogue_v:
                    if current_time - virgilio_dialogue_cooldown > duree_dialogue_cooldown:
                        dialogue_v = True; joueur.peut_bouger = False; counter = 0; active_message2 = 0; message2 = message_v[0]

                elif event.key == pygame.K_e and dialogue_v2:
                    if not done:
                        counter = speed * len(message_v2_actuel); sfx.sfxnpc.stop()
                    else:
                        if active_message_v2 < len(message_v2) - 1:
                            active_message_v2 += 1; message_v2_actuel = message_v2[active_message_v2]; counter = 0; done = False
                        else:
                            dialogue_v2 = False; done = False; active_message_v2 = 0; counter = 0
                            joueur.peut_bouger = True; virgilio2_dialogue_fait = True
                            porte_enfer_ouverte = True; sfx.debloquer_porte.play()
                            virgilio2_dialogue_cooldown = current_time

                elif event.key == pygame.K_e and active_v2 and not dialogue_v2:
                    if current_time - virgilio2_dialogue_cooldown > duree_dialogue_cooldown:
                        dialogue_v2 = True; joueur.peut_bouger = False; counter = 0; active_message_v2 = 0; message_v2_actuel = message_v2[0]

                elif event.key == pygame.K_e and dialogue_c1:
                    if not done:
                        counter = speed * len(message3); sfx.dialogue_csfx.stop()
                    else:
                        if active_message_c1 < len(message_c1) - 1:
                            active_message_c1 += 1; message3 = message_c1[active_message_c1]; counter = 0; done = False
                        else:
                            dialogue_c1 = False; done = False; active_message_c1 = 0; counter = 0; joueur.peut_bouger = True
                            if not inventaire_contient("couteau"):
                                ajouter_objet_inventaire("couteau"); sfx.objetsfx.play(); condamne1_dialogue_cooldown = current_time

                elif event.key == pygame.K_e and active3 and not dialogue_c1:
                    if current_time - condamne1_dialogue_cooldown > duree_dialogue_cooldown:
                        dialogue_c1 = True; joueur.peut_bouger = False; counter = 0; active_message_c1 = 0; message3 = message_c1[0]

                elif event.key == pygame.K_e and dialogue_caronte:
                    if not done:
                        counter = speed * len(message4); sfx.carontesfx.stop()
                    else:
                        if active_message_caronte < len(message_caronte) - 1:
                            active_message_caronte += 1; message4 = message_caronte[active_message_caronte]; counter = 0; done = False
                        else:
                            dialogue_caronte = False; done = False; active_message_caronte = 0; counter = 0; choix_active = True

                elif event.key == pygame.K_1 and choix_active:
                    choix_active = False; choix_fait = 1
                    message_reponse_active = True; message_reponse_index = 0; message_reponse_counter = 0; message_reponse_done = False; joueur.peut_bouger = False

                elif event.key == pygame.K_2 and choix_active:
                    choix_active = False; choix_fait = 2
                    message_reponse_active = True; message_reponse_index = 1; message_reponse_counter = 0; message_reponse_done = False; joueur.peut_bouger = False

                elif event.key == pygame.K_e and message_reponse_active:
                    if not message_reponse_done:
                        message_reponse_counter = speed * len(message5[message_reponse_index]); sfx.carontesfx.stop()
                    else:
                        message_reponse_active = False; joueur.peut_bouger = True
                        if choix_fait == 1:
                            transition_caronte_start = current_time; transition_caronte_teleporte = False; joueur.peut_bouger = False
                        caronte_dialogue_cooldown = current_time; choix_fait = None

                elif event.key == pygame.K_e and active4 and not dialogue_caronte and not dialogue_caronte_fin and not choix_active and not message_reponse_active:
                    if current_time - caronte_dialogue_cooldown > duree_dialogue_cooldown:
                        if caronte_niveau2_termine:
                            # Dialogue post-niveau 2 : remerciement simple sans proposition
                            dialogue_caronte_fin = True  # On réutilise ce dialogue pour afficher un message simple
                            joueur.peut_bouger = False
                            counter = 0
                            active_message_caronte = 0
                            message4 = message_caronte_post_niveau2[0]
                            message_caronte_fin = message_caronte_post_niveau2  # Temporairement remplacer pour ce dialogue
                            done = False
                        else:
                            dialogue_caronte = True
                            joueur.peut_bouger = False
                            counter = 0
                            active_message_caronte = 0
                            message4 = message_caronte[0]
                            done = False

                elif event.key == pygame.K_e and dialogue_caronte_fin:
                    if not done:
                        counter = speed * len(message4); sfx.carontesfx.stop()
                    else:
                        if active_message_caronte < len(message_caronte_fin) - 1:
                            active_message_caronte += 1; message4 = message_caronte_fin[active_message_caronte]; counter = 0; done = False
                        else:
                            dialogue_caronte_fin = False; active_message_caronte = 0; counter = 0; done = False; joueur.peut_bouger = True
                            if not inventaire_contient("cle_caronte"):
                                ajouter_objet_inventaire("cle_caronte"); cle_caronte_equipee = True; sfx.objetsfx.play()
                elif event.key == pygame.K_e and pancarte_active and not lire_pancarte:
                    lire_pancarte = True
                    pancarte_timer = current_time
                    show_button_e_pancarte = False
                    joueur.peut_bouger = False
                    panneau_button_hidden = True
                    panneau_button_timer = current_time
                    sfx.liresfx.play()

                elif event.key == pygame.K_e and lire_pancarte and show_button_e_pancarte:
                    lire_pancarte = False
                    show_button_e_pancarte = False
                    joueur.peut_bouger = True
                    sfx.stoplire.play()
                elif event.key == pygame.K_e and active_porte:
                    if joueur.rect.x < 2000:
                        if porte_enfer_ouverte:
                            porte_enfer_origine_x = 100; transition_porte_enfer_start = current_time; joueur.peut_bouger = False; sfx.porte_entrer.play()
                        else:
                            message_porte_fermee_timer = current_time; sfx.indicesfx.play()
                    else:
                        porte_enfer_origine_x = 9999; transition_porte_enfer_start = current_time; sfx.porte_entrer.play(); joueur.peut_bouger = False

                elif event.key == pygame.K_e and active_porte_finale:
                    if porte_finale_prete:
                        transition_fin_active = True; transition_fin_start = current_time; transition_fin_phase = 0
                        joueur.peut_bouger = False; inventaire_affiche = False; pause_active = False
                    elif not cle_caronte_equipee and not cle_enfer_equipee:
                        message_cle_timer = current_time; message_cle_actif = True; sfx.indicesfx.play()
                    else:
                        if inventaire_contient("cle_caronte") and cle_caronte_equipee and not porte_cle_caronte_utilisee:
                            porte_cle_caronte_utilisee = True; retirer_objet_inventaire("cle_caronte"); cle_caronte_equipee = False; sfx.objetsfx.play()
                        elif cle_enfer_equipee and not porte_cle_enfer_utilisee:
                            porte_cle_enfer_utilisee = True; retirer_objet_inventaire("cle_enfer"); cle_enfer_equipee = False; sfx.objetsfx.play()
                        if porte_cle_caronte_utilisee and porte_cle_enfer_utilisee:
                            porte_finale_prete = True
                elif porte_finale_prete:
                    transition_fin_active = True; transition_fin_start = current_time; transition_fin_phase = 0
                    joueur.peut_bouger = False; inventaire_affiche = False; pause_active = False

            if (event.key == pygame.K_f and inventaire_active and not inventaire_affiche
                    and not lire_pancarte and not dialogue_g and not dialogue_v
                    and not dialogue_c1 and not dialogue_caronte and not dialogue_caronte_fin
                    and not choix_active and not message_reponse_active and not fin_caronte_declenchee
                    and not caronte_aide):
                sfx.ouvrir_inv.play(); inventaire_affiche = True; joueur.peut_bouger = False
                inventaire_timer = current_time; show_button_f_inventaire = False
            elif event.key == pygame.K_f and inventaire_affiche:
                sfx.fermer_inv.play(); inventaire_affiche = False; show_button_f_inventaire = False
                tooltip_inventaire_visible = False; inventaire_index_selectionne = None; joueur.peut_bouger = True
                if invincible:
                    invincibilite_temps = current_time - duree_invincibilite + 500  # laisse 500ms de clignotement puis s'arrête

        if event.type == pygame.MOUSEMOTION and en_pause and not afficher_parametres_pause:
            mx, my = event.pos
            for i, bouton in enumerate(boutons_pause):
                y_b = 280 + i * 80; x_b = screen_width // 2 - pause_button_width // 2
                if pygame.Rect(x_b, y_b, pause_button_width, pause_button_height).collidepoint(mx, my):
                    if pause_hover_index != i: sfx.pausesfxbutton.play()
                    pause_selected = i; pause_hover_index = i

        if event.type == pygame.MOUSEBUTTONDOWN:
            if afficher_parametres_pause:
                if fermer_pause_rect.collidepoint(event.pos):
                    afficher_parametres_pause = False; sfx.retoursfx.play()
                else:
                    for parametre in parametres_toggles_pause:
                        if parametre["rect"].collidepoint(event.pos):
                            parametre["enabled"] = not parametre["enabled"]
                            appliquer_parametre_jeu(parametre["name"], parametre["enabled"])
                            sfx.pausesfxbutton.play(); break
            elif en_pause:
                mx, my = event.pos
                for i, bouton in enumerate(boutons_pause):
                    y_b = 280 + i * 80; x_b = screen_width // 2 - pause_button_width // 2
                    if pygame.Rect(x_b, y_b, pause_button_width, pause_button_height).collidepoint(mx, my):
                        action = bouton["action"]; sfx.choisirsfx.play()
                        if action == "reprendre":
                            en_pause = False
                            joueur.peut_bouger = not (lire_pancarte or inventaire_affiche or dialogue_g or dialogue_v or dialogue_c1 or dialogue_caronte)
                            reprendre_speedrun_apres_pause(current_time); joueur.reprendre_apres_pause(current_time)
                            pygame.mixer.unpause(); sfx.pausesfxfermer.play()
                        elif action == "menu":
                            sfx.musiquefond.stop(); sfx.niveau_2caronte.stop()
                            en_pause = False; etat_global = "menu"
                            if settings.musique:
                                sfx.musiquemenu.set_volume(0.5); sfx.musiquemenu.play(-1, 0, 3000)
                        elif action == "quitter":
                            running = False
                        elif action == "parametres":
                            afficher_parametres_pause = True
                        elif action == "recommencer":
                            transition_recommencer = True; transition_start = current_time
            else:
                if inventaire_affiche:
                    tooltip_clique = False
                    if tooltip_inventaire_visible and inventaire_index_selectionne is not None:
                        slot_rect = get_slot_inventaire_rect(inventaire_index_selectionne)
                        tooltip_equiper_rect = pygame.Rect(slot_rect.right + 10, slot_rect.y, 130, 40)
                        if tooltip_equiper_rect.collidepoint(event.pos):
                            tooltip_clique = True; sfx.selectsfx.play()
                            item_id = inventaire[inventaire_index_selectionne]["id"]
                            if item_id == "bottes": joueur.double_saut = not joueur.double_saut; bottes_equipees = joueur.double_saut
                            elif item_id == "couteau": joueur.couteau_equipee = not joueur.couteau_equipee; couteau_equipee = joueur.couteau_equipee
                            elif item_id == "cle_caronte": cle_caronte_equipee = not cle_caronte_equipee
                            elif item_id == "cle_enfer": cle_enfer_equipee = not cle_enfer_equipee
                            tooltip_inventaire_visible = False
                    if not tooltip_clique:
                        for index, item in enumerate(inventaire):
                            slot_rect = get_slot_inventaire_rect(index)
                            if slot_rect.collidepoint(event.pos):
                                sfx.selectsfx.play(); inventaire_index_selectionne = index
                                tooltip_inventaire_visible = ITEMS_INVENTAIRE[item["id"]]["utilisable"]; break

    keys = pygame.key.get_pressed()

    if not transition_recommencer and not transition_porte_enfer_start and not transition_fin_active:
        if not joueur.peut_bouger:
            joueur.is_animating = False
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            joueur.is_animating = True; joueur.facing_left = False
            if speedrun and not speedrun_started: speedrun_started = True; speedrun_start_time = current_time
        elif keys[pygame.K_q] or keys[pygame.K_LEFT]:
            joueur.is_animating = True; joueur.facing_left = True
            if speedrun and not speedrun_started: speedrun_started = True; speedrun_start_time = current_time
        else:
            joueur.is_animating = False

    if joueur.peut_bouger and joueur.est_au_sol(plateformes + plateformes_prison + sol) and not transition_fin_active:
        if keys[pygame.K_SPACE] and not ground_jump_consumed and not transition_porte_enfer_start and not transition_fin_active:
            ground_jump_consumed = True; jump_key_held = True
            joueur.vel_y = joueur.jump_force; joueur.nb_sauts = 1
            joueur.demarrer_animation_saut(); sauter.play()
        elif not keys[pygame.K_SPACE]:
            ground_jump_consumed = False; jump_key_held = False
    else:
        ground_jump_consumed = False

    if inventaire_affiche and not show_button_f_inventaire:
        show_button_f_inventaire = True
    if lire_pancarte and not show_button_e_pancarte and current_time - pancarte_timer > 3000:
        show_button_e_pancarte = True
    if panneau_button_hidden and current_time - panneau_button_timer > 2000:
        panneau_button_hidden = False

    for plat in plateformes_mobiles:
        old_x, old_y = plat.rect.x, plat.rect.y
        plat.update()
        dx_plat = plat.rect.x - old_x; dy_plat = plat.rect.y - old_y
        if (joueur.rect.bottom >= plat.rect.top and joueur.rect.bottom <= plat.rect.top + 15
                and joueur.rect.right > plat.rect.left and joueur.rect.left < plat.rect.right):
            joueur.rect.x += dx_plat; joueur.rect.y += dy_plat

    if not en_pause and not transition_recommencer and not transition_porte_enfer_start and etat not in ("mort", "game_over") and not transition_fin_active:
        if niveau_actuel == 1:
            rects_mobiles = [p.rect for p in plateformes_mobiles]
            joueur.deplacement(plateformes + plateformes_prison + sol + sol2 + mur2_rects + plateformes2 + rects_mobiles)
            joueur.appliquer_gravite(plateformes + plateformes_prison + sol + sol2 + mur2_rects + plateformes2 + rects_mobiles, murs=plateformes_haute)
            joueur.update_double_jump_effects()
            if not invincible:
                for plat_danger in plateformes_danger + plateformes_danger2:
                    if joueur.rect.colliderect(plat_danger):
                        vies -= 1; sfx.degat.play(); invincible = True; invincibilite_temps = current_time
                        if vies <= 0:
                            pause_active = False; inventaire_active = False; etat = "mort"
                            death_animation_start = current_time; death_sound_stage = 0
                            joueur.peut_bouger = False; joueur.is_animating = False; couper_sons_pour_mort(); break
            if invincible and current_time - invincibilite_temps > duree_invincibilite:
                invincible = False
            if monstre.vivant:
                vies, invincible, invincibilite_temps, mort = monstre.update_and_collide(
                    joueur, plateformes + plateformes_prison + sol + sol2 + plateformes_haute_m,
                    vies, invincible, current_time, invincibilite_temps, duree_invincibilite)
                if mort: sfx.degat.play()


        elif niveau_actuel == 2:
            sfx.musiquefond.stop()
            joueur.update_double_jump_effects()
            if bateau_reparer:
                joueur.deplacement(bateau_plat)
                joueur.appliquer_gravite(bateau_plat)
                if (palier_bateau_index < len(paliers_bateau)
                        and nombre_de_monstre >= paliers_bateau[palier_bateau_index]
                        and not caronte_aide and len(monstres_niveau2) == 0 and not fin_caronte_declenchee):
                    freeze_bg = current_time - niveau2_bg_offset
                    bateau_reparer = False; caronte_aide = True
                    message_caronte_rame_counter = 0; message_caronte_rame_done = False; joueur.peut_bouger = False

            if (not fin_caronte_declenchee and palier_bateau_index < len(paliers_bateau)
                    and current_time - dernier_spawn_monstre > spawn_delay
                    and nombre_de_monstre < paliers_bateau[palier_bateau_index]
                    and etat not in ("mort", "game_over")):
                choix_spawn = random.choice(["monstre", "esprit", "squelette"])
                if choix_spawn == "monstre":
                    m = Monstre(1250, 550); m.distance_activation = 1500; monstres_niveau2.append(m)
                elif choix_spawn == "esprit":
                    monstres_niveau2.append(Esprit(1250, 550))
                else:
                    monstres_niveau2.append(Squelette(1250, bateau_plat[4].top - 150))
                nombre_de_monstre += 1
                if nombre_de_monstre == 1: bulle_monstre_timer = current_time
                dernier_spawn_monstre = current_time
                spawn_delay = random.randint(4500, 5500)

            for m in monstres_niveau2[:]:
                if etat == "mort":  # ← ajouter ce guard
                    break
                vies, invincible, invincibilite_temps, mort = m.update_and_collide(
                    joueur, [bateau_plat[0], bateau_plat[4]], vies, invincible, current_time, invincibilite_temps, duree_invincibilite)
                if mort: sfx.degat.play()
                if not m.vivant:
                    nombre_monstres_tues += 1
                    type_m = getattr(m, "type_monstre", "monstre")
                    if type_m == "squelette": sons_squelette[random.randint(0, 2)].play()
                    else: sons_monstre[random.randint(0, 1)].play()
                    monstres_niveau2.remove(m)
                    if len(monstres_niveau2) == 0:
                        bulle_monstre_actif = False
                        sfx.dialogue_csfx.stop()
                        sfx.sfxnpc.stop()
                        sfx.carontesfx.stop()
            if vies <= 0 and etat != "mort":
                etat = "mort"; death_animation_start = current_time; death_sound_stage = 0
                joueur.peut_bouger = False; joueur.is_animating = False; couper_sons_pour_mort()
            if invincible and current_time - invincibilite_temps > duree_invincibilite: invincible = False
            if joueur.rect.top > chute_y:
                vies = 0; etat = "mort"; death_animation_start = current_time; death_sound_stage = 0
                joueur.peut_bouger = False; joueur.is_animating = False; couper_sons_pour_mort()

    if etat == "mort" and death_animation_done:
        etat = "game_over"
        monstres_niveau2.clear()
        bulle_monstre_actif = False
        sfx.fireballsfx.stop()
        sfx.dialogue_csfx.stop()
        sfx.sfxnpc.stop()
        sfx.carontesfx.stop()

    # GAME OVER
    if etat == "game_over":
        screen.blit(background_game_over, (0, 0))
        mouse_pos_go = pygame.mouse.get_pos()
        for rect, c_on, c_off in [(bouton_menu_go, (0,255,0),(0,200,0)), (bouton_quitter,(255,0,0),(200,0,0)), (bouton_rejouer,(0,255,0),(0,200,0))]:
            pygame.draw.rect(screen, c_on if rect.collidepoint(mouse_pos_go) else c_off, rect)
        screen.blit(police_grande.render("GAME OVER", True, (255,0,0)), (640 - police_grande.size("GAME OVER")[0]//2, 250))
        for surf, rect in [
            (police_petite.render("Menu Début", True, (255,255,255)), bouton_menu_go),
            (police_petite.render("Quitter",    True, (255,255,255)), bouton_quitter),
            (police_petite.render("Rejouer",    True, (255,255,255)), bouton_rejouer),
        ]:
            screen.blit(surf, (rect.centerx - surf.get_width()//2, rect.centery - surf.get_height()//2))
        screen.blit(curseur_img, mouse_pos_go)
        pygame.display.flip()
        continue

    # Camera
    if not en_pause:
        if niveau_actuel == 1:
            camera_x += (joueur.rect.centerx - screen_width//2 - camera_x) * 0.11
            if joueur.rect.centerx < 2000:
                camera_x = max(0, min(camera_x, 2000 - screen_width))
            else:
                camera_x = max(2000, min(camera_x, 4100 - screen_width))
            camera_y += (joueur.rect.centery - screen_height//2 + camera_y_offset - camera_y) * 0.11
            camera_y = max(0, camera_y)
        elif niveau_actuel == 2:
            camera_x += (joueur.rect.centerx - screen_width//2 - camera_x) * 0.11
            camera_x = max(0, camera_x)
            camera_y += (250 - camera_y) * 0.11

    if niveau_actuel == 1:
        bg_x = (-(camera_x - 2000) * parallax_factor + bg_offset_x - bg_width//2
                if joueur.rect.centerx >= 2000
                else -camera_x * parallax_factor + bg_offset_x)
        bg_y = -camera_y * parallax_factor + bg_offset_y
    elif niveau_actuel == 2:
        t_bg = (current_time - niveau2_bg_offset) if bateau_reparer else freeze_bg
        bg_x = (-camera_x * parallax_factor + bg_offset_x + (t_bg * -0.02)) % fond_caronte1.get_width()
        bg_y = -camera_y * parallax_factor + bg_offset_y

    # Animation mort
    if etat == "mort" and death_animation_start is not None:
        death_elapsed    = current_time - death_animation_start
        heart_travel_end  = DEATH_HEART_ON_PLAYER_MS + DEATH_HEART_TRAVEL_MS
        heart_hold_end    = heart_travel_end + DEATH_HEART_CENTER_HOLD_MS - DEATH_ANIMATION_SPEEDUP_MS
        hand_grab_end     = heart_hold_end + DEATH_HAND_GRAB_MS
        satan_enter_start = hand_grab_end + DEATH_HAND_EXIT_MS

        if death_sound_stage == 0: sfx.mortsfx.play(); death_sound_stage = 1
        elif death_sound_stage == 1 and death_elapsed >= heart_travel_end: sfx.coeursfx.play(); death_sound_stage = 2

        screen.fill((0, 0, 0))
        if death_elapsed < DEATH_HEART_ON_PLAYER_MS:
            screen.blit(coeurt_mort, coeurt_mort.get_rect(center=(joueur.rect.centerx - camera_x, joueur.rect.centery - camera_y)))
        elif death_elapsed < heart_travel_end:
            t = 1 - (1 - min((death_elapsed - DEATH_HEART_ON_PLAYER_MS) / DEATH_HEART_TRAVEL_MS, 1)) ** 3
            screen.blit(coeurt_mort, coeurt_mort.get_rect(center=(
                (joueur.rect.centerx - camera_x) + (screen_width//2 - (joueur.rect.centerx - camera_x)) * t,
                (joueur.rect.centery - camera_y) + (screen_height//2 - (joueur.rect.centery - camera_y)) * t,
            )))
        elif death_elapsed < heart_hold_end:
            screen.blit(coeurt_mort, coeurt_mort.get_rect(center=(screen_width//2, screen_height//2)))

        if death_elapsed >= DEATH_HAND_DELAY_MS:
            if death_elapsed < heart_hold_end:
                screen.blit(main1, main1.get_rect(center=(
                    (screen_width + main1.get_width()//2) + ((screen_width//2) - (screen_width + main1.get_width()//2))
                    * (1 - (1 - min((death_elapsed - DEATH_HAND_DELAY_MS) / DEATH_HAND_ENTER_MS, 1)) ** 3),
                    screen_height//2 - 50,
                )))
            elif death_elapsed < hand_grab_end:
                if death_sound_stage == 2:
                    sfx.coeursfx.stop(); sfx.coeurmort.set_volume(0.5); sfx.coeurmort.play(); death_sound_stage = 3
                screen.blit(main2, main2.get_rect(center=(screen_width//2, screen_height//2 - 50)))
            else:
                screen.blit(main2, main2.get_rect(center=(
                    screen_width//2 + (screen_width + main2.get_width()//2 - screen_width//2)
                    * min((death_elapsed - hand_grab_end) / DEATH_HAND_EXIT_MS, 1) ** 3,
                    screen_height//2 - 50,
                )))
                if death_elapsed >= satan_enter_start:
                    t = 1 - (1 - min((death_elapsed - satan_enter_start) / DEATH_SATAN_ENTER_MS, 1)) ** 3
                    img = satan1
                    if death_elapsed >= satan_enter_start + DEATH_SATAN_ENTER_MS:
                        if death_sound_stage == 3: sfx.satan.set_volume(0.5); sfx.satan.play(); death_sound_stage = 4
                        img = satan1 if ((death_elapsed - satan_enter_start - DEATH_SATAN_ENTER_MS) // 120) % 2 == 0 else satan2
                    screen.blit(img, img.get_rect(center=(
                        screen_width//2,
                        (-img.get_height()//2) + (220 + img.get_height()//2) * t - (15 if img == satan2 else 0),
                    )))
            if death_elapsed >= DEATH_GAME_OVER_DELAY_MS:
                death_animation_done = True
        pygame.display.flip()
        continue

    # ---- RENDU JEU ----
    if niveau_actuel == 1:
        screen.blit(background, (bg_x, bg_y + 100))  # ← background d'abord
        img_porte = porte_enfer_img_ouverte if porte_enfer_ouverte else porte
        if joueur.rect.x < 2000:
            screen.blit(img_porte, (300 - camera_x, 320 - camera_y))
        else:
            screen.blit(porte_enfer_img_ouverte, (2000 - camera_x, 5970 - camera_y))

        if porte_cle_caronte_utilisee and porte_cle_enfer_utilisee: img_pf = porte_finale_ouverte_img
        elif porte_cle_caronte_utilisee: img_pf = porte_finale_rouge
        elif porte_cle_enfer_utilisee:  img_pf = porte_finale_noir
        else: img_pf = porte_finale_bloquee
        screen.blit(img_pf, (porte_finale_rect.x - camera_x, porte_finale_rect.y - camera_y))

        screen.blit(panneau, (panneau_rect.x - camera_x, panneau_rect.y - camera_y))
        screen.blit(giordano_images[current_giordano], (giordano_rect.x - camera_x, giordano_rect.y - camera_y))
        screen.blit(virgilio, (virgilio_rect.x - camera_x, virgilio_rect.y - camera_y))
        screen.blit(condamne1, (condamne1_rect.x - camera_x, condamne1_rect.y - camera_y))
        screen.blit(caronte_npc, (caronte_rect.x - camera_x, caronte_rect.y - camera_y))
        screen.blit(bateau_deco, (bateau_rect.x - camera_x, bateau_rect.y - camera_y))
        screen.blit(virgilio, (virgilio2_rect.x - camera_x, virgilio2_rect.y - camera_y))

    elif niveau_actuel == 2:
        for calque, vitesse in [(fond_caronte4,0.1),(fond_caronte5,0.05),(fond_caronte3,0.35),(fond_caronte2,0.35),(fond_caronte_eau,1),(fond_caronte1,0.6)]:
            t_cal = (current_time - niveau2_bg_offset) if bateau_reparer else freeze_bg
            ox = (-camera_x * vitesse + (t_cal * -0.02 * vitesse / 0.5)) % calque.get_width()
            screen.blit(calque, (ox - calque.get_width(), bg_y + 100))
            screen.blit(calque, (ox, bg_y + 100))

    if monstre.vivant: monstre.draw(screen, camera_x, camera_y)

    if joueur.couteau_equipee and not en_pause:
        temps_ecoule = pygame.time.get_ticks() - joueur.cooldown_attaque
        if temps_ecoule < 2500:
            frame_cd = min(int(temps_ecoule / 500), 4)
            img_cd = pygame.transform.scale(pygame.image.load(f"images/cooldown/cooldown{frame_cd}.png").convert_alpha(), (51, 15))
            screen.blit(img_cd, (joueur.rect.x - camera_x, joueur.rect.y - camera_y - 70))

    afficher_joueur = True
    if invincible: afficher_joueur = (current_time // 100) % 2 == 0
    if afficher_joueur:
        sprite_offset_x = joueur.draw_offset_x_left if joueur.facing_left else joueur.draw_offset_x
        sprite_x = joueur.rect.centerx - camera_x - joueur.image.get_width()//2 + sprite_offset_x
        sprite_y = joueur.rect.bottom  - camera_y - joueur.image.get_height() + joueur.draw_offset_y
        screen.blit(joueur.image, (sprite_x, sprite_y))

    if niveau_actuel == 1:
        for mur, img in zip(plateformes_prison, mur_prison_images): screen.blit(img, (mur.x - camera_x, mur.y - camera_y))
        for plat, img in zip(plateformes, platform_images):
            if img: screen.blit(img, (plat.x - camera_x, plat.y - camera_y))
        for plat in plateformes_mobiles:
            if plateforme_petite_orig:
                screen.blit(pygame.transform.scale(plateforme2_img, (plat.rect.width, plat.rect.height)), (plat.rect.x - camera_x, plat.rect.y - camera_y))
        for s, img in zip(sol2, sol2_images): screen.blit(img, (s.x - camera_x, s.y - camera_y))
        for s, img in zip(plateformes2, plateforme2_images):
            if img: screen.blit(img, (s.x - camera_x, s.y - camera_y))
        for s, img in zip(sol, sol_images): screen.blit(img, (s.x - camera_x, s.y - camera_y - 15))
        for s, img in zip(mur2_rects, mur2_images):
            if img: screen.blit(img, (s.x - camera_x, s.y - camera_y))
        for plat, img in zip(plateformes_danger, pic_sol_images): screen.blit(img, (plat.x - camera_x, plat.y - camera_y))
        for plat, img in zip(plateformes_danger2, pic_plafond_images): screen.blit(img, (plat.x - camera_x, plat.y - camera_y))
        for ph in plateformes_haute:
            pygame.draw.rect(screen, (0,0,0), (ph.x - camera_x, ph.y - camera_y, ph.width, ph.height))
        if pancarte_active and not lire_pancarte:
            screen.blit(bouton_e, (bouton_e_rect.x - camera_x - 700, bouton_e_rect.y - camera_y + button_offset))
        if active_porte_finale and not (porte_cle_caronte_utilisee and porte_cle_enfer_utilisee):
            screen.blit(bouton_e, (porte_finale_rect.x - camera_x + porte_finale_rect.width//2 + 200, porte_finale_rect.y - camera_y + 300 + button_offset))

    if niveau_actuel == 2:
        if not en_pause:
            img_bateau = bateau_image if (current_time // 500) % 2 == 0 else bateau_image2
            for i, plat in enumerate(bateau_plat):
                if i == 0:
                    img_b = bateau_rame_casse if not bateau_reparer else img_bateau[i]
                    screen.blit(img_b, (plat.x - camera_x, plat.y - camera_y - 100))
        for m in monstres_niveau2:
            if not en_pause and etat not in ("mort", "game_over"):
                m.draw(screen, camera_x, camera_y)

        if caronte_aide:
            bateau_reparer = False; rame_ramasser = False
            joueur.peut_bouger = False; joueur.is_animating = False
            if not en_pause and message_caronte_rame_counter < speed * len(message_caronte_rame):
                message_caronte_rame_counter += 1
                if message_caronte_rame_counter % speed == 0 and sfx.carontesfx.get_num_channels() == 0:
                    sfx.carontesfx.play()
            elif message_caronte_rame_counter >= speed * len(message_caronte_rame):
                sfx.carontesfx.stop(); message_caronte_rame_done = True
                screen.blit(bouton_e, (1020, 550 + button_offset))

        if not bateau_reparer:
            bateau_plat_reparer = [bateau_plat[0], bateau_plat[1], bateau_plat[3], bateau_plat[5]]
            joueur.deplacement(bateau_plat_reparer + niveau2_plat)
            joueur.appliquer_gravite(bateau_plat_reparer + niveau2_plat)
            if not rame_ramasser:
                screen.blit(rame_casse, (rame_casse_plat.x - camera_x + 100, rame_casse_plat.y - camera_y))
                if active_rame:
                    screen.blit(bouton_e, (rame_casse_plat.x - camera_x + 20, rame_casse_plat.y - camera_y + button_offset - 20))
        if rame_ramasser and donner_rame and not bateau_reparer:
            screen.blit(bouton_e, (sol_bateau.centerx - camera_x - 25, sol_bateau.y - camera_y - 70 + button_offset))
        for s, img in zip(niveau2_plat, niveau2_images):
            if img and not bateau_reparer: screen.blit(img, (s.x - camera_x, s.y - camera_y))

    for effect in joueur.double_jump_effects:
        ef_surf = pygame.Surface((effect['width'], effect['height']), pygame.SRCALPHA)
        ef_surf.fill((255, 255, 255, effect['alpha']))
        screen.blit(ef_surf, (effect['x'] - camera_x - effect['width']//2, effect['y'] - camera_y))

    if not lire_pancarte:
        screen.blit(vie_text, (20, 20))
        for i in range(vies): screen.blit(coeur, (230 + i * 110, 5))
    if joueur.double_saut and not lire_pancarte:
        screen.blit(double_jump_img, (screen_width - 150, screen_height - 260))
    if (not lire_pancarte and not dialogue_g and not dialogue_v and not dialogue_c1
            and not dialogue_caronte and not dialogue_caronte_fin
            and not choix_active and not message_reponse_active and not caronte_aide):
        screen.blit(icone_inventaire, (screen_width - 150, screen_height - 150))
        screen.blit(lettre_f, (screen_width - 107, screen_height - 175))

    joueur.update()

    if 0 < current_time - message_porte_fermee_timer < 3000:
        texte_porte = police.render("Parlez a Virgilio pour ouvrir la porte", True, (255, 215, 0))
        screen.blit(texte_porte, (screen_width//2 - texte_porte.get_width()//2, screen_height - 200))

    # -----------------------------------------------------------------------------------------
    # HITBOXES DEBUG
    # -----------------------------------------------------------------------------------------
    if debug_hitboxes:
        for plat in caronte2:
            debug_surface = pygame.Surface((plat.width, plat.height), pygame.SRCALPHA)
            debug_surface.fill((255, 255, 255, 100))
            screen.blit(debug_surface, (plat.x - camera_x, plat.y - camera_y))
        for mur in plateformes_prison:
            debug_surface = pygame.Surface((mur.width, mur.height), pygame.SRCALPHA)
            debug_surface.fill((0, 0, 255, 100))
            screen.blit(debug_surface, (mur.x - camera_x, mur.y - camera_y))
    if debug_hitboxes:
        for plat in plateformes + bateau_plat:
            debug_surface = pygame.Surface((plat.width, plat.height), pygame.SRCALPHA)
            debug_surface.fill((255, 0, 0, 100))
            screen.blit(debug_surface, (plat.x - camera_x, plat.y - camera_y))
    if debug_hitboxes:
        for s in sol:
            debug_surface = pygame.Surface((s.width, s.height), pygame.SRCALPHA)
            debug_surface.fill((255, 128, 0, 100))
            screen.blit(debug_surface, (s.x - camera_x, s.y - camera_y))
    if debug_hitboxes:
        for plat in plateformes_danger + plateformes_danger2:
            debug_surface = pygame.Surface((plat.width, plat.height), pygame.SRCALPHA)
            debug_surface.fill((0, 255, 0, 100))
            screen.blit(debug_surface, (plat.x - camera_x, plat.y - camera_y))
    if debug_hitboxes:
        debug_surface = pygame.Surface((joueur.rect.width, joueur.rect.height), pygame.SRCALPHA)
        debug_surface.fill((0, 255, 0, 100))
        screen.blit(debug_surface, (joueur.rect.x - camera_x, joueur.rect.y - camera_y))
        debug_surface_m = pygame.Surface((monstre_spawn.rect.width, monstre_spawn.rect.height), pygame.SRCALPHA)
        debug_surface_m.fill((255, 0, 255, 100))
        screen.blit(debug_surface_m, (monstre_spawn.rect.x - camera_x, monstre_spawn.rect.y - camera_y))
        for m in monstres_niveau2:
            debug_surface_m2 = pygame.Surface((m.rect.width, m.rect.height), pygame.SRCALPHA)
            debug_surface_m2.fill((255, 0, 255, 100))
            screen.blit(debug_surface_m2, (m.rect.x - camera_x, m.rect.y - camera_y))
        for m in monstres_niveau2:
            if isinstance(m, Squelette):
                for boule in m.boules:
                    debug_surface = pygame.Surface((boule.rect.width, boule.rect.height), pygame.SRCALPHA)
                    debug_surface.fill((255, 165, 0, 180))
                    screen.blit(debug_surface, (boule.rect.x - camera_x, boule.rect.y - camera_y))
    # Dialogues
    if active and not dialogue_g and current_time - giordano_dialogue_cooldown > duree_dialogue_cooldown:
        screen.blit(bouton_e, (bouton_e_rect.x - camera_x, bouton_e_rect.y - camera_y + button_offset))
    if dialogue_g:
        texte_affiche = message[0:counter // speed]
        joueur.peut_bouger = False; joueur.is_animating = False
        screen.blit(cadre_g, cadre_g_rect)
        for i, ligne in enumerate(texte_affiche.split("\n")): screen.blit(police.render(ligne, True, '#4f2310'), (480, 470 + i * 30))
        if not en_pause and counter < speed * len(message):
            counter += 1
            if counter % speed == 0 and sfx.sfxnpc.get_num_channels() == 0: sfx.sfxnpc.play()
        elif counter >= speed * len(message): sfx.sfxnpc.stop(); done = True; screen.blit(bouton_e, (1000, 600 + button_offset))

    if active2 and not dialogue_v and current_time - virgilio_dialogue_cooldown > duree_dialogue_cooldown:
        screen.blit(bouton_e, ((bouton_e_rect.x - 900) - camera_x, (bouton_e_rect.y - 2110) - camera_y + button_offset))
    if dialogue_v:
        texte_affiche = message2[0:counter // speed]
        joueur.peut_bouger = False; joueur.is_animating = False
        screen.blit(cadre_v, cadre_v_rect)
        for i, ligne in enumerate(texte_affiche.split("\n")): screen.blit(police.render(ligne, True, '#4f2310'), (480, 470 + i * 30))
        if not en_pause and counter < speed * len(message2):
            counter += 1
            if counter % speed == 0 and sfx.sfxnpc.get_num_channels() == 0: sfx.sfxnpc.play()
        elif counter >= speed * len(message2): sfx.sfxnpc.stop(); done = True; screen.blit(bouton_e, (1020, 550 + button_offset))

    if active3 and not dialogue_c1 and current_time - condamne1_dialogue_cooldown > duree_dialogue_cooldown:
        screen.blit(bouton_e, (280 - camera_x, 5730 - camera_y + button_offset))
    if dialogue_c1:
        texte_affiche = message3[0:counter // speed]
        joueur.peut_bouger = False; joueur.is_animating = False
        screen.blit(cadre_c1, cadre_c1_rect)
        for i, ligne in enumerate(texte_affiche.split("\n")): screen.blit(police.render(ligne, True, '#4f2310'), (480, 470 + i * 30))
        if not en_pause and counter < speed * len(message3):
            counter += 1
            if counter % speed == 0 and sfx.dialogue_csfx.get_num_channels() == 0: sfx.dialogue_csfx.play()
        elif counter >= speed * len(message3): sfx.dialogue_csfx.stop(); done = True; screen.blit(bouton_e, (1020, 550 + button_offset))

    if active4 and not dialogue_caronte and not choix_active and not message_reponse_active and current_time - caronte_dialogue_cooldown > duree_dialogue_cooldown:
        screen.blit(bouton_e, (caronte_rect.centerx - camera_x + 50, caronte_rect.y - camera_y - 35 + button_offset))
    if dialogue_caronte:
        texte_affiche = message4[0:counter // speed]
        joueur.peut_bouger = False; joueur.is_animating = False
        screen.blit(cadre_caronte, cadre_caronte_rect)
        for i, ligne in enumerate(texte_affiche.split("\n")): screen.blit(police.render(ligne, True, '#4f2310'), (480, 470 + i * 30))
        if not en_pause and counter < speed * len(message4):
            counter += 1
            if counter % speed == 0 and sfx.carontesfx.get_num_channels() == 0: sfx.carontesfx.play()
        elif counter >= speed * len(message4): sfx.carontesfx.stop(); done = True; screen.blit(bouton_e, (1020, 550 + button_offset))

    if dialogue_caronte_fin:
        texte_affiche = message4[0:counter // speed]
        joueur.peut_bouger = False; joueur.is_animating = False
        screen.blit(cadre_caronte, cadre_caronte_rect)
        for i, ligne in enumerate(texte_affiche.split("\n")): screen.blit(police.render(ligne, True, '#4f2310'), (480, 470 + i * 30))
        if not en_pause and counter < speed * len(message4):
            counter += 1
            if counter % speed == 0 and sfx.carontesfx.get_num_channels() == 0: sfx.carontesfx.play()
        elif counter >= speed * len(message4): sfx.carontesfx.stop(); done = True; screen.blit(bouton_e, (1020, 550 + button_offset))

    if choix_active: joueur.peut_bouger = False; joueur.is_animating = False; screen.blit(choix_cadre, choix_cadre_rect)

    if message_reponse_active:
        texte_rep = message5[message_reponse_index][0:message_reponse_counter // speed]
        screen.blit(cadre_caronte, cadre_caronte_rect)
        for i, ligne in enumerate(texte_rep.split("\n")): screen.blit(police.render(ligne, True, '#4f2310'), (480, 470 + i * 30))
        if not en_pause and message_reponse_counter < speed * len(message5[message_reponse_index]):
            message_reponse_counter += 1
            if message_reponse_counter % speed == 0 and sfx.carontesfx.get_num_channels() == 0: sfx.carontesfx.play()
        elif message_reponse_counter >= speed * len(message5[message_reponse_index]):
            sfx.carontesfx.stop(); message_reponse_done = True; screen.blit(bouton_e, (1020, 550 + button_offset))

    if message_cle_actif:
        texte = police.render("Equipez une clé pour déverrouiller, la rouge se trouve chez Giordano", True, (255, 215, 0))
        screen.blit(texte, (screen_width//2 - texte.get_width()//2, screen_height - 200))
        if current_time - message_cle_timer > 3000: message_cle_actif = False

    if caronte_aide:
        texte_affiche = message_caronte_rame[0:message_caronte_rame_counter // speed]
        screen.blit(cadre_caronte, cadre_caronte_rect)
        for i, ligne in enumerate(texte_affiche.split("\n")): screen.blit(police.render(ligne, True, '#4f2310'), (480, 470 + i * 30))
        if message_caronte_rame_done: screen.blit(bouton_e, (1020, 550 + button_offset))

    if active_v2 and not dialogue_v2 and current_time - virgilio2_dialogue_cooldown > duree_dialogue_cooldown:
        screen.blit(bouton_e, (virgilio2_rect.centerx - camera_x - 25, virgilio2_rect.y - camera_y - 60 + button_offset))
    if dialogue_v2:
        texte_affiche = message_v2_actuel[0:counter // speed]
        joueur.peut_bouger = False; joueur.is_animating = False
        screen.blit(cadre_v2, cadre_v_rect)
        for i, ligne in enumerate(texte_affiche.split("\n")): screen.blit(police.render(ligne, True, '#4f2310'), (480, 470 + i * 30))
        if not en_pause and counter < speed * len(message_v2_actuel):
            counter += 1
            if counter % speed == 0 and sfx.sfxnpc.get_num_channels() == 0: sfx.sfxnpc.play()
        elif counter >= speed * len(message_v2_actuel): sfx.sfxnpc.stop(); done = True; screen.blit(bouton_e, (1020, 550 + button_offset))

    # Titre L'Enfer
    if not en_pause and titre_index < speed * len(titre_jeu):
        titre_index += 1
        if titre_index % speed == 0: sfx.sfxtitre.play()
    elif not en_pause and titre_index >= speed * len(titre_jeu) and titre_fin == 0:
        sfx.sfxtitre.stop(); titre_fin = pygame.time.get_ticks()
    titre_texte = police_titre.render(titre_jeu[0:titre_index // speed], True, 'white')
    if (titre_index < speed * len(titre_jeu) or pygame.time.get_ticks() - titre_fin < 3000) and not lire_pancarte:
        screen.blit(titre_texte, (20, 100))
    else:
        if titre_fin > 0: sfx.fin.play(loops=0); titre_fin = -1

    if lire_pancarte:
        pancarte_x = screen_width//2 - pancarte.get_width()//2
        pancarte_y = screen_height//2 - pancarte.get_height()//2
        screen.blit(pancarte, (pancarte_x, pancarte_y))
        if show_button_e_pancarte: screen.blit(bouton_e, (950, 500 + button_offset))

    if inventaire_affiche:
        inv_x = screen_width//2 - inventaire_img.get_width()//2
        inv_y = screen_height//2 - inventaire_img.get_height()//2
        screen.blit(inventaire_img, (inv_x, inv_y))
        if show_button_f_inventaire: screen.blit(bouton_f, (850, 600 + button_offset))
        for index, item in enumerate(inventaire):
            slot_rect = get_slot_inventaire_rect(index)
            item_data = ITEMS_INVENTAIRE[item["id"]]
            screen.blit(frame_inventaire, slot_rect.topleft)
            screen.blit(item_data["image"], slot_rect.topleft)
            est_equipe = ((item["id"]=="bottes" and bottes_equipees) or (item["id"]=="couteau" and couteau_equipee)
                          or (item["id"]=="cle_caronte" and cle_caronte_equipee) or (item["id"]=="cle_enfer" and cle_enfer_equipee))
            if est_equipe: pygame.draw.rect(screen, (255,215,0), slot_rect, 3)
            elif inventaire_index_selectionne == index: pygame.draw.rect(screen, (255,255,255), slot_rect, 2)
        if tooltip_inventaire_visible and inventaire_index_selectionne is not None and inventaire_index_selectionne < len(inventaire):
            item = inventaire[inventaire_index_selectionne]
            action_label = ITEMS_INVENTAIRE[item["id"]]["action_label"]()
            if action_label:
                slot_rect = get_slot_inventaire_rect(inventaire_index_selectionne)
                tooltip_rect = pygame.Rect(slot_rect.right + 10, slot_rect.y, 130, 40)
                pygame.draw.rect(screen, (40,40,40), tooltip_rect); pygame.draw.rect(screen, (200,200,200), tooltip_rect, 2)
                screen.blit(police.render(action_label, True, (255,255,255)), (tooltip_rect.x + 7, tooltip_rect.y + 10))
        if not inventaire:
            screen.blit(inventaire_vide_text, (500, 380)); screen.blit(inventaire_vide_text2, (530, 400))

    if en_pause:
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA); overlay.fill((0,0,0,150)); screen.blit(overlay, (0,0))
        screen.blit(titre_logo_jeu, titre_rect_jeu)
        for i, bouton in enumerate(boutons_pause):
            y_b = 280 + i * 80; x_b = screen_width//2 - pause_button_width//2
            rect_b = pygame.Rect(x_b, y_b, pause_button_width, pause_button_height)
            couleur = "#f5c542" if i == pause_selected else "white"
            texte_b = police_bouton_pause.render(bouton["texte"], True, couleur)
            pygame.draw.rect(screen, "#521010", rect_b, border_radius=12)
            pygame.draw.rect(screen, "#B65252", rect_b, 3, border_radius=12)
            screen.blit(texte_b, (rect_b.centerx - texte_b.get_width()//2, rect_b.centery - texte_b.get_height()//2))
            if i == pause_selected:
                fleche = police_bouton_pause.render(">", True, "#f5c542")
                screen.blit(fleche, (rect_b.x - 35, rect_b.centery - fleche.get_height()//2))

    if en_pause and afficher_parametres_pause:
        screen.blit(parametre_gui_pause, parametre_gui_rect_p); screen.blit(fermer_pause, fermer_pause_rect)
        screen.blit(police_param_pause.render("musique", True, (255,255,255)), (270, 170))
        screen.blit(police_param_pause.render("speedrun (recommencer pour prendre effet)", True, (255,255,255)), (270, 270))
        screen.blit(police_param_pause.render("sfx", True, (255,255,255)), (270, 370))
        for p in parametres_toggles_pause: screen.blit(activer_p if p["enabled"] else desactiver_p, p["rect"])

    if speedrun and not en_pause:
        if speedrun_started and not speedrun_finished: speedrun_elapsed = current_time - speedrun_start_time
        ms = speedrun_elapsed % 1000; sec = (speedrun_elapsed // 1000) % 60; mins = speedrun_elapsed // 60000
        timer_str = f"{mins:02d}:{sec:02d}.{ms // 10:02d}"
        timer_surf = police.render(timer_str, True, (255,215,0) if speedrun_finished else (255,255,255))
        screen.blit(timer_surf, (screen_width - timer_surf.get_width() - 20, 20))
        if not speedrun_finished:
            pygame.draw.rect(screen, (255,215,0), (speedrun_finish_rect.x - camera_x, speedrun_finish_rect.y - camera_y, speedrun_finish_rect.width, speedrun_finish_rect.height), 3)
            fin_label = police.render("FIN", True, (255,215,0))
            screen.blit(fin_label, (speedrun_finish_rect.x - camera_x + speedrun_finish_rect.width//2 - fin_label.get_width()//2, speedrun_finish_rect.y - camera_y - 30))
        else:
            fini_surf = police.render("TERMINE !", True, (255,215,0))
            screen.blit(fini_surf, (screen_width - fini_surf.get_width() - 20, 50))

    if niveau_actuel == 2 and not lire_pancarte:
        palier_ref = paliers_bateau[palier_bateau_index] if palier_bateau_index < len(paliers_bateau) else paliers_bateau[-1]
        dessiner_texte_contour(screen, police, f"Monstres tues : {nombre_monstres_tues}/{palier_ref}", screen_width - 20, 70, "#ffffff", "#000000", epaisseur=4)

    if active_porte:
        screen.blit(bouton_e, (porte_rect.x - camera_x + porte_rect.width//2 + 250, porte_rect.y - camera_y + button_offset + 350))

    # Transitions
    if transition_recommencer:
        temps_t = current_time - transition_start
        alpha = int(min(temps_t / transition_duree_fondu, 1) * 255)
        if temps_t >= transition_duree_fondu + transition_pause_noire:
            transition_recommencer = False; reset()
        fondu = pygame.Surface((screen_width, screen_height)); fondu.fill((0,0,0)); fondu.set_alpha(alpha); screen.blit(fondu, (0,0))
        ti = titre_logo_jeu.copy(); ti.set_alpha(alpha); screen.blit(ti, ti.get_rect(center=(screen_width//2, screen_height//2)))

    if transition_porte_enfer_start:
        joueur.vx = 0; joueur.vel_y = 0; joueur.is_animating = False
        t_porte = current_time - transition_porte_enfer_start
        if t_porte < 500: alpha = int(t_porte / 500 * 255)
        elif t_porte < 4000:
            if not transition_porte_teleporte:
                joueur.rect.center = (2100, 6450) if joueur.rect.x < 2000 else (400, 750)
                joueur.vel_y = 0; joueur.vx = 0; transition_porte_teleporte = True
        elif t_porte < 4500:
            alpha = int((1 - (t_porte - 4000) / 500) * 255)
        else:
            alpha = 0; transition_porte_enfer_start = 0
            transition_porte_teleporte = False
            joueur.peut_bouger = not (en_pause or lire_pancarte or inventaire_affiche or dialogue_g or dialogue_v or dialogue_c1 or dialogue_caronte)
            sfx.porte_sortir.play()
        if alpha > 0:
            fondu = pygame.Surface((screen_width, screen_height)); fondu.fill((0,0,0)); fondu.set_alpha(alpha); screen.blit(fondu, (0,0))

    if transition_caronte_start:
        t_c = current_time - transition_caronte_start
        if t_c < 500: alpha = int(t_c / 500 * 255)
        elif t_c < 1000:
            alpha = 255
            if not transition_caronte_teleporte:
                niveau_actuel = 2; joueur.rect.topleft = (200, 550); joueur.vel_y = joueur.vx = 0
                transition_caronte_teleporte = True; sfx.niveau_2caronte.play(-1)
        elif t_c < 1500: alpha = int((1 - (t_c - 1000) / 500) * 255)
        else: transition_caronte_start = 0; transition_caronte_teleporte = False; joueur.peut_bouger = True; alpha = 0
        if alpha > 0:
            fondu = pygame.Surface((screen_width, screen_height)); fondu.fill((0,0,0)); fondu.set_alpha(alpha); screen.blit(fondu, (0,0))

    if transition_caronte_fin_start:
        t_cf = current_time - transition_caronte_fin_start
        if t_cf < 0: alpha = 0
        elif t_cf < 1000: alpha = int(t_cf / 1000 * 255)
        elif t_cf < 1500:
            alpha = 255
            if not transition_caronte_fin_teleporte:
                niveau_actuel = 1; joueur.rect.topleft = (3850, 5380); joueur.vel_y = joueur.vx = 0
                monstres_niveau2 = []; caronte_niveau2_termine = True; sfx.niveau_2caronte.stop()
                if settings.musique: sfx.musiquefond.set_volume(0.1); sfx.musiquefond.play(-1) if sfx.musiquefond.get_num_channels() == 0 else None
                else: sfx.musiquefond.set_volume(0)
                transition_caronte_fin_teleporte = True
        elif t_cf < 2500: alpha = int((1 - (t_cf - 1500) / 1000) * 255)
        else:
            transition_caronte_fin_start = 0; transition_caronte_fin_teleporte = False; fin_caronte_declenchee = False
            dialogue_caronte_fin = True; joueur.peut_bouger = False; active_message_caronte = 0
            message4 = message_caronte_fin[0]; counter = 0; done = False; alpha = 0
        if alpha > 0:
            fondu = pygame.Surface((screen_width, screen_height)); fondu.fill((0,0,0)); fondu.set_alpha(alpha); screen.blit(fondu, (0,0))

    if transition_fin_active:
        if speedrun and speedrun_started and not speedrun_finished:
            speedrun_finished = True
            speedrun_final_time = speedrun_elapsed
        t_fin = current_time - transition_fin_start
        if t_fin < 2500:
            alpha = int(t_fin / 2500 * 255)
            fondu = pygame.Surface((screen_width, screen_height)); fondu.fill((0,0,0)); fondu.set_alpha(alpha); screen.blit(fondu, (0,0))
        elif t_fin < 17500:
            if transition_fin_phase < 1:
                transition_fin_phase = 1; sfx.musiquefond.stop(); sfx.niveau_2caronte.stop(); pygame.mixer.pause()
            screen.fill((0,0,0))
            t_texte = t_fin - 2500
            police_fin = pygame.font.Font("asset/polices/ari-w9500-bold.ttf", 26)
            for i, ligne in enumerate(TEXTES_FIN):
                debut = [2000, 5000, 8000][i]
                if t_texte >= debut:
                    alpha_ligne = min(int((t_texte - debut) / 800 * 255), 255)
                    surf_ligne = police_fin.render(ligne, True, (255,255,255))
                    surf_copy  = surf_ligne.copy(); surf_copy.set_alpha(alpha_ligne)
                    y = screen_height//2 - 60 + i * 40 if i < 2 else screen_height//2 + 40
                    screen.blit(surf_copy, (screen_width//2 - surf_ligne.get_width()//2, y))
        elif t_fin < 19000:
            if transition_fin_phase < 2: transition_fin_phase = 2; sfx.paradis.play(-1)
            screen.fill((0,0,0))
            alpha_img = int((t_fin - 17500) / 1500 * 255)
            img_copie = fin_image.copy(); img_copie.set_alpha(alpha_img); screen.blit(img_copie, (0,0))
        else:
            if transition_fin_phase < 3: transition_fin_phase = 3
            screen.blit(fin_image, (0,0))
            t_phase3 = t_fin - 19000

            # "Le Paradis" apparaît lentement après 2s
            if t_phase3 >= 2000:
                alpha_titre = min(int((t_phase3 - 2000) / 3000 * 255), 255)
                police_fin_titre = pygame.font.Font("asset/polices/Dungeon Depths.otf", 90)
                surf_titre = police_fin_titre.render("Le Paradis", True, (0, 0, 0))
                surf_titre.set_alpha(alpha_titre)
                screen.blit(surf_titre, surf_titre.get_rect(center=(screen_width // 2, screen_height // 2 - 60)))

            # "La Fin" apparaît une fois "Le Paradis" totalement affiché (2000 + 3000 = 5000ms)
            if t_phase3 >= 5000:
                alpha_fin = min(int((t_phase3 - 5000) / 2000 * 255), 255)
                police_fin_sous = pygame.font.Font("asset/polices/Coolvetica Rg.otf", 54)
                surf_lafin = police_fin_sous.render("La Fin", True, (0, 0, 0))
                surf_lafin.set_alpha(alpha_fin)
                screen.blit(surf_lafin, surf_lafin.get_rect(center=(screen_width // 2, screen_height // 2 + 30)))

            # Bouton "Menu" apparaît 3s après "La Fin" (5000 + 2000 + 3000 = 10000ms)
            if t_phase3 >= 10000:
                bouton_fin_rect = pygame.Rect(0, 0, 300, 60)
                bouton_fin_rect.center = (screen_width // 2, screen_height // 2 + 130)
                couleur_btn = (80, 20, 20) if bouton_fin_rect.collidepoint(mouse_pos) else (40, 10, 10)
                pygame.draw.rect(screen, couleur_btn, bouton_fin_rect, border_radius=12)
                pygame.draw.rect(screen, (180, 120, 60), bouton_fin_rect, 3, border_radius=12)
                police_btn = pygame.font.Font("asset/polices/Coolvetica Rg.otf", 36)
                surf_btn = police_btn.render("Retour au menu", True, (248, 236, 214))
                screen.blit(surf_btn, surf_btn.get_rect(center=bouton_fin_rect.center))

                if mouse_pressed[0] and bouton_fin_rect.collidepoint(mouse_pos):
                    sfxboutton.play()
                    pygame.mixer.stop()
                    etat_global = "menu"
                    transition_fin_active = False
                    intro = True
                    intro_start = pygame.time.get_ticks()
                    if settings.musique:
                        sfx.musiquemenu.set_volume(0.5)
                        sfx.musiquemenu.play(-1, 0, 3000)

    if niveau_actuel == 2 and bulle_monstre_actif and not caronte_aide and len(monstres_niveau2) > 0:
        bulle_surf = police.render(bulle_monstre_texte, True, (255,255,255))
        bulle_x = screen_width//2 - bulle_surf.get_width()//2; bulle_y = screen_height - 200
        if bulle_monstre_type == "monstre":
            icone_bulle_active = icone_bulle_monstre
        elif bulle_monstre_type == "esprit":
            icone_bulle_active = icone_bulle_esprit
        else:
            icone_bulle_active = icone_bulle_squelette
        screen.blit(icone_bulle_active, (bulle_x - 50, bulle_y - 4))
        screen.blit(bulle_surf, (bulle_x, bulle_y))

    screen.blit(curseur_img, mouse_pos)
    pygame.display.flip()

pygame.quit()
sys.exit()