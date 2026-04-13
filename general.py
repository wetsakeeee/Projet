import pygame, sys, subprocess, time, random
import math
from joueur import Joueur
from monstre import Monstre
from niveau1 import get_plateforme_prison, get_plateformes, plateforme_pic, plateforme_pic2, get_sol, get_plateformeshaute, get_sol2, mur2, plateforme_2, get_bateau, get_plateformes_mobiles, get_niveau2, caronte_niveau2
import sfx
from sfx import sauter, sfxmarche1, sfxmarche2, sfxmarche3, tombersfx, musiquefond, sfxboutton, choisirsfx, retoursfx
import settings
from esprit import Esprit
from squelette import Squelette
from pathlib import Path
# ----------------------------
# Initialisation Pygame
# ----------------------------
pygame.init()
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
icon = pygame.image.load("images/logo.png").convert_alpha()
pygame.display.set_icon(icon)
pygame.display.set_caption("Galileo Galilei : Across the afterlife")
clock = pygame.time.Clock()
etat = "jeu"
niveau_actuel = 1 # 2 si niveau avec caronte, 3 si boss
# Joueur
if len(sys.argv) == 3:
    joueur = Joueur(int(sys.argv[1]), int(sys.argv[2]))
else:
    joueur = Joueur()
# Monstre
if len(sys.argv) == 3:
    monstre = Monstre(int(sys.argv[1]), int(sys.argv[2]))
else:
    monstre = Monstre()

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

def dessiner_texte_contour(surface, font, texte, x, y, couleur_texte, couleur_contour, epaisseur=3):
    texte_surface = font.render(texte, True, couleur_texte)
    contour_surface = font.render(texte, True, couleur_contour)
    texte_rect = texte_surface.get_rect(topright=(x, y))

    for offset_x in range(-epaisseur, epaisseur + 1):
        for offset_y in range(-epaisseur, epaisseur + 1):
            if offset_x == 0 and offset_y == 0:
                continue
            surface.blit(contour_surface, texte_rect.move(offset_x, offset_y))

    surface.blit(texte_surface, texte_rect)
# Porte de l'enfer
porte = pygame.image.load("images/Divers/porte_enfer.png").convert_alpha()
porte = pygame.transform.scale(porte, (380, 530)) 
porte_rect = porte.get_rect(topleft=(300, 320))

pause_active = True
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
        ambient, sfx.degat, sfx.viesfx, sfx.sfxtitre, sfx.fin, sfx.liresfx, sfx.stoplire,
        sfx.ouvrir_inv, sfx.fermer_inv, sfx.selectsfx, sfx.pausesfxouvrir, sfx.pausesfxfermer,
        sfx.pausesfxbutton, sfx.sfxnpc, sfx.dialogue_csfx, sfx.carontesfx, sfxmarche1, sfxmarche2, sfxmarche3,
        sauter, tombersfx, musiquefond, musique_niveau2
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
        vol = 0 if not enabled else 0.5
        sfx.viesfx.set_volume(vol)
        sfx.sfxtitre.set_volume(0.5 if enabled else 0)
        sfx.fin.set_volume(0.5 if enabled else 0)
        sfx.liresfx.set_volume(0.5 if enabled else 0)
        sfx.stoplire.set_volume(0.5 if enabled else 0)
        sfx.ouvrir_inv.set_volume(vol)
        sfx.fermer_inv.set_volume(vol)
        sfx.selectsfx.set_volume(vol)
        sfx.pausesfxouvrir.set_volume(vol)
        sfx.pausesfxfermer.set_volume(vol)
        sfx.pausesfxbutton.set_volume(vol)
        sfx.sfxnpc.set_volume(0.5 if enabled else 0)
        sfx.dialogue_csfx.set_volume(vol)
        sfx.carontesfx.set_volume(vol)
        sfx.degat.set_volume(vol)
        sfx.mortsfx.set_volume(vol)
        sfx.satan.set_volume(vol)
        sfxmarche1.set_volume(vol)
        sfxmarche2.set_volume(vol)
        sfxmarche3.set_volume(vol)
        sauter.set_volume(0.5 if enabled else 0)
        for s in [sfxmarche1, sfxmarche2, sfxmarche3]:
            s.set_volume(0.5 if enabled else 0)

        
    sauvegarder_settings()

chute_y = 7000
zoom_factor = 3
camera_y_offset = -100

camera_x = joueur.rect.centerx - screen_width // 2
camera_y = joueur.rect.centery - screen_height // 2

coeur       = pygame.transform.scale(pygame.image.load("images/GUI/coeur.png").convert_alpha(), (100, 100))
vie_text    = pygame.transform.scale(pygame.image.load("images/GUI/vie.png").convert_alpha(), (186, 72))
double_jump = pygame.transform.scale(pygame.image.load("images/GUI/icone_double_jump.png").convert_alpha(), (100, 100))

police       = pygame.font.Font("asset/polices/ari-w9500-bold.ttf", 24)
police_titre = pygame.font.Font("asset/polices/Dungeon Depths.otf", 50)

# Système d'invincibilité
invincible          = False
invincibilite_temps = 0
duree_invincibilite = 2000

# TITRE DEBUT DE JEU
titre_sfx = sfx.sfxtitre
titre_sfx.set_volume(0.5)
titre       = "L'Enfer"
titre_index = 0
titre_fin   = 0

# Curseur custom
curseur_img = pygame.transform.scale(pygame.image.load("images/GUI/curseur.png").convert_alpha(), (30, 30))
pygame.mouse.set_visible(False)

# Pancarte
panneau = pygame.image.load("images/Divers/panneau.png").convert_alpha()
panneau = pygame.transform.scale(panneau, (96, 150))
panneau_rect = panneau.get_rect()
panneau_rect.topleft = (800, 6150)
pancarte_active        = False
panneau_button_hidden  = False
panneau_button_timer   = 0
pancarte = pygame.transform.scale(pygame.image.load("images/GUI/Pancartes/pancarte1.png").convert_alpha(), (850, 500))
lire_pancarte          = False
pancarte_timer         = 0
show_button_e_pancarte = False
liresfx                = sfx.liresfx
stoplire               = sfx.stoplire
stoplire.set_volume(0.5)
liresfx.set_volume(0.5)

# Toute interaction active
# 1 pour Giordano, 2 pour Virgilio, 3 pour Condamné, 4 pour Caronte, porte pour la porte
if niveau_actuel == 1:
    active = False
    active2 = False
    active3 = False
    active4 = False
    active_porte = False
else:
    active = active2 = active3 = active4 = active_porte = False

# --- INVENTAIRE ---
inventaire_active = True
frame_inventaire           = pygame.transform.scale(pygame.image.load("images/GUI/Inventaire/frame_inventaire.png").convert_alpha(), (80, 80))
bottes                     = pygame.transform.scale(pygame.image.load("images/Objets/botte.png").convert_alpha(), (80, 80))
potion_vie                 = pygame.transform.scale(pygame.image.load("images/Objets/potion_vie.png").convert_alpha(), (80, 80))

# Image du couteau avec son cooldown
couteau                       = pygame.transform.scale(pygame.image.load("images/Objets/couteau.png").convert_alpha(), (80, 80))
cooldown_imgs = [pygame.transform.scale(pygame.image.load(f"images/cooldown/cooldown{i}.png").convert_alpha(), (51, 15)) for i in range(5)]

icone_inventaire           = pygame.transform.scale(pygame.image.load("images/GUI/icone_inventaire.png").convert_alpha(), (100, 100))
inventaire_img             = pygame.transform.scale(pygame.image.load("images/GUI/Inventaire/inventaire.png").convert_alpha(), (560, 630))
inventaire_affiche         = False
inventaire_timer           = 0
show_button_f_inventaire   = False
pause_ouvrir_sfx = sfx.pausesfxouvrir
pause_fermer_sfx = sfx.pausesfxfermer
pause_button_sfx = sfx.pausesfxbutton
inventaire_vide_text       = police.render("Vous n'avez rien dans", True, "#7a371b")
inventaire_vide_text2      = police.render("votre inventaire !", True, "#7a371b")
lettre_f                   = police.render("F", True, "#ffffff")
# Équipement bottes
bottes_equipees             = joueur.double_saut
couteau_equipee                = joueur.couteau_equipee
inventaire                  = []
inventaire_index_selectionne = None
tooltip_inventaire_visible  = False
INVENTAIRE_SLOT_DEPART      = (400, 250)
INVENTAIRE_SLOT_TAILLE      = 80
INVENTAIRE_SLOT_COLONNES    = 2
INVENTAIRE_SLOT_ECART_X     = 110
INVENTAIRE_SLOT_ECART_Y     = 110
ITEMS_INVENTAIRE = {
    "bottes": {
        "image": bottes,
        "nom": "Bottes",
        "utilisable": True,
        "action_label": lambda: "Desequiper" if bottes_equipees else "Equiper",
    },
    "potion_vie": {
        "image": potion_vie,
        "nom": "Potion de vie",
        "utilisable": False,
        "action_label": lambda: "Utiliser" if vies < 3 else None,
    },
    "couteau": {
        "image": couteau,
        "nom": "couteau",
        "utilisable": True,
        "action_label": lambda: "Desequiper" if couteau_equipee else "Equiper",
    },
}

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
    if item_id not in ITEMS_INVENTAIRE:
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

