import pygame
import sys
import subprocess
from pygame.display import flip
pygame.init()
width , height = 1280 , 720
screen = pygame.display.set_mode((width,height))
BG = pygame.image.load("galaxy-1.jpg").convert_alpha()
BG = pygame.transform.scale(BG, (1280, 720))
pygame.display.set_caption("SAGGIO BREVE")
pygame.display.set_caption("Jouer")
#couleurs
Blanc = (255,255,255)
bleu_transparent = (0,80,200,180)
bleu_selection = (0,140,255,220)
shadow = (0,0,0)
#polices d'écritures
try :   
    Police_titre = pygame.font.Font("Coolvetica Rg.otf", 72)
    Police_bouton =  pygame.font.Font("Coolvetica Rg.otf", 36)

except :
    Police_titre = pygame.font.SysFont(None, 72)
    Police_bouton =  pygame.font.SysFont(None, 36)

class Button :
    def __init__(self,text,center_y,action):
        self.text = text
        self.action = action
        self.center_y = center_y
        self.widht, self.height = 320,70
        self.rect = pygame.rect((0,0,self.widht,self.height))
        self.rect.center = (width//2 , center_y)
    def draw(self, win, mouse_pos)   

  





running = True
while running:
    screen.fill((0,0,0))
    screen.blit(BG,(0,0))
    pygame.display.flip()

    
    
    
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()
    
    
POS_SOURIS = pygame.mouse.get_pos
