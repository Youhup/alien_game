import pygame
from pygame.sprite import Sprite
class AlienBullet(Sprite):
    """classe pour gerer les ballles tires par la fusee"""
    def __init__(self, ai_game,alien):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bomb_color
        # creer une balle alaposition (0,0) puis definir sa position correct
        self.rect = pygame.Rect(0, 0, self.settings.bomb_width, self.settings.bomb_height)
        self.rect.midtop = alien.rect.midbottom
        #stocker la position de la ballse dans une variable deimale
        self.y = float(self.rect.y)
    def update(self):
        """Faire monter la balle a l'ecran"""
        # Mettre a jour la position decimale de la balle
        self.y += self.settings.bullet_speed
        #mettre a jour la postion du rect
        self.rect.y = self.y
    def draw_bullet(self):
        """Dessiner la balle a l'ecran'"""
        pygame.draw.rect(self.screen, self.color, self.rect)