# ----------------------------
# NPC
# ----------------------------
# Son de dialogue standard des NPC.
npcsfx = sfx.sfxnpc
npcsfx.set_volume(0.1)

# Boutons d'interaction reutilises par plusieurs systemes.
bouton_e      = pygame.image.load("images/GUI/bouton_e.png").convert_alpha()
bouton_e_rect = bouton_e.get_rect(topleft=(1600, 6150))
bouton_e      = pygame.transform.scale(bouton_e, (50, 50))
bouton_f      = pygame.image.load("images/GUI/bouton_f.png").convert_alpha()
bouton_f      = pygame.transform.scale(bouton_f, (50, 50))

# NPC 1 - Giordano
# Animation 3 frames.
giordano  = pygame.transform.scale(pygame.image.load("images/Npc/Textures/giordano.png").convert_alpha(),  (160, 105))
giordano2 = pygame.transform.scale(pygame.image.load("images/Npc/Textures/giordano2.png").convert_alpha(), (160, 105))
giordano3 = pygame.transform.scale(pygame.image.load("images/Npc/Textures/giordano3.png").convert_alpha(), (160, 105))
giordano_images      = [giordano, giordano2, giordano3]

# Variables d'animation de Giordano.
current_giordano     = 0
giordano_anim_timer  = 0
giordano_forward     = True
giordano_pause       = False
giordano_pause_timer = 0

giordano_rect = giordano.get_rect()
giordano_rect.topleft = (1600, 6190)

# "dialogue_g" dit si la fenetre de dialogue de Giordano est ouverte.
dialogue_g    = False
cadre_g       = pygame.image.load("images/Npc/Dialogues/cadre_dialogue_giordano.png").convert_alpha()
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
death_animation_done = False
freeze_bg = 0
niveau2_bg_offset = 0
paliers_bateau = [5, 15, 30]
palier_bateau_index = 0
nombre_monstres_tues = 0

coeursfx = sfx.coeursfx
mortsfx = sfx.mortsfx
mortsfx.set_volume(0.5 if settings.option_3 else 0)


# Variables partagees par les dialogues.
# "counter" suit la progression de l'ecriture lettre par lettre.
# "speed" regle la vitesse d'affichage du texte.
# "done" passe a True quand le message courant est entierement affiche.

# Cooldowns des interactions NPC.
# "duree_cooldown" evite de redonner une recompense trop souvent.
# "duree_dialogue_cooldown" evite de rouvrir un dialogue instantanement.
giordano_cooldown = -30000
virgilio_cooldown = -30000
duree_cooldown    = 30000
giordano_dialogue_cooldown = -3000
virgilio_dialogue_cooldown = -3000
condamne1_dialogue_cooldown = -3000
caronte_dialogue_cooldown = -3000
duree_dialogue_cooldown = 3000

# NPC 2 - Virgilio
virgilio      = pygame.transform.scale(pygame.image.load("images/Npc/Textures/virgilio.png").convert_alpha(), (60, 120))
virgilio_rect = virgilio.get_rect()
virgilio_rect.topleft = (700, 4080)
# "dialogue_v" dit si le dialogue de Virgilio est ouvert.
dialogue_v    = False
cadre_v       = pygame.image.load("images/Npc/Dialogues/cadre_dialogue_virgilio.png").convert_alpha()
cadre_v_rect  = cadre_v.get_rect(center=(640, 550))

# "active_message" est l'index du message courant de Giordano.
counter         = 0
speed           = 3
active_message  = 0
message         = messages[active_message]
done            = False
# "active_message2" est l'index du message courant dans "message_v".
message_v       = ["Salut Galileo !", "Fais attention car les plateformes deviennent\nchaudes !","Prends ces bottes pour sauter deux fois."]
active_message2 = 0
message2        = message_v[active_message2]

# NPC 3 -- Condamnés
condamnesfx = sfx.dialogue_csfx
condamne1 = pygame.transform.scale(pygame.image.load("images/Npc/Textures/condamne1.png").convert_alpha(), (112, 112))
condamne1_rect = condamne1.get_rect()
condamne1_rect.topleft = (300, 5737)
# "dialogue_c1" dit si le dialogue du condamne est ouvert.
dialogue_c1 = False
cadre_c1 = pygame.image.load("images/Npc/Dialogues/cadre_dialogue_condamne.png").convert_alpha()
cadre_c1_rect  = cadre_c1.get_rect(center=(640, 550))

# "active_message_c1" est l'index du message courant dans "message_c1".
message_c1 = ["...", "...", "Aide m-", "...", "Prends ce couteau, t'en aura besoin...","C'est trop dangereux ici...", "J'suis pas capable de survivre..."]
active_message_c1 = 0
message3 = message_c1[active_message_c1]

# NPC 4 -- Caronte
carontesfx = sfx.carontesfx
caronte = pygame.transform.scale(pygame.image.load("images/Npc/Textures/caronte.png").convert_alpha(), (64, 120))
caronte_rect = caronte.get_rect()
caronte_rect.topleft = (3850, 5380)
dialogue_caronte = False
dialogue_caronte_fin = False
cadre_caronte = pygame.image.load("images/Npc/Dialogues/cadre_dialogue_caronte.png").convert_alpha()
cadre_caronte_rect  = cadre_caronte.get_rect(center=(640, 550))
message_caronte = ["Je suis Caronte, le passeur des Enfers.", "Si tu veux sortir d'ici, tu devras m'aider à passer\nsur le fleuve.","Des codamnés y abritent et tentent de nous faire\ncouler moi et mon bateau. ", "Aide moi à passer et je te donnerai un cadeau\nen échange."]
active_message_caronte = 0
message4 = message_caronte[active_message_caronte]
message_caronte_fin = ["Merci de m'avoir aidé, Galileo !", "Comme promis, voici t'as récompense"]

choix_cadre = pygame.image.load("images/Npc/Dialogues/cadre_choix.png").convert_alpha()
choix_cadre_rect = choix_cadre.get_rect(center=(640, 550))
message5 = ["Merci beaucoup ! Aller viens, monte dans mon\nbateau !", "Aucun problème, passe me voir quand tu\nchangeras d'avis."]
choix_active = False
choix_fait = None  # None, 1 ou 2
message_reponse_active = False
message_reponse_index = None
message_reponse_counter = 0
message_reponse_done = False


transition_caronte_start = 0 # Aller au niveau 2
transition_caronte_teleporte = False
transition_caronte_fin_start = 0
transition_caronte_fin_teleporte = False
fin_caronte_declenchee = False

bateau = pygame.transform.scale(pygame.image.load("images/Divers/bateau.png").convert_alpha(), (300,130))
bateau_rect = bateau.get_rect()
bateau_rect.topleft = (3500, 5370)

# MURS
plateformes_haute = get_plateformeshaute()
mur2 = mur2()
# Music
pygame.mixer.init(48200)
ambient = sfx.musiquefond
if settings.musique:
    ambient.set_volume(0.1)
    ambient.play(-1)
else:
    ambient.set_volume(0)

# Appliquer sfx au démarrage
if not settings.option_3:
    _vol = 0
    sfx.viesfx.set_volume(_vol)
    sfx.sfxtitre.set_volume(_vol)
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
    sfx.carontesfx.set_volume(_vol)
    sfx.degat.set_volume(_vol)
    sfx.mortsfx.set_volume(_vol)
    sfx.satan.set_volume(_vol)

# Plateformes
plateformes_prison = get_plateforme_prison()
plateformes_niveau = get_plateformes()
plateformes        = plateformes_niveau
plateformes2 = plateforme_2()
sol                = get_sol()
niveau_largeur     = 5000
sol2 = get_sol2()
plateformes_mobiles = get_plateformes_mobiles()

