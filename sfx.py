import pygame

pygame.mixer.init(44100)


musiquefond = pygame.mixer.Sound("asset/sons/music_enfer.mp3")
sauter = pygame.mixer.Sound("asset/sons/jump.mp3")
musiquemenu = pygame.mixer.Sound("asset/sons/menu.mp3")
sfxboutton = pygame.mixer.Sound("asset/sons/bouton.mp3")
degat = pygame.mixer.Sound("asset/sons/sfxdegat.mp3")
sfxdialogue = pygame.mixer.Sound("asset/sons/dialogue.mp3")
fin = pygame.mixer.Sound("asset/sons/titre_fin.wav")
sfxnpc = pygame.mixer.Sound("asset/sons/npc.mp3")
hacker = pygame.mixer.Sound("asset/sons/hacker.mp3")
liresfx = pygame.mixer.Sound("asset/sons/lire.mp3")
stoplire = pygame.mixer.Sound("asset/sons/stop_lire.mp3")
dialogue_csfx = pygame.mixer.Sound("asset/sons/dialogue_condamne.mp3")
sfxmarche1 = pygame.mixer.Sound("asset/sons/marche1.mp3")
sfxmarche2 = pygame.mixer.Sound("asset/sons/marche2.mp3")
sfxmarche3 = pygame.mixer.Sound("asset/sons/marche3.mp3")
# SFX dans l'inventaire
ouvrir_inv = pygame.mixer.Sound("asset/sons/ouvrir_inventaire.mp3")
fermer_inv = pygame.mixer.Sound("asset/sons/fermer_inventaire.mp3")
selectsfx =  pygame.mixer.Sound("asset/sons/selectionner.mp3")
# Le joueur tombe
tombersfx = pygame.mixer.Sound("asset/sons/tomber.mp3")