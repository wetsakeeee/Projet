import pygame

def get_plateformes():
    '''Retourne une liste de rectangles représentant les
    plateformes du niveau : (x, y, largeur, hauteur)'''
    return [
        #-------------niveau------------- 
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
        pygame.Rect(0, 4000, 100,40),
        pygame.Rect(1400, 3800, 950,40),
        pygame.Rect(1865, 3600, 100,40),
        pygame.Rect(1865, 3600, 100,40),
        pygame.Rect(1570, 3400, 110,40),
        #------------Bordure-----------
        pygame.Rect(-250, 1000, 255, 10000),
        pygame.Rect(-250, 4875, 500, 40),
       
    ]
def get_plateforme_prison():
    '''Retourne une liste de rectangles représentant les
    plateformes de la prison : (x, y, largeur, hauteur)'''
    return [
        #------------prison-------------
        pygame.Rect(1750, 6000, 20, 770),
        pygame.Rect(1200, 6000, 20, 770),
    ]


def get_plateforme_danger():
    '''Retourne une liste de rectangles représentant les
    plateformes de danger : (x, y, largeur, hauteur)'''
    return[
        pygame.Rect(1220, 6200, 530, 20),
        pygame.Rect(600,  5800, 150, 20),
        pygame.Rect(650,  5050, 150, 95),
        pygame.Rect(935,  4600, 200, 95),
    ]
def get_sol():
    '''Retourne une liste de rectangles représentant le 
    sol du niveau: (x, y, largeur, hauteur)'''
    return [
        pygame.Rect(-100,6300,2100,350)
    ]
def get_mur():
    '''Retourne une liste de rectangles représentant les
    murs du niveau : (x, y, largeur, hauteur)'''
    return[
    pygame.Rect(-70, 3700, 90,700),
    ]
def get_plateformeshaute():
    '''Retourne une liste de rectangles représentant les
    plateformes hautes (murs) : (x, y, largeur, hauteur)'''
    return[
        pygame.Rect(1960,3100,40,800),
        pygame.Rect(1550,2900,40,800)
    ]