# Modules/Libraries
from ship import Ship, Player, Enemy, EnemyManager, Bullet
from upgrades import Button, UpgradeMenuManager
from astroids import Astroid, AstroidsManager
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
BG = pg.transform.scale(pg.image.load(os.path.join("assets", "background_space.png")), (WIDTH, HEIGHT))
PLAYER_SHIP = pg.image.load(os.path.join("assets", "player", "rocket_ship.png"))
ENEMY_SHIP = pg.image.load(os.path.join("assets", "enemies", "enemy_ship.png"))
BULLET_IMAGE = pg.image.load(os.path.join("assets", "player", "laser2.png"))

MATERIAL_IMAGE_T1 = pg.image.load(os.path.join("assets", "materials", "material_t1.png"))
MATERIAL_IMAGE_T2 = pg.image.load(os.path.join("assets", "materials", "material_t2.png"))
MATERIAL_IMAGE_T3 = pg.image.load(os.path.join("assets", "materials", "material_t3.png"))
MATERIAL_IMAGE_T4 = pg.image.load(os.path.join("assets", "materials", "material_t4.png"))
# Screen 
pg.display.set_caption("Space Game")
screen = pg.display.set_mode((WIDTH, HEIGHT))
main_surface = pg.Surface((WIDTH, HEIGHT))


def main():
    # Variables and constants
    FPS = 60
    run = True
    enemy_spawn_timer = 2500
    astroids_spawn_timer = 10000
    right_mouse_button_down = False
    left_mouse_button_down = False
    moving = False
    player = Player(SHIP_LOCATION[0], SHIP_LOCATION[1], main_surface, 2)
    enemy_manager = EnemyManager(player, main_surface)
    upgrades_menu_manager = UpgradeMenuManager(player)
    astroids_manager = AstroidsManager(main_surface, player, upgrades_menu_manager.upgrade_materials)
    game_loop_manager = GameLoopManager(screen, main_surface, upgrades_menu_manager, enemy_manager)
    clock = pg.time.Clock()
    last_enemy_time = pg.time.get_ticks()
    last_astroid_time = pg.time.get_ticks()
    # Updates window
    def redraw_window():
        main_surface.blit(BG, (0, 0))
        player.draw_ship_info()
        player.draw()
        player.draw_bullets()
        player.update_player()
        astroids_manager.manage_astroids()
        
        if right_mouse_button_down and not upgrades_menu_manager.upgrade_menu_active: # Laser mining beam has to be blited out before main_surface
            player.mining_laser(current_time)
            
            
        enemy_manager.draw_enemies()
    
        screen.blit(main_surface, (0, 0))
        if upgrades_menu_manager.upgrade_menu_active:
            upgrades_menu_manager.redraw_material(MATERIAL_IMAGE_T1, "Metiorite Stone", 130, 275)
            upgrades_menu_manager.redraw_material(MATERIAL_IMAGE_T2, "Malachite", 230, 275)
            upgrades_menu_manager.redraw_material(MATERIAL_IMAGE_T3, "Blue Crystal", 330, 275)
            upgrades_menu_manager.redraw_material(MATERIAL_IMAGE_T4, "Magma Stone", 430, 275)
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
        
       
        moving = player.move(keys, upgrades_menu_manager, player, moving, left_mouse_button_down)
        
        if left_mouse_button_down and not upgrades_menu_manager.upgrade_menu_active and not right_mouse_button_down:
            click_x, click_y = pg.mouse.get_pos()
            player.player_shoot(click_x, click_y)
        
        if right_mouse_button_down and not upgrades_menu_manager.upgrade_menu_active and not left_mouse_button_down: # Laser mining beam has to be blited out before main_surface
            astroids_manager.check_astroids_hit(current_time)
              
        enemy_manager.update_enemies()
        enemy_manager.check_bullet_hits(player.bullets)
        
        if current_time - last_enemy_time >= enemy_spawn_timer and not upgrades_menu_manager.upgrade_menu_active:
            enemy_manager.create_enemy()
            last_enemy_time = current_time
            
        if current_time - last_astroid_time >= astroids_spawn_timer and not upgrades_menu_manager.upgrade_menu_active:
            astroids_manager.spawn_astroid()
            last_astroid_time = current_time
        
        if player.score == upgrades_menu_manager.score_for_next_level:
            upgrades_menu_manager.set_upgrade_menu_active(True)
    
    pg.quit()

    
if __name__ == "__main__":
    main()



