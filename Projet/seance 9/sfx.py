import pygame
# --------------------------------------------
# Fichier pour gérer tout les sons du programme
# --------------------------------------------
pygame.mixer.init()
musiquefond = pygame.mixer.Sound("asset/sons/music_enfer.mp3")
sauter = pygame.mixer.Sound("asset/sons/jump.mp3")
musiquemenu = pygame.mixer.Sound("asset/sons/menu.mp3")
sfxboutton = pygame.mixer.Sound("asset/sons/bouton.mp3")
degat = pygame.mixer.Sound("asset/sons/sfxdegat.mp3")
sfxdialogue = pygame.mixer.Sound("asset/sons/dialogue.mp3")
