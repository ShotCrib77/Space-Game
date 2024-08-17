# Modules/Libraries
from ship import Player, EnemyManager
from upgrades import UpgradeMenuManager
from astroids import AstroidsManager
from gameloop import GameLoopManager
from upgrades_cards import UpgradesMenu
import pygame as pg
from pygame.locals import *
import os
import random

# Initializes pygame
pg.font.init()
pg.init()

# Constants
WIDTH = 800
HEIGHT = 1000
SHIP_LOCATION = 260, 750 # Ship width = 140px Ship height = 160px

# Image loads
BG = pg.transform.scale(pg.image.load(os.path.join("assets", "background_space.png")), (WIDTH, HEIGHT))
PLAYER_SHIP_ICON = pg.image.load(os.path.join("assets", "player", "rocket_ship.png"))

ENEMY_SHIP_IMAGE_NORMAL = pg.image.load(os.path.join("assets", "enemies", "enemy_ship_normal.png"))
ENEMY_SHIP_IMAGE_SMALL = pg.image.load(os.path.join("assets", "enemies", "enemy_ship_small.png"))
ENEMY_SHIP_IMAGE_TANK = pg.image.load(os.path.join("assets", "enemies", "enemy_ship_tank.png"))
ENEMY_SHIP_IMAGE_BOSS = pg.image.load(os.path.join("assets", "enemies", "enemy_ship_boss.png"))

UPGRADE_CARD_IMAGE_T1 = pg.image.load(os.path.join("assets", "upgrade_cards", "upgrade_card_t1.png")) # 200 x 281
UPGRADE_CARD_IMAGE_T2 = pg.image.load(os.path.join("assets", "upgrade_cards", "upgrade_card_t2.png")) # 215 x 300
UPGRADE_CARD_IMAGE_T3 = pg.image.load(os.path.join("assets", "upgrade_cards", "upgrade_card_t3.png")) # 222 x 300
UPGRADE_CARD_IMAGE_T4 = pg.image.load(os.path.join("assets", "upgrade_cards", "upgrade_card_t4.png")) # 200 x 300
UPGRADE_CARD_IMAGE_T5 = pg.image.load(os.path.join("assets", "upgrade_cards", "upgrade_card_t5.png")) # 188 x 300

# Screen 
pg.display.set_caption("Space Game")
pg.display.set_icon(PLAYER_SHIP_ICON)
screen = pg.display.set_mode((WIDTH, HEIGHT))
main_surface = pg.Surface((WIDTH, HEIGHT))


def main():
    # Variables and constants
    FPS = 60
    run = True
    enemy_spawn_timer = 3000
    astroids_spawn_timer = 10000
    right_mouse_button_down = False
    left_mouse_button_down = False
    moving = False
    player = Player(SHIP_LOCATION[0], SHIP_LOCATION[1], main_surface, 2)
    upgrades_menu_manager = UpgradeMenuManager(player)
    upgrades_menu = UpgradesMenu(screen, player)
    enemy_manager = EnemyManager(player, main_surface, upgrades_menu)
    astroids_manager = AstroidsManager(main_surface, player, upgrades_menu_manager.upgrade_materials)
    game_loop_manager = GameLoopManager(screen, main_surface, upgrades_menu_manager, enemy_manager, astroids_manager, upgrades_menu)

    upgrades_menu.import_enemy_manager(enemy_manager)
    
    clock = pg.time.Clock()
    last_enemy_time = pg.time.get_ticks()
    last_astroid_time = pg.time.get_ticks()
    enemy_types = [1, 2, 3]  # 1: Normal Enemy, 2: Small Enemy, 3: Tank Enemy
    weights = [11, 3, 1]  # Frequency of what enemy gets spawned: 5 for Normal, 2 for Small, 1 for Tank

    # Updates window
    def redraw_window():
        main_surface.blit(BG, (0, 0))
        player.draw_ship_info()
        player.draw()
        player.draw_bullets()
        player.update_player()
        astroids_manager.manage_astroids()
        if right_mouse_button_down and not upgrades_menu.menu_active and not game_loop_manager.game_over_active: # Laser mining beam has to be blited out before main_surface
            player.mining_laser(current_time)
            print(upgrades_menu.upgrade_cards_manager.cards)
            
        enemy_manager.draw_enemies()

        screen.blit(main_surface, (0, 0))
        if upgrades_menu.menu_active:
            game_loop_manager.draw_upgrades2()
        
        if player.health == 0:
            game_loop_manager.game_over()
            
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
            
            if upgrades_menu.menu_active: 
                #upgrades_menu_manager.button_interaction(event)
                upgrades_menu.menu_functions(event)
            
            # Let's the user hold lef/right mousebutton instead of having to spam it.
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                right_mouse_button_down = True
            if event.type == pg.MOUSEBUTTONUP and event.button == 3:
                right_mouse_button_down = False
                
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                left_mouse_button_down = True
                
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                left_mouse_button_down = False
        
       
        moving = player.move(keys, upgrades_menu, player, moving, left_mouse_button_down)
        
        if left_mouse_button_down and not upgrades_menu.menu_active and not right_mouse_button_down and not game_loop_manager.game_over_active:
            click_x, click_y = pg.mouse.get_pos()
            player.player_shoot(click_x, click_y)
        
        if right_mouse_button_down and not upgrades_menu.menu_active and not left_mouse_button_down and not game_loop_manager.game_over_active: # Laser mining beam has to be blited out before main_surface
            astroids_manager.check_astroids_hit(current_time)
              
        enemy_manager.update_enemies()
        enemy_manager.check_bullet_hits(player.bullets)
        
        if current_time - last_enemy_time >= enemy_spawn_timer and not upgrades_menu.menu_active and not game_loop_manager.game_over_active:
            if player.score >= upgrades_menu_manager.score_for_next_level and not enemy_manager.active:
                enemy_manager.create_enemy(4)
                enemy_manager.boss_active(True)
            else:
                chosen_enemy = random.choices(enemy_types, weights=weights, k=1)[0]
                enemy_manager.create_enemy(chosen_enemy)
            last_enemy_time = current_time
            
        if current_time - last_astroid_time >= astroids_spawn_timer and not upgrades_menu.menu_active and not game_loop_manager.game_over_active:
            astroids_manager.spawn_astroid()
            last_astroid_time = current_time
        
        if player.health <= 0:
            game_loop_manager.set_game_over_active(True)
        
            
    
    pg.quit()

    
if __name__ == "__main__":
    main()