import pygame
import random
from pygame.sprite import Sprite

class Life(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.ship = ai_game.ship
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        #Charger l'image de fusee et obtenir son rect
        self.image = pygame.image.load('images/ship.bmp')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        #Parametre du temps
        self.now = 0
        self.last_time = 0
        self.wait = 15
        #Placer chaque nouvelle boucle au centre et en bas
        self.rect.midtop = self.screen_rect.midtop
        self.x = float(self.rect.x)
    def update(self):
        if self.rect.y < self.screen_rect.bottom:
            self.rect.y += 1
    def blitme(self):
        """Dessiner la fusee a son emplacement actuel"""
        self.screen.blit(self.image,self.rect)
