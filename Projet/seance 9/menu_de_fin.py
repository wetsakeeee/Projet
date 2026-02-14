import pygame, sys, subprocess, time
from sfx import musiquefond, sfxboutton


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
police_grande = pygame.font.SysFont(None, 80)
police_petite = pygame.font.SysFont(None, 40)

bouton_rejouer = pygame.Rect(490, 350, 300, 50)
bouton_quitter = pygame.Rect(490, 420, 300, 50)

icon = pygame.image.load("images/logo.png").convert_alpha()
pygame.display.set_icon(icon)
pygame.display.set_caption("Game Over")


background = pygame.image.load("images/image3.jpg").convert() 
background = pygame.transform.scale(background, (1280, 720))

ambiance = musiquefond
ambiance.set_volume(0.4)
ambiance.play(-1)

clic = sfxboutton
clic.set_volume(0.5)

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.blit(background, (0, 0))

    if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_rejouer.collidepoint(event.pos):
                    clic.play()
                    time.sleep(0.3)
                    pygame.quit()
                    subprocess.run([sys.executable, "main.py"])  
                    running = False
                elif bouton_quitter.collidepoint(event.pos):
                    clic.play()
                    time.sleep(0.3)
                    running = False

    texte = police_grande.render("GAME OVER", True, (255, 0, 0))
    screen.blit(texte, (640 - texte.get_width() // 2, 250))

    pygame.draw.rect(screen, (0, 200, 0), bouton_rejouer)
    pygame.draw.rect(screen, (200, 0, 0), bouton_quitter)

    texte_rejouer = police_petite.render("Menu Début", True, (255, 255, 255))
    texte_quitter = police_petite.render("Quitter ", True, (255, 255, 255))

    screen.blit(texte_rejouer, (bouton_rejouer.x + (bouton_rejouer.width - texte_rejouer.get_width()) // 2,
                                    bouton_rejouer.y + (bouton_rejouer.height - texte_rejouer.get_height()) // 2))
    screen.blit(texte_quitter, (bouton_quitter.x + (bouton_quitter.width - texte_quitter.get_width()) // 2,
                                    bouton_quitter.y + (bouton_quitter.height - texte_quitter.get_height()) // 2))

    pygame.display.flip()

pygame.quit()