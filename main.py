# Modules/Libraries
from ship import Ship, Player, Enemy, EnemyManager, Bullet
from upgrades import Button, UpgradeMenuManager
from gameloop import GameLoopManager
import pygame as pg
from pygame.locals import *
import os
import random
import time


pg.font.init()
pg.init()

# Constants
WIDTH = 800
HEIGHT = 1000
SHIP_LOCATION = 260, 750 # Ship width = 140px Ship height = 160px
ENEMY_Y_SPAWN = 0

# Image loads
BG = pg.transform.scale(pg.image.load(os.path.join("Assets", "backgroundSpace.png")), (WIDTH, HEIGHT))
PLAYER_SHIP = pg.image.load(os.path.join("Assets", "RocketShip.png"))
ENEMY_SHIP = pg.image.load(os.path.join("Assets", "EnemyShip.png"))
BULLET_IMAGE = pg.image.load(os.path.join("Assets", "laser2.png"))

# Screen
pg.display.set_caption("Space Game")
screen = pg.display.set_mode((WIDTH, HEIGHT))
main_surface = pg.Surface((WIDTH, HEIGHT))



def main():
    # Variables and constants
    FPS = 60
    run = True
    player_vel = 2
    enemy_spawn_timer = 500
    
    player = Player(SHIP_LOCATION[0], SHIP_LOCATION[1], main_surface)
    enemy_manager = EnemyManager(player, main_surface)
    upgrades_menu_manager = UpgradeMenuManager(player)
    game_loop_manager = GameLoopManager(screen, main_surface, upgrades_menu_manager, enemy_manager)
    clock = pg.time.Clock()
    last_enemy_time = pg.time.get_ticks()
    
    # Updates window
    def redraw_window():
        main_surface.blit(BG, (0, 0))
        player.draw_ship_info()
        player.draw()
        enemy_manager.draw_enemies()
        player.draw_bullets()
        player.update_player()
        screen.blit(main_surface, (0, 0))
        if upgrades_menu_manager.upgrade_menu_active:
            game_loop_manager.draw_upgrades()
        pg.display.update() # Makes all of these updates actually happen.


    while run:
        # Max Fps - Makes it consistent.
        clock.tick(FPS)
        current_time = pg.time.get_ticks()
        redraw_window()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            
            if upgrades_menu_manager.upgrade_menu_active: 
                upgrades_menu_manager.button_interaction(event)

                     
        keys = pg.key.get_pressed()
    
        if keys[pg.K_a] and player.x - player_vel > 0 and not upgrades_menu_manager.upgrade_menu_active:
            player.x -= player_vel
            
        if keys[pg.K_d] and player.x + player.ship_img.get_width() + player_vel < WIDTH and not upgrades_menu_manager.upgrade_menu_active:
            player.x += player_vel
            
        if event.type == MOUSEBUTTONDOWN and event.button == 1 and not upgrades_menu_manager.upgrade_menu_active:
            click_x, click_y = event.pos
            player.player_shoot(click_x, click_y)

        enemy_manager.update_enemies()
        enemy_manager.check_bullet_hits(player.bullets)
        
        if current_time - last_enemy_time >= enemy_spawn_timer and not upgrades_menu_manager.upgrade_menu_active:
            enemy_manager.create_enemy()
            last_enemy_time = current_time 
            
        if player.score == upgrades_menu_manager.score_for_next_level:
            upgrades_menu_manager.set_upgrade_menu_active(True)
            
    pg.quit()

    
if __name__ == "__main__":
    main()