# Permet d'attribuer au plateformes une image correspondante
# Le except sert à ce que le jeu ne crash pas si l'image est introuvable
try:
    platform_image_orig  = pygame.image.load("images/Plateformes/Niveau1/plateforme_moyenne.png").convert_alpha()
    plateforme_petite_orig = pygame.image.load("images/Plateformes/Niveau1/plateforme_petite.png").convert_alpha()
    plateforme2_img = pygame.image.load("images/Plateformes/Niveau2/plateforme2.png").convert_alpha()
    mur_prison_orig   = pygame.image.load("images/Plateformes/Niveau1/murprison.png").convert_alpha()
    sol_image_orig = pygame.image.load("images/Plateformes/Niveau1/sol.png").convert_alpha()
    pic_sol_orig     = pygame.image.load("images/Plateformes/pic_sol.png").convert_alpha()
    pic_plafond_orig = pygame.image.load("images/Plateformes/pic_plafond.png").convert_alpha()
    sol2_image_orig = pygame.image.load("images/Plateformes/Niveau2/sol_niveau2.png").convert_alpha()
    mur2_image_orig = pygame.image.load("images/Plateformes/Niveau2/mur_niveau2.png").convert_alpha()
    mur2_2_image_orig = pygame.image.load("images/Plateformes/Niveau2/mur2_niveau2.png").convert_alpha()
except:
    platform_image_orig  = None
    plateforme_petite_orig = None
    plateforme2_img = None
    mur_prison_orig = None
    sol_image_orig = None
    pic_sol_orig     = None
    pic_plafond_orig = None
    sol2_image_orig = None
    mur2_image_orig = None
    mur2_2_image_orig = None

#--------------------------------------------------------------
# IMAGES PLATEFORMES 
#--------------------------------------------------------------
# Crée une liste où on stockera les images des plateformes redimensionnées à la bonne taille

platform_images = []
for plateforme in plateformes:
    if plateforme.width == 100 and plateforme.height == 40:
        orig = plateforme_petite_orig
    else:
        orig = platform_image_orig
    if orig:
        img = pygame.transform.scale(orig, (plateforme.width, plateforme.height))
        platform_images.append(img)
    else:
        platform_images.append(None)

sol_images = []
for s in sol:
    img = pygame.transform.scale(sol_image_orig, (s.width, s.height))
    sol_images.append(img)

sol2_images = []
for s in sol2:
    img = pygame.transform.scale(sol2_image_orig, (s.width, s.height))
    sol2_images.append(img)

mur2_images = []
for index, s in enumerate(mur2):
    orig = mur2_image_orig if index == 0 else mur2_2_image_orig
    if orig:
        img = pygame.transform.scale(orig, (s.width, s.height))
        mur2_images.append(img)
    else:
        mur2_images.append(None)

# Plateformes de danger
plateformes_danger  = plateforme_pic()
plateformes_danger2 = plateforme_pic2()

pic_sol_images = []
for plat in plateformes_danger:
    img = pygame.transform.scale(pic_sol_orig, (plat.width, plat.height))
    pic_sol_images.append(img)

pic_plafond_images = []
for plat in plateformes_danger2:
    img = pygame.transform.scale(pic_plafond_orig, (plat.width, plat.height))
    pic_plafond_images.append(img)

# Murs prison
mur_prison_images = []
for mur in plateformes_prison:
    img = pygame.transform.scale(mur_prison_orig, (mur.width, mur.height))
    mur_prison_images.append(img)

# Plateforme du niveau 2
plateforme2_images = []
for plat in plateformes2:
    img = pygame.transform.scale(plateforme2_img,(plat.width,plat.height))
    plateforme2_images.append(img)

# Background
background_orig = pygame.image.load("images/Fonds/background.png").convert_alpha()
img_w, img_h    = background_orig.get_size()
ratio           = max(screen_width / img_w, screen_height / img_h)
bg_width        = int(img_w * ratio * zoom_factor)
bg_height       = int(img_h * ratio * zoom_factor)
background      = pygame.transform.smoothscale(background_orig, (bg_width, bg_height))
bg_offset_x     = -200
bg_offset_y     = -300
parallax_factor = 0.5

# Monstre
monstre_spawn = Monstre(1500, 3550)

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

# --- Menu paramètres en pause ---
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
    {"name": "option_3", "enabled": settings.option_3, "rect": pygame.Rect(100, 350, 150, 75)},
]

# Sert comme reset de progression quand le joueur veut
# recommencer la partie
def reset():
    global vies, etat, invincible, invincibilite_temps
    global death_animation_start, death_sound_stage, death_animation_done, freeze_bg, niveau2_bg_offset
    global speedrun, speedrun_started, speedrun_start_time, speedrun_elapsed, speedrun_pause_start, speedrun_finished, speedrun_final_time
    global dialogue_g, dialogue_v, dialogue_c1, dialogue_caronte, dialogue_caronte_fin
    global active_message, active_message2, active_message_c1, active_message_caronte
    global message, message2, message3, message4
    global counter, done
    global giordano_cooldown, virgilio_cooldown
    global giordano_dialogue_cooldown, virgilio_dialogue_cooldown, condamne1_dialogue_cooldown, caronte_dialogue_cooldown
    global bottes_equipees, couteau_equipee, inventaire, inventaire_index_selectionne, tooltip_inventaire_visible
    global inventaire_affiche, lire_pancarte, pancarte_active, panneau_button_hidden
    global titre_index, titre_fin
    global en_pause, afficher_parametres_pause
    global transition_caronte_start, transition_caronte_teleporte, transition_caronte_fin_start, transition_caronte_fin_teleporte
    global choix_active, choix_fait, message_reponse_active, message_reponse_index, message_reponse_counter, message_reponse_done
    global niveau_actuel
    global caronte_rame_dialogue_fait
    global caronte_aide, bateau_reparer, rame_ramasser, active_rame, donner_rame
    global nombre_de_monstre, monstres_niveau2, dernier_spawn_monstre, spawn_delay
    global palier_bateau_index
    global nombre_monstres_tues, fin_caronte_declenchee

    tombersfx.stop()
    sfx.mortsfx.stop()
    sfx.coeursfx.stop()
    sfx.coeurmort.stop()
    sfx.satan.stop()
    tombersfx.set_volume(0)
    joueur.en_chute = False
    joueur.chute_son_joue = False
    joueur.chute_fadeout = False
    joueur.double_saut = False   # pas de bottes au départ
    joueur.couteau_equipee = False  # pas d'épée au départ 
    transition_caronte_start = 0
    transition_caronte_teleporte = False
    transition_caronte_fin_start = 0
    transition_caronte_fin_teleporte = False

    vies = 3
    etat = "jeu"
    death_animation_start = None
    death_sound_stage = 0
    death_animation_done = False
    freeze_bg = 0
    niveau2_bg_offset = 0
    palier_bateau_index = 0
    invincible = False
    invincibilite_temps = 0
    nombre_de_monstre = 0
    nombre_monstres_tues = 0
    monstres_niveau2 = []
    dernier_spawn_monstre = 0
    spawn_delay = random.randint(500,500)

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
    dialogue_caronte = False
    dialogue_caronte_fin = False
    active_message = 0
    active_message2 = 0
    active_message_c1 = 0
    active_message_caronte = 0
    message = messages[0]
    message2 = message_v[0]
    message3 = message_c1[0]
    message4 = message_caronte[0]
    counter = 0
    done = False

    giordano_cooldown = -30000
    virgilio_cooldown = -30000
    giordano_dialogue_cooldown = -3000
    virgilio_dialogue_cooldown = -3000
    condamne1_dialogue_cooldown = -3000
    caronte_dialogue_cooldown = -3000

    bottes_equipees = False
    couteau_equipee = False
    inventaire = []
    inventaire_index_selectionne = None
    tooltip_inventaire_visible = False
    inventaire_affiche = False
    lire_pancarte = False
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
    joueur.couteau_equipee = False
    joueur.au_sol = False
    joueur.double_jump_effects = []
    joueur.peut_bouger = True
    joueur.en_chute = False
    joueur.chute_son_joue = False
    joueur.facing_left = False
    niveau_actuel = 1
    transition_caronte_start = 0
    transition_caronte_teleporte = False
    choix_active = False
    choix_fait = None
    message_reponse_active = False
    message_reponse_index = None
    message_reponse_counter = 0
    message_reponse_done = False
    caronte_rame_dialogue_fait = False
    caronte_aide = False
    fin_caronte_declenchee = False
    bateau_reparer = True
    rame_ramasser = True
    active_rame = False
    donner_rame = False
    pygame.mixer.unpause()

# Menu de fin
police_grande = pygame.font.SysFont(None, 80)
police_petite = pygame.font.Font("asset/polices/Coolvetica Rg.otf", 36)

