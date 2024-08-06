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
MINING_LASER_IMAGE_FRAME_1 = pg.image.load(os.path.join("Assets", "mining_laser_v6_frame_1.png"))
MINING_LASER_IMAGE_FRAME_2 = pg.image.load(os.path.join("Assets", "mining_laser_v6_frame_2.png"))
MINING_LASER_IMAGE_FRAME_3 = pg.image.load(os.path.join("Assets", "mining_laser_v6_frame_3.png"))
MINING_LASER_IMAGE_FRAME_4 = pg.image.load(os.path.join("Assets", "mining_laser_v6_frame_4.png"))
MINING_LASER_IMAGE_FRAME_5 = pg.image.load(os.path.join("Assets", "mining_laser_v6_frame_5.png"))
# Screen
pg.display.set_caption("Space Game")
screen = pg.display.set_mode((WIDTH, HEIGHT))
main_surface = pg.Surface((WIDTH, HEIGHT))


def main():
    # Variables and constants
    FPS = 60
    run = True
    enemy_spawn_timer = 500
    right_mouse_button_down = False
    left_mouse_button_down = False
    player = Player(SHIP_LOCATION[0], SHIP_LOCATION[1], main_surface, 2)
    enemy_manager = EnemyManager(player, main_surface)
    upgrades_menu_manager = UpgradeMenuManager(player)
    game_loop_manager = GameLoopManager(screen, main_surface, upgrades_menu_manager, enemy_manager)
    clock = pg.time.Clock()
    last_enemy_time = pg.time.get_ticks()
    tick_count = 0
    
    # Updates window
    def redraw_window():
        main_surface.blit(BG, (0, 0))
        player.draw_ship_info()
        player.draw()
        player.draw_bullets()
        player.update_player()
                
        if right_mouse_button_down and not upgrades_menu_manager.upgrade_menu_active: # Laser mining beam has to be blited out before main_surface
            player.mining_laser(current_time)
        
        enemy_manager.draw_enemies()
    
        screen.blit(main_surface, (0, 0))
        if upgrades_menu_manager.upgrade_menu_active:
            game_loop_manager.draw_upgrades()
        pg.display.update() # Makes all of these updates actually happen.

    while run:
        # Max Fps - Makes it consistent.
        clock.tick(FPS)
        current_time = pg.time.get_ticks()
        redraw_window()
        keys = pg.key.get_pressed()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            
            if upgrades_menu_manager.upgrade_menu_active: 
                upgrades_menu_manager.button_interaction(event)
            
            # Let's the user hold lef/right mousebutton instead of having to spam it.
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                right_mouse_button_down = True
            if event.type == pg.MOUSEBUTTONUP and event.button == 3:
                right_mouse_button_down = False
                
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                left_mouse_button_down = True
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                left_mouse_button_down = False
                     
       
        player.move(keys, upgrades_menu_manager, player)
            
        if left_mouse_button_down and not upgrades_menu_manager.upgrade_menu_active:
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
