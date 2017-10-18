import sys
from time import sleep
import pygame
from bullet import Bullet
from Alien import Alien

def check_keydown_event(event,setting,screen,ship,bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True

    elif event.key == pygame.K_LEFT:
        ship.moving_left = True

    elif event.key == pygame.K_SPACE:
        fire_bullet(setting,screen,ship,bullets)
    elif event.key == pygame.K_z:
        fire_bullet(setting,screen,ship,bullets)
    elif event.key == pygame.K_x:
        fire_bullet(setting,screen,ship,bullets)


def check_keyup_event(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def fire_bullet(setting,screen,ship,bullets):
    if len(bullets) < setting.bullet_allowed:
            new_bullet = Bullet(setting,screen,ship)
            bullets.add(new_bullet)


def check_event(setting,screen,stats ,sb ,play_button,ship,aliens,bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event,setting,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x , mouse_y = pygame.mouse.get_pos()
            check_play_button(setting, screen, stats, sb, play_button, ship,aliens, bullets, mouse_x, mouse_y)

def check_play_button(setting, screen, stats,sb, play_button, ship, aliens, bullets , mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        setting.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(setting, screen, ship, aliens)
        ship.center_ship()



def update_screen(setting,screen,stats,sb,ship,bullets,aliens,play_button):
    screen.fill(setting.bg_color)
    ship.blitme()
    sb.show_score()
    for bullet in bullets.copy():
        bullet.draw_bullet()
    aliens.draw(screen)



    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()


def update_bullets(setting, screen,stats, sb, ship, aliens,bullets):
    for bullet in bullets.copy():
        if bullet.rect.bottom < - 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(setting,screen,stats, sb, ship,aliens,bullets)

def check_bullet_alien_collisions(setting,screen,stats, sb, ship,aliens,bullets):
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions:
        for alien in collisions.values():
            stats.score += setting.alien_points
            sb.prep_score()
        check_high_score(stats,sb)

    if len(aliens) == 0:
        bullets.empty()
        setting.increase_speed()

        stats.level += 1
        sb.prep_level()

        create_fleet(setting, screen, ship, aliens)


def create_fleet(setting,screen,ship,aliens):
    alien = Alien(setting,screen)
    number_alien_x = get_number_aliens_x(setting, alien.rect.width)
    number_rows = get_number_rows(setting,ship.rect.height,alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_alien_x):
            create_alien(setting,screen,aliens,alien_number,row_number)

def get_number_aliens_x(setting, alien_width):
    available_space_x = setting.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x/(2*alien_width))
    return number_alien_x


def create_alien(setting,screen,aliens,alien_number,row_number):
    alien = Alien(setting,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2  * alien_width * alien_number
    alien.rect.x = alien.x
    alien.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.rect.y = alien.y
    aliens.add(alien)


def get_number_rows(setting,ship_height, alien_height):
    available_space_y = (setting.screen_height - (3* alien_height) - ship_height)
    number_rows = int(available_space_y / (2*alien_height))
    print(number_rows)
    return number_rows

def update_aliens(setting, screen,stats, sb, ship,aliens,bullets):
    check_fleet_edges(setting,aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(setting,screen, stats, sb,ship,aliens,bullets)

    check_aliens_bottom(setting,screen,stats, sb,ship,aliens,bullets)
def check_fleet_edges(setting,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(setting,aliens)
            break

def change_fleet_direction(setting,aliens):
    for alien in aliens.sprites():
        alien.rect.y += setting.fleet_drop_speed
    setting.fleet_direction *= -1

def ship_hit(setting, stats , screen,sb, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1

        sb.prep_ships()
        aliens.empty()
        bullets.empty()

        create_fleet(setting, screen, ship, aliens)
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(setting,stats,screen,sb,ship,aliens,bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(setting,stats,screen,sb,ship,aliens,bullets)
            break

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
