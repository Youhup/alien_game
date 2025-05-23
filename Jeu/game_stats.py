class GameStats:
    """"Suivre les statistiques du jeu"""
    def __init__(self, ai_game):
        """Initialiser les statistiques du jeu"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        self.high_score = 0
    def reset_stats(self):
        """Intialiser les statistiques qui peuvent changer aucours du jeu"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1