bouton_rejouer= pygame.Rect(490, 350, 300, 50)
bouton_menu = pygame.Rect(490, 420, 300, 50)
bouton_quitter = pygame.Rect(490, 490, 300, 50)

background_game_over = pygame.image.load("images/Fonds/image3.jpg").convert() 
background_game_over = pygame.transform.scale(background_game_over, (1280, 720))

clic = sfxboutton
clic.set_volume(0.5)
# -------------------------------------------------------------------------------------------------#
# Niveau 2
# -------------------------------------------------------------------------------------------------#
fond_caronte = pygame.transform.scale(pygame.image.load("images/Fonds/fond_caronte.png").convert_alpha(), (screen_width * 2,screen_height * 2))

bateau_plat = get_bateau()
bateau_img1 = pygame.image.load("images/Divers/bateau_1.png").convert_alpha()
bateau_img2 = pygame.image.load("images/Divers/bateau_2.png").convert_alpha()
bateau_rame_casse = pygame.transform.scale(pygame.image.load("images/Divers/bateau_rame_casse.png").convert_alpha(), (bateau_plat[0].width, bateau_plat[0].height))
rame_casse = pygame.transform.scale(pygame.image.load("images/Divers/rame_casse.png").convert_alpha(), (63,36))
rame_casse_plat = rame_casse.get_rect(topleft=(2900,780))
rame_interaction_rect = rame_casse_plat.inflate(80, 80)

bateau_image = []
bateau_image2 = []
for bat in bateau_plat:
    img = pygame.transform.scale(bateau_img1,(bat.width,bat.height))
    bateau_image.append(img)
for bat in bateau_plat:
    img2 = pygame.transform.scale(bateau_img2,(bat.width,bat.height))
    bateau_image2.append(img2)
monstres_niveau2 = []
dernier_spawn_monstre = 0
spawn_delay = random.randint(4500,5500) 
nombre_de_monstre = 0
nombre_monstres_tues = 0

musique_niveau2 = sfx.niveau_2caronte

sol_bateau = bateau_plat[0]
caronte_aide = False
bateau_reparer = True
rame_ramasser = True
active_rame = False
donner_rame = False
palier_bateau_index = 0

caronte_rame_dialogue_fait = False

message_caronte_rame = "Oh non ! La rame s'est cassée. Va la\nramasser !"
message_caronte_rame_counter = 0
message_caronte_rame_done = False
caronte2 = caronte_niveau2()

# Plateforme du niveau 2 pour réparer le bateau de Caronte
niveau2_plat = get_niveau2()
niveau2_images = []
for plat in niveau2_plat:
    img = pygame.transform.scale(plateforme2_img,(plat.width,plat.height))
    niveau2_images.append(img)
