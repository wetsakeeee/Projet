import pygame

class Background:
    def __init__(fond, largeur, hauteur, image_path):
        fond.largeur = largeur
        fond.hauteur = hauteur
        fond.image = pygame.image.load(image_path).convert()
        fond.image = pygame.transform.scale(fond.image, (largeur, hauteur))

        fond.x = 0  # position actuelle de la caméra

    def update(fond, joueur, ecran_width, vitesse=0.1):
        # objectif : centrer la caméra sur le joueur
        camera_target_x = joueur.rect.centerx - ecran_width // 2

        # interpolation pour un mouvement plus doux
        fond.x += (camera_target_x - fond.x) * vitesse

        # limites pour ne pas sortir du niveau
        fond.x = max(0, min(fond.x, fond.largeur - ecran_width))

    def draw(fond, ecran):
        ecran.blit(fond.image, (-fond.x, 0))  # le fond défile

