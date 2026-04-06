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
        pygame.Rect(1270, 5150, 100, 40),
        pygame.Rect(1100, 5150, 100,40),
        pygame.Rect(800, 5050, 200,40),
        pygame.Rect(450, 5050, 200,40),
        pygame.Rect(450, 4700, 200,40),
        pygame.Rect(900, 4800, 200,40),
        pygame.Rect(1300, 4600, 200,40),
        pygame.Rect(1300, 4400, 200,40),
        pygame.Rect(1300, 4200, 200,40),
        pygame.Rect(-250, 4200, 1270,200),
        pygame.Rect(500, 3800, 950,40),
        pygame.Rect(0, 4000, 100,40),
        pygame.Rect(1400, 3800, 950,40),
        pygame.Rect(1570, 3400, 110,40),
        pygame.Rect(1865, 3000, 110,40),
        pygame.Rect(1865, 2650, 110,40),
        pygame.Rect(1570, 2650, 110,40),
        pygame.Rect(1700,2460,300,40),
        pygame.Rect(1865,2100,200,40),
        pygame.Rect(1700,1800,100,40),
        pygame.Rect(1875,1400,100,40),
        pygame.Rect(285, 840, 1270,200),
        pygame.Rect(1910,980,100,40),
        pygame.Rect(-5, 1300, 500,40),




        
        #------------Bordure-----------
        pygame.Rect(-260, 200, 255, 10000),
        pygame.Rect(-250, 4875, 500, 40),
        pygame.Rect(2000,-700,40,4500),
        pygame.Rect(2000,2200,40,4500),
       
    ]
def get_plateforme_prison():
    '''Retourne une liste de rectangles représentant les
    plateformes de la prison : (x, y, largeur, hauteur)'''
    return [
        #------------prison-------------
        pygame.Rect(1750, 6000, 20, 770),
        pygame.Rect(1200, 6000, 20, 770),
    ]


def plateforme_pic():
    '''Retourne une liste de rectangles représentant les
    plateformes de danger de pic'''
    return[
        pygame.Rect(1220, 6150, 530, 20),
        pygame.Rect(1865, 2690, 110,40),
        pygame.Rect(1570, 2690, 110,40),
        pygame.Rect(900,  4400, 200, 200),
    ]
def plateforme_pic2():
    return [
            pygame.Rect(600,  5660, 150, 80),
            pygame.Rect(650,  5000, 150, 95),
            pygame.Rect(1700, 2380, 150,80),



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
        pygame.Rect(1960,1020,40,2800),
        pygame.Rect(1535,860,40,2800)
    ]
def get_sol2():
    return [
        pygame.Rect(1680, 6500, 2420, 400)
    ]
def mur2():
    return [
        pygame.Rect(3484, 5497, 616, 1004)
    ]
def plateforme_2():
    return [
        pygame.Rect(3000, 6350, 110,40),
        pygame.Rect(3100, 6000, 400,160),
        pygame.Rect(2750, 6180, 110,40),
        pygame.Rect(3100, 5497, 400,160),
        pygame.Rect(2800, 5850, 110,40),
    ]