start_time = pygame.time.get_ticks()
# -------------------------------------------------------------------------------------------------#
# Boucle principale
# -------------------------------------------------------------------------------------------------#
running = True
jump_key_held = False
ground_jump_consumed = False
while running:
    clock.tick(60)
    current_time  = pygame.time.get_ticks()
    if not joueur.peut_bouger and current_time - start_time >= 500 and etat == "jeu":
        if not (dialogue_g or dialogue_v or dialogue_c1 or dialogue_caronte or dialogue_caronte_fin or choix_active or message_reponse_active or lire_pancarte or inventaire_affiche or caronte_aide or fin_caronte_declenchee or transition_caronte_fin_start):
            joueur.peut_bouger = True
    synchroniser_bottes_double_saut()
    synchroniser_couteau()

    button_offset = int(math.sin(current_time * 0.01) * 3)
    if niveau_actuel == 1:
        active_porte = joueur.rect.colliderect(porte_rect)
        active = joueur.rect.colliderect(giordano_rect)
        active2 = joueur.rect.colliderect(virgilio_rect)
        active3 = joueur.rect.colliderect(condamne1_rect)
        active4 = joueur.rect.colliderect(caronte_rect)
        pancarte_active = joueur.rect.colliderect(panneau_rect) and not panneau_button_hidden
    else:
        active = active2 = active3 = active4 = active_porte = False
        pancarte_active = False
        active_rame = joueur.rect.colliderect(rame_interaction_rect)
        donner_rame = joueur.rect.colliderect(caronte2[0])

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

    # ---- Évènements ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if transition_recommencer or transition_porte_enfer_start or transition_caronte_fin_start:
            continue
        if etat == "game_over" and event.type == pygame.MOUSEBUTTONDOWN:
            if bouton_menu.collidepoint(event.pos):
                clic.play(); time.sleep(0.3); pygame.quit(); subprocess.run([sys.executable, "main.py"]); running = False
            elif bouton_quitter.collidepoint(event.pos):
                clic.play(); time.sleep(0.3); running = False
            elif bouton_rejouer.collidepoint(event.pos):
                reset()
            continue
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Double jump
                if joueur.peut_bouger and joueur.double_saut and joueur.nb_sauts == 1 and not jump_key_held:
                    jump_key_held = True
                    joueur.vel_y = joueur.jump_force
                    joueur.nb_sauts = 2
                    joueur.demarrer_animation_saut()
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
            # Mettre en pause avec echappe
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
                        pause_ouvrir_sfx.play()
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
                        sfx.pausesfxbutton.play()
                        pause_hover_index = pause_selected
                if event.key == pygame.K_UP:
                    ancien_pause_selected = pause_selected
                    pause_selected = (pause_selected - 1) % len(boutons_pause)
                    if pause_selected != ancien_pause_selected:
                        sfx.pausesfxbutton.play()
                        pause_hover_index = pause_selected
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    action = boutons_pause[pause_selected]["action"]
                    sfx.choisirsfx.play()
                    if action == "reprendre":
                        en_pause = False
                        joueur.peut_bouger = not (lire_pancarte or inventaire_affiche or dialogue_g or dialogue_v or dialogue_c1 or dialogue_caronte)
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
                    elif action == "recommencer":
                        transition_recommencer = True
                        transition_start = current_time
            if event.key == pygame.K_e and caronte_aide:
                if not message_caronte_rame_done:
                    message_caronte_rame_counter = speed * len(message_caronte_rame)
                    carontesfx.stop()
                else:
                    caronte_aide = False
                    caronte_rame_dialogue_fait = True
                    joueur.peut_bouger = True
            if event.key == pygame.K_e and not rame_ramasser and active_rame:
                rame_ramasser = True
            if event.key == pygame.K_e and rame_ramasser and donner_rame and not bateau_reparer:
                niveau2_bg_offset = current_time - freeze_bg
                bateau_reparer = True
                rame_ramasser = False
                if palier_bateau_index >= len(paliers_bateau) - 1 and nombre_de_monstre >= paliers_bateau[-1]:
                    fin_caronte_declenchee = True
                    joueur.peut_bouger = False
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
                            if not inventaire_contient("bottes"):
                                ajouter_objet_inventaire("bottes")
                                sfx.objetsfx.play()
                            if current_time - virgilio_cooldown > duree_cooldown and vies < 3:
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
                            if not inventaire_contient("couteau"):
                                ajouter_objet_inventaire("couteau")
                                sfx.objetsfx.play()
                                condamne1_dialogue_cooldown = current_time
                elif event.key == pygame.K_e and active3 and not dialogue_c1:
                    if current_time - condamne1_dialogue_cooldown > duree_dialogue_cooldown:
                        dialogue_c1 = True
                        joueur.peut_bouger = False
                        counter = 0
                        active_message_c1 = 0
                        message3 = message_c1[0]
                #---Caronte
                elif event.key == pygame.K_e and dialogue_caronte:
                    if not done:
                        counter = speed * len(message4)
                        carontesfx.stop()
                    else:
                        if active_message_caronte < len(message_caronte) - 1:
                            active_message_caronte += 1
                            message4 = message_caronte[active_message_caronte]
                            counter = 0
                            done = False
                        else:
                            dialogue_caronte = False
                            done = False
                            active_message_caronte = 0
                            counter = 0
                            choix_active = True

                elif event.key == pygame.K_1 and choix_active:
                    choix_active = False
                    choix_fait = 1
                    message_reponse_active = True
                    message_reponse_index = 0
                    message_reponse_counter = 0
                    message_reponse_done = False
                    joueur.peut_bouger = False

                elif event.key == pygame.K_2 and choix_active:
                    choix_active = False
                    choix_fait = 2
                    message_reponse_active = True
                    message_reponse_index = 1
                    message_reponse_counter = 0
                    message_reponse_done = False
                    joueur.peut_bouger = False


                elif event.key == pygame.K_e and message_reponse_active:
                    if not message_reponse_done:
                        message_reponse_counter = speed * len(message5[message_reponse_index])
                        carontesfx.stop()
                    else:
                        message_reponse_active = False
                        joueur.peut_bouger = True
                        if choix_fait == 1:
                            transition_caronte_start = current_time
                            transition_caronte_teleporte = False
                            joueur.peut_bouger = False
                        elif choix_fait == 2:
                            pass
                        caronte_dialogue_cooldown = current_time
                        choix_fait = None

                elif event.key == pygame.K_e and active4 and not dialogue_caronte and not dialogue_caronte_fin and not choix_active and not message_reponse_active:
                    if current_time - caronte_dialogue_cooldown > duree_dialogue_cooldown:
                        dialogue_caronte = True
                        joueur.peut_bouger = False
                        counter = 0
                        active_message_caronte = 0
                        message4 = message_caronte[0]
                        done = False
                elif event.key == pygame.K_e and dialogue_caronte_fin:
                    if not done:
                        counter = speed * len(message4)
                        carontesfx.stop()
                    else:
                        if active_message_caronte < len(message_caronte_fin) - 1:
                            active_message_caronte += 1
                            message4 = message_caronte_fin[active_message_caronte]
                            counter = 0
                            done = False
                        else:
                            dialogue_caronte_fin = False
                            active_message_caronte = 0
                            counter = 0
                            done = False
                            joueur.peut_bouger = True

                elif event.key == pygame.K_e and active_porte:
                    transition_porte_enfer_start = current_time
                    joueur.peut_bouger = False
            if event.key == pygame.K_f and inventaire_active and not inventaire_affiche and not lire_pancarte and not dialogue_g and not dialogue_v and not dialogue_c1 and not dialogue_caronte and not dialogue_caronte_fin and not choix_active and not message_reponse_active and not fin_caronte_declenchee:
                sfx.ouvrir_inv.play()
                inventaire_affiche = True
                joueur.peut_bouger = False
                inventaire_timer = current_time
                show_button_f_inventaire = False
            elif event.key == pygame.K_f and inventaire_affiche:
                sfx.fermer_inv.play()
                inventaire_affiche = False
                show_button_f_inventaire = False
                tooltip_inventaire_visible = False
                inventaire_index_selectionne = None
                joueur.peut_bouger = True
        if event.type == pygame.MOUSEMOTION and en_pause and not afficher_parametres_pause:
            mx, my = event.pos
            for i, bouton in enumerate(boutons_pause):
                y_bouton = 280 + i * 80
                x_bouton = screen_width // 2 - pause_button_width // 2
                rect_bouton = pygame.Rect(x_bouton, y_bouton, pause_button_width, pause_button_height)
                if rect_bouton.collidepoint(mx, my):
                    if pause_hover_index != i:
                        sfx.pausesfxbutton.play()
                    pause_selected = i
                    pause_hover_index = i

        if event.type == pygame.MOUSEBUTTONDOWN:
            if afficher_parametres_pause:
                if fermer_pause_rect.collidepoint(event.pos):
                    afficher_parametres_pause = False
                    sfx.retoursfx.play()
                else:
                    for parametre in parametres_toggles_pause:
                        if parametre["rect"].collidepoint(event.pos):
                            parametre["enabled"] = not parametre["enabled"]
                            appliquer_parametre_jeu(parametre["name"], parametre["enabled"])
                            sfx.pausesfxbutton.play()
                            break
            elif en_pause:
                mx, my = event.pos
                for i, bouton in enumerate(boutons_pause):
                    y_bouton = 280 + i * 80
                    x_bouton = screen_width // 2 - pause_button_width // 2
                    rect_bouton = pygame.Rect(x_bouton, y_bouton, pause_button_width, pause_button_height)
                    if rect_bouton.collidepoint(mx, my):
                        action = bouton["action"]
                        sfx.choisirsfx.play()  # ← son de sélection au clic
                        if action == "reprendre":
                            en_pause = False
                            joueur.peut_bouger = not (lire_pancarte or inventaire_affiche or dialogue_g or dialogue_v or dialogue_c1 or dialogue_caronte)
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
                        elif action == "recommencer":
                            transition_recommencer = True
                            transition_start = current_time
            else:
                if inventaire_affiche:
                    tooltip_clique = False
                    if tooltip_inventaire_visible and inventaire_index_selectionne is not None:
                        slot_rect = get_slot_inventaire_rect(inventaire_index_selectionne)
                        tooltip_equiper_rect = pygame.Rect(slot_rect.right + 10, slot_rect.y, 130, 40)
                        if tooltip_equiper_rect.collidepoint(event.pos):
                            tooltip_clique = True
                            sfx.selectsfx.play()
                            item_id = inventaire[inventaire_index_selectionne]["id"]
                            if item_id == "bottes":
                                if bottes_equipees:
                                    joueur.double_saut = False
                                    bottes_equipees = False
                                else:
                                    joueur.double_saut = True
                                    bottes_equipees = True
                            if item_id == "couteau":
                                joueur.couteau_equipee = not joueur.couteau_equipee
                            tooltip_inventaire_visible = False

                    if not tooltip_clique:
                        for index, item in enumerate(inventaire):
                            slot_rect = get_slot_inventaire_rect(index)
                            if slot_rect.collidepoint(event.pos):
                                sfx.selectsfx.play()
                                inventaire_index_selectionne = index
                                tooltip_inventaire_visible = ITEMS_INVENTAIRE[item["id"]]["utilisable"]
                                break
    
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
            joueur.demarrer_animation_saut()
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
    for plat in plateformes_mobiles:
        old_x, old_y = plat.rect.x,plat.rect.y
        plat.update()
    # Transporte le joueur si il est dessus
        dx_plat = plat.rect.x - old_x
        dy_plat = plat.rect.y - old_y
        joueur_sur_plat = (
            joueur.rect.bottom >= plat.rect.top and
            joueur.rect.bottom <= plat.rect.top + 15 and
            joueur.rect.right > plat.rect.left and
            joueur.rect.left < plat.rect.right
        )
        if joueur_sur_plat:
            joueur.rect.x += dx_plat
            joueur.rect.y += dy_plat
    # Permet d'ajouter la collisions avec les plateformes sur les niveaux
    if not en_pause and not transition_recommencer and not transition_porte_enfer_start and etat != "mort":

# --------------------------------------------------
# NIVEAU 1
# --------------------------------------------------

        if niveau_actuel == 1:
            rects_mobiles = [p.rect for p in plateformes_mobiles]
            joueur.deplacement(plateformes + plateformes_prison + sol + sol2 + mur2 + plateformes2 + rects_mobiles)
            joueur.appliquer_gravite(plateformes + plateformes_prison + sol + sol2 + mur2 + plateformes2 + rects_mobiles, murs=plateformes_haute)
            joueur.update_double_jump_effects()

            if not invincible:
                for plat_danger in plateformes_danger + plateformes_danger2:
                    if joueur.rect.colliderect(plat_danger):
                        vies -= 1
                        sfx.degat.play()
                        invincible = True
                        invincibilite_temps = current_time
                        if vies <= 0:
                            pause_active = False
                            inventaire_active = False
                            etat = "mort"
                            death_animation_start = current_time
                            death_sound_stage = 0
                            joueur.peut_bouger = False
                            joueur.is_animating = False
                            couper_sons_pour_mort()
                            break

            vies, invincible, invincibilite_temps, mort = monstre.update_and_collide(
                joueur,
                plateformes + plateformes_prison + sol + sol2 + plateformes_haute,
                vies, invincible, current_time, invincibilite_temps, duree_invincibilite,
            )
            if mort:
                sfx.degat.play()
            if invincible and current_time - invincibilite_temps > duree_invincibilite:
                invincible = False
