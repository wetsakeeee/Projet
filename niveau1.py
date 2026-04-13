import pygame, math


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
        pygame.Rect(1910,990,100,40),
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
            pygame.Rect(3100,5920,150,80)



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
        pygame.Rect(3484, 5497, 616, 1004),
        pygame.Rect(2000, 4000, 546, 2133),
    ]
def plateforme_2():
    return [
        pygame.Rect(3000, 6350, 110,40),
        pygame.Rect(3100, 6000, 400,160),
        pygame.Rect(2750, 6180, 110,40),
        pygame.Rect(3100, 5497, 400,160),
        pygame.Rect(2800, 5850, 110,40),
        pygame.Rect(2540, 5250, 110,40),
        pygame.Rect(2740, 5050, 110,40),
        pygame.Rect(2840, 4050, 110,40),
    ]
def get_bateau(): # Plateformes du bateau au niveau 2
    return [
        # bateau
        pygame.Rect(50,760,300,130),
        # limite du bateau
        pygame.Rect(30,430,50,350),
        pygame.Rect(330,430,50,450),
        pygame.Rect(50,230,300,130),
        # sol du monstre
        pygame.Rect(350,800,2000,20),
        # Plafond
        pygame.Rect(0,220,2000,10),
        ]
def caronte_niveau2():
    return [
    pygame.Rect(60,700,200,600),
        ]

def get_niveau2(): # Plateforme du niveau 2 pour réparer le bateau de Caronte

    return [
        pygame.Rect(430,760,300,130),
        pygame.Rect(800,500,300,130),
        pygame.Rect(1300,600,300,130),
        pygame.Rect(1800,750,300,130),
        pygame.Rect(2500,800,500,130),

            ]
class MovingPlatform:
    def __init__(self, x, y, width, height, dy_amplitude=0, dx_amplitude=0, y_min=None, y_max=None, x_min=None, x_max=None, speed=0.02, phase=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.origin_x = float(x)
        self.origin_y = float(y)
        self.dy_amplitude = dy_amplitude  # distance max parcourue verticalement
        self.dx_amplitude = dx_amplitude  # distance max parcourue horizontalement
        self.speed = speed                # vitesse de l'oscillation (plus petit = plus lent)
        self.t = phase  # démarre à un angle différent         

    def update(self):
        self.t += self.speed
        # math.sin va de -1 à 1 en douceur → accélère au milieu, ralentit aux extrémités
        self.rect.y = int(self.origin_y + math.sin(self.t) * self.dy_amplitude)
        self.rect.x = int(self.origin_x + math.sin(self.t) * self.dx_amplitude)

def get_plateformes_mobiles():
    return [
        MovingPlatform(2940, 4900, 110, 40, dy_amplitude=100, speed=0.04),
        MovingPlatform(2940, 4600, 110, 40, dx_amplitude=100, dy_amplitude=0, speed=0.04),
        MovingPlatform(3470, 4600, 110, 40, dx_amplitude=100, dy_amplitude=0, speed=0.04, phase=math.pi),
        MovingPlatform(3700, 4400, 110, 40, dy_amplitude=200, speed=0.06),
    ]
