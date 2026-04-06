import pygame

pygame.mixer.init(44100)

sfxtitre = pygame.mixer.Sound("asset/sons/Sfx/Titre/titre.mp3")
fin = pygame.mixer.Sound("asset/sons/Sfx/Titre/titre_fin.wav")

# Joueur
sauter = pygame.mixer.Sound("asset/sons/Sfx/Joueur/jump.mp3")
sfxmarche1 = pygame.mixer.Sound("asset/sons/Sfx/Joueur/marche1.mp3")
sfxmarche2 = pygame.mixer.Sound("asset/sons/Sfx/Joueur/marche2.mp3")
sfxmarche3 = pygame.mixer.Sound("asset/sons/Sfx/Joueur/marche3.mp3")
degat = pygame.mixer.Sound("asset/sons/Sfx/Joueur/sfxdegat.mp3")

# Musique
musiquefond = pygame.mixer.Sound("asset/sons/Musique/Enfer.mp3")
musiquemenu = pygame.mixer.Sound("asset/sons/Musique/menu.mp3")
hacker = pygame.mixer.Sound("asset/sons/Musique/hacker.mp3")

# SFX interaction
sfxboutton = pygame.mixer.Sound("asset/sons/Sfx/Boutons/bouton.mp3")
liresfx = pygame.mixer.Sound("asset/sons/Sfx/Boutons/lire.mp3")
stoplire = pygame.mixer.Sound("asset/sons/Sfx/Boutons/stop_lire.mp3")

## NPC
# Giordano et Virgilio
sfxnpc = pygame.mixer.Sound("asset/sons/Sfx/Dialogues/Dialogue.mp3")

# Condamne
dialogue_csfx = pygame.mixer.Sound("asset/sons/Sfx/Dialogues/Dialogue_condamne.mp3")

# Caronte
carontesfx = pygame.mixer.Sound("asset/sons/Sfx/Dialogues/Dialogue_caronte.mp3")

# SFX dans l'inventaire
ouvrir_inv = pygame.mixer.Sound("asset/sons/Sfx/Boutons/ouvrir_inventaire.mp3")
fermer_inv = pygame.mixer.Sound("asset/sons/Sfx/Boutons/fermer_inventaire.mp3")
selectsfx =  pygame.mixer.Sound("asset/sons/Sfx/Boutons/selectionner.mp3")
objetsfx = pygame.mixer.Sound("asset/sons/Sfx/Notifications/item_pick.wav")

# Le joueur tombe
tombersfx = pygame.mixer.Sound("asset/sons/Sfx/Joueur/tomber.mp3")
viesfx = pygame.mixer.Sound("asset/sons/Sfx/Notifications/gain_de_vie.mp3")

# Pause
pausesfxouvrir = pygame.mixer.Sound("asset/sons/Sfx/Boutons/pause_ouvrir.wav")
pausesfxfermer = pygame.mixer.Sound("asset/sons/Sfx/Boutons/pause_fermer.wav")
pausesfxbutton = pygame.mixer.Sound("asset/sons/Sfx/Boutons/pause_button.wav")

# Animation de mort
coeursfx = pygame.mixer.Sound("asset/sons/Sfx/AnimationMort/coeur.mp3")
coeurmort = pygame.mixer.Sound("asset/sons/Sfx/AnimationMort/coeur_mort.mp3")
mortsfx = pygame.mixer.Sound("asset/sons/Sfx/AnimationMort/mort.mp3")
satan = pygame.mixer.Sound("asset/sons/Sfx/AnimationMort/satan.mp3")
