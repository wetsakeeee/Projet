import pygame

def get_plateformes():
    '''Retourne une liste de rectangles représentant les
    plateformes du niveau : (x, y, largeur, hauteur)'''
    return [
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
        pygame.Rect(450, 5050, 200,40),
        pygame.Rect(450, 4700, 200,40),
        pygame.Rect(950, 4800, 200,40),
        pygame.Rect(1300, 4600, 200,40),
        pygame.Rect(1300, 4400, 200,40),
        pygame.Rect(1300, 4200, 200,40),
        pygame.Rect(-250, 4200, 1270,200),
        pygame.Rect(500, 3800, 950,40),

       
        #------------Bordure-----------
        pygame.Rect(-250, 1000, 200, 10000),
        pygame.Rect(-250, 4875, 500, 40),
       
    ]
def get_plateforme_prison():
    return [
        #------------prison-------------
        pygame.Rect(1750, 6000, 20, 770),
        pygame.Rect(1200, 6000, 20, 770),
    ]

def get_plateforme_danger():
    return[
        pygame.Rect(1275,6200,530,20),
        pygame.Rect(655,5800,150,20),
        pygame.Rect(705,5050,150,95),
        pygame.Rect(970, 4600,200,95),
    ]
def get_sol():
    return [
        pygame.Rect(-100,6300,2100,350)
    ]
def get_mur():
    return[
    pygame.Rect(-70, 3700, 90,700),
    ]
