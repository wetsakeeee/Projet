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
        pygame.Rect(100, 6200, 250, 30),
        pygame.Rect(100, 6100, 200, 30),
        pygame.Rect(400, 6000, 200, 30),
        pygame.Rect(600, 5900, 200, 30),
        pygame.Rect(300, 5800, 200, 30),
        pygame.Rect(500, 5700, 100, 30),
        pygame.Rect(750, 5700, 60, 30),
        pygame.Rect(900, 5600, 60, 30),
        pygame.Rect(1050, 5500, 60, 30),
        pygame.Rect(1200, 5370, 60, 30),
        pygame.Rect(1400, 5370, 60, 30),
        pygame.Rect(1500, 5250, 30, 30),
        pygame.Rect(1450, 5150, 20, 30),
        pygame.Rect(1270, 5150, 20, 30),
        pygame.Rect(1100, 5150, 20,30),
        pygame.Rect(800, 5050, 200,40),
    ]

