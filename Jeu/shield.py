import pygame
import random
from pygame.sprite import Sprite

class Shield(Sprite):
    """Gerer la boucle"""
    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.ship = ai_game.ship
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        #Charger l'image de fusee et obtenir son rect
        self.image = pygame.image.load('images/shield.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        #Parametre du temps
        self.now = 0
        self.last_time = 0
        self.wait = 10
        #Placer chaque nouvelle boucle au centre et en bas
        self.rect.midtop = self.screen_rect.midtop
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False
        self.image_shield = pygame.image.load('images/Circle_Shield.png').convert_alpha()
        self.image_shield = pygame.transform.scale(self.image_shield, (70, 70))
        self.image_shield.set_alpha(128)
        self.image_shield_rect = self.image_shield.get_rect()
    def update(self):
        if self.rect.y < self.screen_rect.bottom:
            self.rect.y += 1

        if self.settings.Protected:
            self.image_shield_rect.center = self.ship.rect.center
    def blitme(self):
        """Dessiner la fusee a son emplacement actuel"""
        self.screen.blit(self.image,self.rect)
        if self.settings.Protected:
            self.screen.blit(self.image_shield, self.image_shield_rect)
