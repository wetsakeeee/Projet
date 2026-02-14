import pygame

def get_plateformes():
    '''Retourne une liste de rectangles représentant les
    plateformes du niveau : (x, y, largeur, hauteur)'''
    return [
         #------------Prison-------------
        pygame.Rect(1750, 6000, 20,770),
        pygame.Rect(1200, 6000, 20,770),
        #-------------niveau------------- 
        pygame.Rect(-100, 6300, 2100, 350),
        pygame.Rect(300, 6200, 400, 80),
        pygame.Rect(370, 6000, 200, 40),
        pygame.Rect(600, 5900, 200, 40),
        pygame.Rect(300, 5850, 200, 40),
        pygame.Rect(500, 5700, 100, 40),
        pygame.Rect(750, 5700, 100, 40),
        pygame.Rect(900, 5600, 100, 40),
        pygame.Rect(1050, 5500, 100, 40),
        pygame.Rect(1200, 5370, 100, 40),
        pygame.Rect(1400, 5370, 100, 40),
        pygame.Rect(1500, 5250, 100, 40),
        pygame.Rect(1450, 5150, 100, 40),
        pygame.Rect(1270, 5150, 100, 40),
        pygame.Rect(1100, 5150, 100,40),
        pygame.Rect(800, 5050, 200,40),
        #------------Bordure-----------
        pygame.Rect(-250, 4000, 200, 4000),
    ]


def get_plateforme_danger():
    return[
        pygame.Rect(1275,6280,530,20),
        pygame.Rect(655,5800,150,20),

    ]