# --------------------------------------------------
# NIVEAU 2
# --------------------------------------------------

        elif niveau_actuel == 2:
            ambient.stop()
            joueur.update_double_jump_effects()
            bateau_plat_reparer = [bateau_plat[0], bateau_plat[1], bateau_plat[3], bateau_plat[5]]
            if bateau_reparer:
                joueur.deplacement(bateau_plat)
                joueur.appliquer_gravite(bateau_plat)
                if palier_bateau_index < len(paliers_bateau) and nombre_de_monstre >= paliers_bateau[palier_bateau_index] and not caronte_aide and len(monstres_niveau2) == 0:
                    freeze_bg = current_time - niveau2_bg_offset
                    bateau_reparer = False
                    caronte_aide = True
                    message_caronte_rame_counter = 0
                    message_caronte_rame_done = False
                    joueur.peut_bouger = False
            #  SPAWN DES MONSTRES
            if not fin_caronte_declenchee and palier_bateau_index < len(paliers_bateau) and current_time - dernier_spawn_monstre > spawn_delay and nombre_de_monstre < paliers_bateau[palier_bateau_index]:
                if random.choice(["monstre", "esprit", "squelette"]) == "monstre":
                    m = Monstre(1250, 550)
                    m.distance_activation = 1500
                    monstres_niveau2.append(m)
                    nombre_de_monstre += 1

                elif random.choice(["esprit", "squelette"]) == "esprit":
                    e = Esprit(1250, 550)
                    monstres_niveau2.append(e)
                    nombre_de_monstre += 1
                else:
                    monstres_niveau2.append(Squelette(1250, bateau_plat[4].top - 150))
                    nombre_de_monstre += 1

                dernier_spawn_monstre = current_time
                spawn_delay = random.randint(500,500)

            plateforme_monstre = bateau_plat[4]
            for m in monstres_niveau2[:]:
                if isinstance(m, Monstre):
                    vies, invincible, invincibilite_temps, mort = m.update_and_collide(
                        joueur, [bateau_plat[0], bateau_plat[4]], vies, invincible,
                        current_time, invincibilite_temps, duree_invincibilite,
                    )
                else:  # Esprit et Squelette ont la même signature
                    vies, invincible, invincibilite_temps, mort = m.update_and_collide(
                        joueur, [bateau_plat[0], bateau_plat[4]], vies, invincible,
                        current_time, invincibilite_temps, duree_invincibilite,)
                if mort:
                    sfx.degat.play()

                if not m.vivant:
                    nombre_monstres_tues += 1
                    monstres_niveau2.remove(m)
            if vies <= 0 and etat != "mort":
                etat = "mort"
                death_animation_start = current_time
                death_sound_stage = 0
                joueur.peut_bouger = False
                joueur.is_animating = False
                couper_sons_pour_mort()

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

    if etat == "mort" and death_animation_done:
        etat = "game_over"
    if etat == "game_over":
        screen.blit(background_game_over, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        color_menu    = (0, 255, 0)  if bouton_menu.collidepoint(mouse_pos)    else (0, 200, 0)
        color_quitter = (255, 0, 0)  if bouton_quitter.collidepoint(mouse_pos) else (200, 0, 0)
        color_rejouer = (0, 255, 0)  if bouton_rejouer.collidepoint(mouse_pos) else (0, 200, 0)
        pygame.draw.rect(screen, color_menu,    bouton_menu)
        pygame.draw.rect(screen, color_quitter, bouton_quitter)
        pygame.draw.rect(screen, color_rejouer, bouton_rejouer)
        texte         = police_grande.render("GAME OVER", True, (255, 0, 0))
        texte_menu    = police_petite.render("Menu Début", True, (255, 255, 255))
        texte_quitter = police_petite.render("Quitter",    True, (255, 255, 255))
        texte_rejouer = police_petite.render("Rejouer",    True, (255, 255, 255))
        screen.blit(texte,         (640 - texte.get_width() // 2, 250))
        screen.blit(texte_menu,    (bouton_menu.centerx    - texte_menu.get_width()    // 2, bouton_menu.centery    - texte_menu.get_height()    // 2))
        screen.blit(texte_quitter, (bouton_quitter.centerx - texte_quitter.get_width() // 2, bouton_quitter.centery - texte_quitter.get_height() // 2))
        screen.blit(texte_rejouer, (bouton_rejouer.centerx - texte_rejouer.get_width() // 2, bouton_rejouer.centery - texte_rejouer.get_height() // 2))
        screen.blit(curseur_img, mouse_pos)
        pygame.display.flip()
        continue
    
    # ---- Camera ----

    if not en_pause:
        if niveau_actuel == 1:
            camera_x += (joueur.rect.centerx - screen_width // 2 - camera_x) * 0.11
            if joueur.rect.centerx < 2000:
                camera_x = max(0, min(camera_x, 2000 - screen_width))
            else:
                camera_x = max(2000, min(camera_x, 4100 - screen_width))
            camera_y += (joueur.rect.centery - screen_height // 2 + camera_y_offset - camera_y) * 0.11
            camera_y = max(0, camera_y)
        elif niveau_actuel == 2:
            camera_x += (joueur.rect.centerx - screen_width // 2 - camera_x) * 0.11
            camera_x = max(0, camera_x)
            camera_y += (250 - camera_y) * 0.11
        
    if niveau_actuel == 1:
        if joueur.rect.centerx >= 2000:
            bg_x = -(camera_x - 2000) * parallax_factor + bg_offset_x - bg_width // 2
        else:
            bg_x = -camera_x * parallax_factor + bg_offset_x
        bg_y = -camera_y * parallax_factor + bg_offset_y

        if joueur.rect.centerx >= 2000:
            bg_x = -(camera_x - 2000) * parallax_factor + bg_offset_x - bg_width // 2
        else:
            bg_x = -camera_x * parallax_factor + bg_offset_x
        bg_y = -camera_y * parallax_factor + bg_offset_y
    elif niveau_actuel == 2:
        if bateau_reparer:
            t = current_time - niveau2_bg_offset
        else:
            t = freeze_bg
        bg_x = (-camera_x * parallax_factor + bg_offset_x + (t * -0.02)) % fond_caronte.get_width()
        bg_y = -camera_y * parallax_factor + bg_offset_y

    if etat != "mort" or death_animation_start is None:
        pass
    else:
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
                    sfx.coeurmort.set_volume(0.5)
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
                            sfx.satan.set_volume(0.5)
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
            if death_elapsed >= DEATH_GAME_OVER_DELAY_MS:
                death_animation_done = True
        pygame.display.flip()
        continue

    # ========================
    # RENDU
    # ========================
    if niveau_actuel == 1:
        screen.blit(background, (bg_x, bg_y + 100))
        screen.blit(porte, (porte_rect.x - camera_x, porte_rect.y - camera_y))
        screen.blit(panneau, (panneau_rect.x - camera_x, panneau_rect.y - camera_y))
        screen.blit(giordano_images[current_giordano], (giordano_rect.x - camera_x, giordano_rect.y - camera_y))
        screen.blit(virgilio, (virgilio_rect.x - camera_x, virgilio_rect.y - camera_y))
        screen.blit(condamne1, (condamne1_rect.x - camera_x, condamne1_rect.y - camera_y))
        screen.blit(caronte, (caronte_rect.x - camera_x, caronte_rect.y - camera_y))
        screen.blit(bateau,(bateau_rect.x - camera_x,bateau_rect.y - camera_y))
    elif niveau_actuel == 2:
        screen.blit(fond_caronte, (bg_x - fond_caronte.get_width(), bg_y + 100))
        screen.blit(fond_caronte, (bg_x, bg_y + 100))
    # Monstre
    monstre.draw(screen, camera_x, camera_y)


    # Joueur
    afficher_joueur = True
    if invincible:
        afficher_joueur = (current_time // 100) % 2 == 0
    if afficher_joueur:
        sprite_offset_x = joueur.draw_offset_x_left if joueur.facing_left else joueur.draw_offset_x
        sprite_x = joueur.rect.centerx - camera_x - joueur.image.get_width() // 2 + sprite_offset_x
        sprite_y = joueur.rect.bottom - camera_y - joueur.image.get_height() + joueur.draw_offset_y
        screen.blit(joueur.image, (sprite_x, sprite_y))
    if joueur.is_attacking:
        hitbox_screen_x = joueur.hitbox_couteau.x - camera_x
        hitbox_screen_y = joueur.hitbox_couteau.y - camera_y
    # HUD cooldown attaque
    if joueur.couteau_equipee:
        temps_actuel_cd = pygame.time.get_ticks()
        temps_ecoule = temps_actuel_cd - joueur.cooldown_attaque
        if temps_ecoule < 2500:
            # 5 images réparties sur 2500ms → chaque image dure 500ms
            frame_cd = min(int(temps_ecoule / 500), 4)
            img_cd = pygame.transform.scale(
                pygame.image.load(f"images/cooldown/cooldown{frame_cd}.png").convert_alpha(),
                (51, 15)
            )
            screen.blit(img_cd, (joueur.rect.x - camera_x, joueur.rect.y - camera_y - 70))
#-----------------------------------------------
# RENDU DES PLATEFORMES
#-----------------------------------------------
# Parcours deux listes avec zip, celles des plateformes et des images correspondantes, pour afficher chaque plateforme à sa position avec la bonne image.
    if niveau_actuel == 1:
        # Murs prison
        for mur, img in zip(plateformes_prison, mur_prison_images):
            screen.blit(img, (mur.x - camera_x, mur.y - camera_y))
        # Plateformes normales
        for plat, img in zip(plateformes, platform_images):
            if img:
                screen.blit(img, (plat.x - camera_x, plat.y - camera_y))

        # Plateformes mobiles
        for plat in plateformes_mobiles:
            if plateforme_petite_orig:
                img = pygame.transform.scale(plateforme2_img, (plat.rect.width, plat.rect.height))
                screen.blit(img,(plat.rect.x - camera_x, plat.rect.y - camera_y))
        # Sol2
        for s, img in zip(sol2, sol2_images):
            screen.blit(img, (s.x - camera_x, s.y - camera_y))
        # Plateforme2
        for s, img in zip(plateformes2, plateforme2_images):
            if img:
                screen.blit(img, (s.x - camera_x, s.y - camera_y))

        # Sol
        for s, img in zip(sol, sol_images):
            screen.blit(img, (s.x - camera_x, s.y - camera_y - 15))

        # Mur2
        for s, img in zip(mur2, mur2_images):
            if img:
                screen.blit(img, (s.x - camera_x, s.y - camera_y))

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
        if pancarte_active:
            screen.blit(bouton_e, (bouton_e_rect.x - camera_x - 700, bouton_e_rect.y - camera_y + button_offset))

    # NIVEAU 2
    # Bateau du niveau avec Caronte
    if niveau_actuel == 2:
        img_bateau = bateau_image if (current_time // 500) % 2 == 0 else bateau_image2
        for i, plat in enumerate(bateau_plat):
            if i == 0:
                if not bateau_reparer:
                    screen.blit(bateau_rame_casse, (plat.x - camera_x, plat.y - camera_y - 100))
                else:
                    screen.blit(img_bateau[i], (plat.x - camera_x, plat.y - camera_y - 100))

        for m in monstres_niveau2:
            m.draw(screen, camera_x, camera_y)

        if caronte_aide:
            bateau_reparer = False
            rame_ramasser = False
            joueur.peut_bouger = False
            joueur.is_animating = False
            if not en_pause and message_caronte_rame_counter < speed * len(message_caronte_rame):
                message_caronte_rame_counter += 1
                if message_caronte_rame_counter % speed == 0 and carontesfx.get_num_channels() == 0:
                    carontesfx.play()
            elif message_caronte_rame_counter >= speed * len(message_caronte_rame):
                carontesfx.stop()
                message_caronte_rame_done = True
                screen.blit(bouton_e, (1020, 550 + button_offset))
        if not bateau_reparer:
            joueur.deplacement(bateau_plat_reparer + niveau2_plat)
            joueur.appliquer_gravite(bateau_plat_reparer + niveau2_plat)
            if not rame_ramasser:
                screen.blit(rame_casse, (rame_casse_plat.x - camera_x + 100, rame_casse_plat.y - camera_y))
                if active_rame:
                    screen.blit(bouton_e, (rame_casse_plat.x - camera_x + 20, rame_casse_plat.y - camera_y +  + button_offset - 20))
        if rame_ramasser and donner_rame and not bateau_reparer:
            screen.blit(bouton_e, (sol_bateau.centerx - camera_x - 25, sol_bateau.y - camera_y - 70 + button_offset))

        # Plateforme niveau 2 pour reparer le bateau
        for s, img in zip(niveau2_plat, niveau2_images):
            if img:
                if not bateau_reparer:
                    screen.blit(img, (s.x - camera_x, s.y - camera_y))

# -----------------------------------------------------------------------------------------
    # HITBOXES DEBUG
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

    # Effets double saut
    for effect in joueur.double_jump_effects:
        effect_surface = pygame.Surface((effect['width'], effect['height']), pygame.SRCALPHA)
        effect_surface.fill((255, 255, 255, effect['alpha']))
        screen.blit(effect_surface, (effect['x'] - camera_x - effect['width'] // 2, effect['y'] - camera_y))

    # HUD Vies  ← en dehors du if, pour les deux niveaux
    if not lire_pancarte:
        screen.blit(vie_text, (20, 20))
        for i in range(vies):
            screen.blit(coeur, (230 + i * 110, 5))
    # HUD  Icône double saut
    if joueur.double_saut and not lire_pancarte:
        screen.blit(double_jump, (screen_width - 150, screen_height - 260))

    # HUD  Icône inventaire
    if not lire_pancarte and not dialogue_g and not dialogue_v and not dialogue_c1 and not dialogue_caronte:
        screen.blit(icone_inventaire, (screen_width - 150, screen_height - 150))
        screen.blit(lettre_f, (screen_width - 107, screen_height - 175))

    joueur.update()

    # Zone de détection joueur pour les NPC
    # Giordano  bouton E + dialogue
    if active and not dialogue_g and current_time - giordano_dialogue_cooldown > duree_dialogue_cooldown:
        screen.blit(bouton_e, (bouton_e_rect.x - camera_x, bouton_e_rect.y - camera_y + button_offset))
    if dialogue_g:
        texte_affiche = message[0:counter // speed]
        joueur.peut_bouger = False
        joueur.is_animating = False
        screen.blit(cadre_g, cadre_g_rect)
        for i, ligne in enumerate(texte_affiche.split("\n")):
            snip = police.render(ligne, True, '#4f2310')
            screen.blit(snip, (480, 470 + i * 30))
        if not en_pause and counter < speed * len(message):
            counter += 1
            if counter % speed == 0 and npcsfx.get_num_channels() == 0:
                npcsfx.play()
        elif counter >= speed * len(message):
            npcsfx.stop()
            done = True
            screen.blit(bouton_e, (1000, 600 + button_offset))

    # Virgilio  bouton E + dialogue
    if active2 and not dialogue_v and current_time - virgilio_dialogue_cooldown > duree_dialogue_cooldown:
        screen.blit(bouton_e, ((bouton_e_rect.x - 900) - camera_x, (bouton_e_rect.y - 2110) - camera_y + button_offset))
    if dialogue_v:
        texte_affiche = message2[0:counter // speed]
        joueur.peut_bouger = False
        joueur.is_animating = False
        screen.blit(cadre_v, cadre_v_rect)
        for i, ligne in enumerate(texte_affiche.split("\n")):
            snip = police.render(ligne, True, '#4f2310')
            screen.blit(snip, (480, 470 + i * 30))
        if not en_pause and counter < speed * len(message2):
            counter += 1
            if counter % speed == 0 and npcsfx.get_num_channels() == 0:
                npcsfx.play()
        elif counter >= speed * len(message2):
            npcsfx.stop()
            done = True
            screen.blit(bouton_e, (1020, 550 + button_offset))

    # Condamné1  bouton E + dialogue
    if active3 and not dialogue_c1 and current_time - condamne1_dialogue_cooldown > duree_dialogue_cooldown:
        screen.blit(bouton_e, ((280) - camera_x,(5730) - camera_y + button_offset))
    if dialogue_c1:
        texte_affiche = message3[0:counter // speed]
        joueur.peut_bouger = False
        joueur.is_animating = False
        screen.blit(cadre_c1, cadre_c1_rect)
        for i, ligne in enumerate(texte_affiche.split("\n")):
            snip = police.render(ligne, True, '#4f2310')
            screen.blit(snip, (480, 470 + i * 30))
        if not en_pause and counter < speed * len(message3):
            counter += 1
            if counter % speed == 0 and condamnesfx.get_num_channels() == 0:
                condamnesfx.play()
        elif counter >= speed * len(message3):
            condamnesfx.stop()
            done = True
            screen.blit(bouton_e, (1020, 550 + button_offset))

    # Caronte bouton E + dialogue
    if active4 and not dialogue_caronte and not choix_active and not message_reponse_active and current_time - caronte_dialogue_cooldown > duree_dialogue_cooldown:
        screen.blit(bouton_e,(caronte_rect.centerx - camera_x + 50, caronte_rect.y - camera_y - 35 + button_offset))
    if dialogue_caronte:
        texte_affiche = message4[0:counter // speed]
        joueur.peut_bouger = False
        joueur.is_animating = False
        screen.blit(cadre_caronte, cadre_caronte_rect)
        for i, ligne in enumerate(texte_affiche.split("\n")):
            snip = police.render(ligne, True, '#4f2310')
            screen.blit(snip, (480, 470 + i * 30))
        if not en_pause and counter < speed * len(message4):
            counter += 1
            if counter % speed == 0 and carontesfx.get_num_channels() == 0:
                carontesfx.play()
        elif counter >= speed * len(message4):
            carontesfx.stop()
            done = True
            screen.blit(bouton_e, (1020, 550 + button_offset))
    if dialogue_caronte_fin:
        texte_affiche = message4[0:counter // speed]
        joueur.peut_bouger = False
        joueur.is_animating = False
        screen.blit(cadre_caronte, cadre_caronte_rect)
        for i, ligne in enumerate(texte_affiche.split("\n")):
            snip = police.render(ligne, True, '#4f2310')
            screen.blit(snip, (480, 470 + i * 30))
        if not en_pause and counter < speed * len(message4):
            counter += 1
            if counter % speed == 0 and carontesfx.get_num_channels() == 0:
                carontesfx.play()
        elif counter >= speed * len(message4):
            carontesfx.stop()
            done = True
            screen.blit(bouton_e, (1020, 550 + button_offset))
    # Cadre de choix Caronte
    if choix_active:
        joueur.peut_bouger = False 
        joueur.is_animating = False
        screen.blit(choix_cadre, choix_cadre_rect)
    # Message de réponse de Caronte après le choix
    if message_reponse_active:
        texte_rep = message5[message_reponse_index][0:message_reponse_counter // speed]
        screen.blit(cadre_caronte, cadre_caronte_rect)
        for i, ligne in enumerate(texte_rep.split("\n")):
            snip = police.render(ligne, True, '#4f2310')
            screen.blit(snip, (480, 470 + i * 30))
        if not en_pause and message_reponse_counter < speed * len(message5[message_reponse_index]):
            message_reponse_counter += 1
            if message_reponse_counter % speed == 0 and carontesfx.get_num_channels() == 0:
                carontesfx.play()
        elif message_reponse_counter >= speed * len(message5[message_reponse_index]):
            carontesfx.stop()
            message_reponse_done = True
            screen.blit(bouton_e, (1020, 550 + button_offset))
    if caronte_aide:
        texte_affiche = message_caronte_rame[0:message_caronte_rame_counter // speed]
        screen.blit(cadre_caronte, cadre_caronte_rect)
        for i, ligne in enumerate(texte_affiche.split("\n")):
            snip = police.render(ligne, True, '#4f2310')
            screen.blit(snip, (480, 470 + i * 30))
        if message_caronte_rame_done:
            screen.blit(bouton_e, (1020, 550 + button_offset))
    # Titre "L'Enfer"
    if not en_pause and titre_index < speed * len(titre):
        titre_index += 1
        if titre_index % speed == 0:
            titre_sfx.play()
    elif not en_pause and titre_index >= speed * len(titre) and titre_fin == 0:
        titre_sfx.stop()
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
        for index, item in enumerate(inventaire):
            slot_rect = get_slot_inventaire_rect(index)
            item_data = ITEMS_INVENTAIRE[item["id"]]
            screen.blit(frame_inventaire, slot_rect.topleft)
            screen.blit(item_data["image"], slot_rect.topleft)
            if item["id"] == "bottes" and bottes_equipees:
                pygame.draw.rect(screen, (255, 215, 0), slot_rect, 3)
            elif item["id"] == "couteau" and couteau_equipee:
                pygame.draw.rect(screen, (255, 215, 0), slot_rect, 3)
            elif inventaire_index_selectionne == index:
                pygame.draw.rect(screen, (255, 255, 255), slot_rect, 2)

        if tooltip_inventaire_visible and inventaire_index_selectionne is not None and inventaire_index_selectionne < len(inventaire):
            item = inventaire[inventaire_index_selectionne]
            item_data = ITEMS_INVENTAIRE[item["id"]]
            action_label = item_data["action_label"]()
            if action_label:
                slot_rect = get_slot_inventaire_rect(inventaire_index_selectionne)
                tooltip_rect = pygame.Rect(slot_rect.right + 10, slot_rect.y, 130, 40)
                pygame.draw.rect(screen, (40, 40, 40), tooltip_rect)
                pygame.draw.rect(screen, (200, 200, 200), tooltip_rect, 2)
                label = police.render(action_label, True, (255, 255, 255))
                screen.blit(label, (tooltip_rect.x + 7, tooltip_rect.y + 10))

        if False and bottes_dans_inventaire:
            screen.blit(bottes, (400, 250))
            if bottes_equipees:
                pygame.draw.rect(screen, (255, 215, 0), (400, 250, 80, 80), 3)
            if tooltip_bottes_visible:
                tooltip_rect = pygame.Rect(490, 250, 130, 40)
                pygame.draw.rect(screen, (40, 40, 40), tooltip_rect)
                pygame.draw.rect(screen, (200, 200, 200), tooltip_rect, 2)
                texte_tooltip = "Déséquiper" if bottes_equipees else "Équiper"
                label = police.render(texte_tooltip, True, (255, 255, 255))
                screen.blit(label, (497, 260))
        if not inventaire:
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

    # Menu paramètres (par-dessus la pause)
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
    if niveau_actuel == 2 and not lire_pancarte:
        if palier_bateau_index < len(paliers_bateau):
            compteur_monstres = f"Monstres tues : {nombre_monstres_tues}/{paliers_bateau[palier_bateau_index]}"
        else:
            compteur_monstres = f"Monstres tues : {nombre_monstres_tues}/{paliers_bateau[-1]}"
        dessiner_texte_contour(screen, police, compteur_monstres, screen_width - 20, 70, "#ffffff", "#000000", epaisseur=4)
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
        elif temps_transition_porte < 1000:
            alpha = 255
            if not transition_porte_teleporte:
                joueur.rect.center = (2100, 6500)
                joueur.vel_y = 0
                joueur.vx = 0
                transition_porte_teleporte = True
        elif temps_transition_porte < 1500:
            alpha = int((1 - (temps_transition_porte - 1000) / 500) * 255)
        else:
            transition_porte_enfer_start = 0
            joueur.peut_bouger = not (en_pause or lire_pancarte or inventaire_affiche or dialogue_g or dialogue_v or dialogue_c1 or dialogue_caronte)
            alpha = 0
        if alpha > 0:
            fondu = pygame.Surface((screen_width, screen_height))
            fondu.fill((0, 0, 0))
            fondu.set_alpha(alpha)
            screen.blit(fondu, (0, 0))
    if transition_caronte_start:
        temps_transition_caronte = current_time - transition_caronte_start
        if temps_transition_caronte < 500:
            alpha = int((temps_transition_caronte / 500) * 255)
        elif temps_transition_caronte < 1000:
            alpha = 255
            if not transition_caronte_teleporte:
                niveau_actuel = 2
                joueur.rect.topleft = (200, 550)
                joueur.vel_y = 0
                joueur.vx = 0
                transition_caronte_teleporte = True
                musique_niveau2.set_volume(0.3)
                musique_niveau2.play(-1)
        elif temps_transition_caronte < 1500:
            alpha = int((1 - ((temps_transition_caronte - 1000) / 500)) * 255)
        else:
            transition_caronte_start = 0
            transition_caronte_teleporte = False
            joueur.peut_bouger = True
            alpha = 0

        if alpha > 0:
            fondu = pygame.Surface((screen_width, screen_height))
            fondu.fill((0, 0, 0))
            fondu.set_alpha(alpha)
            screen.blit(fondu, (0, 0))
    if transition_caronte_fin_start:
        temps_transition_caronte_fin = current_time - transition_caronte_fin_start
        if temps_transition_caronte_fin < 0:
            alpha = 0
        elif temps_transition_caronte_fin < 1000:
            alpha = int((temps_transition_caronte_fin / 1000) * 255)
        elif temps_transition_caronte_fin < 1500:
            alpha = 255
            if not transition_caronte_fin_teleporte:
                niveau_actuel = 1
                joueur.rect.topleft = (3850, 5380)
                joueur.vel_y = 0
                joueur.vx = 0
                monstres_niveau2 = []
                musique_niveau2.stop()
                if settings.musique:
                    ambient.set_volume(0.1)
                    if ambient.get_num_channels() == 0:
                        ambient.play(-1)
                else:
                    ambient.set_volume(0)
                transition_caronte_fin_teleporte = True
        elif temps_transition_caronte_fin < 2500:
            alpha = int((1 - ((temps_transition_caronte_fin - 1500) / 1000)) * 255)
        else:
            transition_caronte_fin_start = 0
            transition_caronte_fin_teleporte = False
            fin_caronte_declenchee = False
            dialogue_caronte_fin = True
            joueur.peut_bouger = False
            active_message_caronte = 0
            message4 = message_caronte_fin[0]
            counter = 0
            done = False
            alpha = 0

        if alpha > 0:
            fondu = pygame.Surface((screen_width, screen_height))
            fondu.fill((0, 0, 0))
            fondu.set_alpha(alpha)
            screen.blit(fondu, (0, 0))
    pos = pygame.mouse.get_pos()
    screen.blit(curseur_img, pos)
    pygame.display.flip()

pygame.quit()
