import pygame
import subprocess
import sys
import sfx
import time

pygame.init()
screen = pygame.display.set_mode((700, 720))
pygame.display.set_caption("Cheat Code")

#-----------ecriture----------------
police = pygame.font.SysFont(None, 36)
sequence_cible = ['[0]', '[8]', '[1]', '[2]']
sequence_actuelle = []

#-----------Background----------------
BG = pygame.image.load("images/hacker.png").convert_alpha()
BG = pygame.transform.scale(BG, (700, 720))

running = True
clock = pygame.time.Clock()

#-------musique--------
pygame.mixer.init()
ambient = sfx.hacker
ambient.set_volume(0.2)
ambient.play(-1)

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            touche = pygame.key.name(event.key)
            sequence_actuelle.append(touche)
            if len(sequence_actuelle) > len(sequence_cible):
                sequence_actuelle.pop(0)

            if sequence_actuelle == sequence_cible:
                print("Code activé ! Lancement de general.py...")
                # On met l'affichage avant le sleep
                screen.blit(BG, (0, 0))
                texte = police.render("Entrez le code : " + ''.join(sequence_actuelle), True, (139, 0, 0))
                screen.blit(texte, (20, 300))
                pygame.display.flip()
                time.sleep(0.4)
                pygame.quit()
                subprocess.run(['python', 'general.py'])
                sys.exit()

    # Affichage
    screen.blit(BG, (0, 0))
    texte = police.render("Entrez le code : " + ''.join(sequence_actuelle), True, (139, 0, 0))
    screen.blit(texte, (20, 300))
    pygame.display.flip()

pygame.quit()
sys.exit()