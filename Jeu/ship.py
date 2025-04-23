import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    """Gerer la fusee"""
    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        #Charger l'image de fusee et obtenir son rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        #Placer chaque nouvelle fusse au centre et en bas
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False
    def update(self):
        """Mettre a jour la positiondu jeu en fonction du moving_right"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def blitme(self):
        """Dessiner la fusee a son emplacement actuel"""
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        """Cetrer la fusee"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)