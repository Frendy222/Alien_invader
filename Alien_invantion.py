
import pygame
from setting import Setting
from SpaceShip import Ship
from Alien import Alien
from scoreboard import Scoreboard
from button import Button
from game_stats import GameStats
import Game_class as gf
from pygame.sprite import Group

def run_game():
    pygame.init()
    setting = Setting()
    screen = pygame.display.set_mode((setting.screen_width,setting.screen_height))
    ship = Ship(setting,screen)
    alien = Alien(setting,screen)
    bullets = Group()
    aliens = Group()

    gf.create_fleet(setting,screen,ship,aliens)


    pygame.display.set_caption('Alien_Invantion')

    stats = GameStats(setting)
    sb = Scoreboard(setting, screen, stats)
    play_button = Button(setting,screen,"Play")

    while True:

        gf.check_event(setting,screen, stats, sb, play_button,ship,aliens,bullets)

        if stats.game_active:
            ship.update()
            bullets.update()
            gf.update_bullets(setting, screen, stats,sb,ship, aliens,bullets)
            gf.update_aliens(setting,stats,screen,sb, ship,aliens,bullets)

        gf.update_screen(setting,screen,stats,sb, ship,bullets,aliens,play_button)


run_game()
