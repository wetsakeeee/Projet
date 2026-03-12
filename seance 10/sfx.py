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