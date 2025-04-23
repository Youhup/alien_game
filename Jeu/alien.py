import pygame
from pygame.sprite import Sprite
import random
import time
class Alien(Sprite):
    """ Class pour representer les aleins"""
    def __init__(self, ai_game):
        """nitialiser l'alien et definir sa position initiale"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        #Charger l'image de l'alien et defnir sa position initiale
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        self.direction = random.choice([1,-1])

        #Placer chaque nouvel alien pres de l'angle superieur gauche de l'ecran
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        #Stocker la position horizantale exat de l'alien
        self.x = float(self.rect.x)
        #Savoir le temps ecoule depuis la ferniere shoot
        self.bullet_time = random.choice([0.75,1,1.25])
        self.start = time.monotonic()
        self.end = 0

    def check_edges(self):
        """Renvoyer True si l'alien est au bord de l'ecran"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
    def update(self):
        """Deplacer l'alien vers la gauche ou la droite"""
        self.x += (self.settings.alien_speed * self.direction)
        self.rect.x = self.x

