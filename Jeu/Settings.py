class Settings:
    """Stocker les parametre su jeu"""
    def __init__(self):
        #Parametres de l'ecran
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (230, 230, 230)
        #Parametres de la fusee

        self.ship_limit = 2
        # parametres des balles

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3
        #Parametres ds bombes
        self.bomb_width = 15
        self.bomb_height = 15
        self.bomb_color = 200, 60, 60

        #Parametres de l'alien

        self.fleet_drop_speed = 10

        #Rythme d'acceleration du jeu
        self.speedup_scale = 1.1
        #Rapidite de l'augmentation de la valeur des points
        self.score_scale = 1.5

        self.initialize_dynamic_settings()
    def initialize_dynamic_settings(self):
        """Initaliser le parametre sui changent au cours de la partie"""
        self.ship_speed = 1.5
        self.bullet_speed = 3
        self.alien_speed = 1
        self.alien_points = 50
        self.bomb_interval = 1.5
        # fleet_direction = 1 pour la droite et -1 pour le gauche
        self.fleet_direction = 1
        self.Protected = False

    def increase_speed(self):
        """Augmenter les parametre de la vitesse"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        self.bomb_interval /= self.speedup_scale



