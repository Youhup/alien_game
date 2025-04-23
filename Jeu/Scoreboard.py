import pygame.font
from pygame.sprite import Group
from ship import Ship
class Scoreboard:
    """Classe pour afficher les informaions du score"""
    def __init__(self,ai_game):
        """Initialiser les attributs de suivi de score"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        #Parametres de police des informations du score
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # Preparer l'image de score nitiale
        self.prep_scores()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
    def prep_ships(self):
        """Afficher le nombre de fusee restantes"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)


    def prep_scores(self):
        """Transformer le score en image"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score).replace(",", " ")
        self.score_image = self.font.render(score_str,True,self.text_color,self.settings.bg_color)
        #Afficher le score en haut a droite de l'ecran
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    def prep_high_score(self):
        """Transformer le high score en image"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score).replace(",", " ")
        self.high_score_image = self.font.render(high_score_str,True,self.text_color,self.settings.bg_color)
        #Centrer le meilleur score en faut de l'ecran
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
    def prep_level(self):
        """Tranformer le niveau en image"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str,True,self.text_color,self.settings.bg_color)
        #Placer le niveau sous le score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 20
        self.level_rect.top = self.score_rect.bottom + 10

    def show_score(self):
        """Affiche le score et le niveau a l'ecran"""
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.ships.draw(self.screen)
    def check_high_score(self):
        """Verifier s'il ya un nouveau hgh score"""
        if self.stats.high_score < self.stats.score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()