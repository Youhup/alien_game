import sys
import pygame
import time
import random
from Life import Life

from  Settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from Scoreboard import Scoreboard
from Alien_bullet import AlienBullet
from shield import Shield
from Life import Life
class AlienInvasion:
    """Classe global pour gerer le jeu"""
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')
        # Crrer une instance de stockage des statstques du jeu
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self,"Jouer")
        self.shield = Shield(self)
        self.alien_bullets = pygame.sprite.Group()
        self.tir_sound =  pygame.mixer.Sound('Sounds/Tir.wav')
        self.explosion_ship_sound = pygame.mixer.Sound('Sounds/Explosion_ship.wav')
        self.explosion_alien_sound = pygame.mixer.Sound('Sounds/explosion_alien.wav')
        self.end_game = pygame.mixer.Sound('Sounds/End_game.wav')
        self.life = Life(self)





    def run_game(self):
        """LA boucle principale du jeu"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self.Give_Shield()
                self.Give_life()
            self._update_screen()

    def _check_events(self):
        """Repondre aus evenements de la souris et le clavier"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                  
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                button_clicked = self.play_button.rect.collidepoint(mouse_pos)
                self._check_play_button(button_clicked)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    def _check_play_button(self, button_clicked):
        """Commence un enouvelle partie quand lejoueur appui sur Jouer"""

        if button_clicked and not self.stats.game_active:
            #Reinitialiser les statistiques du jeu
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_scores()
            self.sb.prep_level()
            self.sb.prep_ships()
            #Supprimer les balles et les liens restants
            self.aliens.empty()
            self.bullets.empty()
            self.alien_bullets.empty()
            #Creer une autre armee et centrer la fusee
            self._create_fleet()
            self.ship.center_ship()
            #MAsquer le curser de la souris
            pygame.mouse.set_visible(False)
            #Cacher la boucle et la vie
            self.shield.rect.top = self.screen.get_rect().bottom
            self.life.rect.top = self.screen.get_rect().bottom



    def _check_keydown_events(self,event):
        """Repondre aux touches enfonces"""
        if event.key == pygame.K_RIGHT:
            # Deplacer la fusee cers la droie
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
              
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_j:
            self._check_play_button(True)
    def _check_keyup_events(self,event):
        """Repondre aux touches relaches"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    def _fire_bullet(self):
        """Creer une balle et l'ajouter a la liste des balles"""
        if len(self.bullets) < self.settings.bullets_allowed:
            self.tir_sound.play()
            new_ballet = Bullet(self)
            self.bullets.add(new_ballet)
    def _update_bullets(self):
        """Mettre a jour la position de l'ecran et supprimer les anciens"""
        self.bullets.update()
        self.alien_bullets.update()
        # supprimer des balles qui ont disparu
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                bullet.kill()
        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        """Repondre au collisins entre balles-aliens"""
        # rechercher si une balle a touche un alien, si oui supprimer les deux
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for alien in collisions.values():
                self.explosion_alien_sound.play()
                self.stats.score += self.settings.alien_points * len(alien)
            self.sb.prep_scores()
            self.sb.check_high_score()
        if not self.aliens:
            # Detruire les balles existants et creer une autre armee
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            #Accrementer le niveau et le transforme en image pour etreaffiché
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """Mettre a jour la position de l'arme des aliens"""
        self._check_fleet_edges()
        self.aliens.update()
        self.alien_attack()
        #Recherchr les collisins entre l'alien et la fusee
        if pygame.sprite.spritecollideany(self.ship, self.aliens ):
            self._ship_hit()
        self._check_aliens_bottom()
    def _ship_hit(self ):
        """Repondre a la percussion de la fusee avec un alien"""
        if self.stats.ships_left > 0:
            self.explosion_ship_sound.play()
            self.stats.ships_left -=1
            self.sb.prep_ships()
            #Supprimer les aliens et les balles
            self.aliens.empty()
            self.bullets.empty()
            self.alien_bullets.empty()
            #Creer une autre armée et centrer la fuséé
            self._create_fleet()
            self.ship.center_ship()
            #Faire une pause
            time.sleep(0.5)
        else:
            self.stats.game_active = False
            self.end_game.play()
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Verifier si des aliens ont atteint le bas de l'ecran"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens:
            if alien.rect.bottom >= screen_rect.bottom:
                #Traiter ce cas commen si un alien a percuté la fusée
                self._ship_hit()
                break

    def _create_fleet(self):
        """Creer l'arme d'alien"""
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        alien.kill()

        for number_alien in range(random.choice([3,4,5])):
            self._create_alien(number_alien)

    def _create_alien(self,number_alien):
        """Creer un alien et le placer sur la ligne"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width * (2 + 4 * number_alien)
        alien.y = alien_height * (1 + 2 * number_alien)
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)
    def _check_fleet_edges(self):
        """Repondr correctement si des aliens ont atteint les bords"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_alien_direction(alien)

    def _change_alien_direction(self,alien):
        """Faire descendre l'alien d'un cran et inverser son sens de deplacement"""
        alien.rect.y += self.settings.fleet_drop_speed
        alien.direction *= -1
    def alien_attack(self):
        self.activate_shied()
        for alien in self.aliens.sprites():
            alien.end = time.monotonic()
            if alien.end - alien.start > alien.bullet_time:
                self._alien_fire(alien)
                alien.start = time.monotonic()
                alien.bullet_time = random.uniform(0, self.settings.bomb_interval)
        self._check_bomb_ship()

    def _alien_fire(self,alien):
        bullet = AlienBullet(self,alien)
        self.alien_bullets.add(bullet)
    def _check_bomb_ship(self):
        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets) :
            if not self.settings.Protected:
                self._ship_hit()
            else :
                self.settings.Protected = False
                self.alien_bullets.empty()
                self.shield.last_time = time.monotonic()

    def Give_Shield(self):
        self.shield.now = time.monotonic()
        if self.shield.last_time == 0:
            self.shield.last_time = time.monotonic()
        if self.shield.now - self.shield.last_time > self.shield.wait and not self.settings.Protected:
            self.shield.rect.x = random.uniform(0,self.settings.screen_width)
            self.shield.rect.y = 0
            self.shield.wait = random.choice([10,15,20])
            self.shield.last_time = time.monotonic()
        self.shield.update()

    def activate_shied(self):
        if self.ship.rect.colliderect(self.shield.rect):
            self.settings.Protected = True
            self.shield.rect.top = self.screen.get_rect().bottom
    def Give_life(self):
        self.life.now = time.monotonic()
        if self.life.last_time == 0:
            self.life.last_time = time.monotonic()
        if self.life.now - self.life.last_time > self.life.wait:
            self.life.rect.x = random.uniform(0, self.settings.screen_width)
            self.life.rect.y = 0
            self.life.wait = random.choice([15,20,25])
            self.life.last_time = time.monotonic()
        self.life.update()
        if self.ship.rect.colliderect(self.life.rect):
            self.stats.ships_left +=1
            self.sb.prep_ships()
            self.life.rect.top = self.screen.get_rect().bottom



    def _update_screen(self):
        """Mettre a jour l'ecran"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets:
            bullet.draw_bullet()
        for bullet in self.alien_bullets:
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.shield.blitme()
        self.life.blitme()
        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
