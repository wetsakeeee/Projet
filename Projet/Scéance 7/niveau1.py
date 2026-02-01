import pygame

def get_plateformes():
    '''Retourne une liste de rectangles représentant les
    plateformes du niveau : (x, y, largeur, hauteur)'''
    return [
        pygame.Rect(400, 5500, 250, 30),
        pygame.Rect(948, 5050, 200, 30),
        pygame.Rect(-100, 6300, 2100, 350),
    ]

