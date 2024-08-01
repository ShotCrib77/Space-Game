# Modules/Libraries
from ship import Ship, Player, Enemy, EnemyManager, Bullet
from upgrades import Button, UpgradeMenuManager
import pygame as pg
from pygame.locals import *
import os
import random
import time


pg.font.init()
pg.init()

WIDTH = 800
HEIGHT = 1000
SHIP_LOCATION = 265, 750 # Ship width = 140px Ship height = 160px
ENEMY_Y_SPAWN = 0

# Colors
GREY = "#b9b9b5"
BLACK = "#262626"
WHITE = "#FFFFFF"
RED = "#FF0000"

# Image loads
BG = pg.transform.scale(pg.image.load(os.path.join("Assets", "backgroundSpace.png")), (WIDTH, HEIGHT))
PLAYER_SHIP = pg.image.load(os.path.join("Assets", "RocketShip.png"))
ENEMY_SHIP = pg.image.load(os.path.join("Assets", "EnemyShip.png"))
BULLET_IMAGE = pg.image.load(os.path.join("Assets", "laser2.png"))

# Screen
pg.display.set_caption("Space Game")
screen = pg.display.set_mode((WIDTH, HEIGHT))
main_surface = pg.Surface((WIDTH, HEIGHT))
upgrade_menu_surface = pg.Surface((600, 400))

def surface_scale(surface, scale_factor): # Scales everyhting on the screen (1 being default (normal scale)). A lower or higher scale will result in a blury feel - Used for upgrade menu
    small_size = (int(surface.get_width() * scale_factor), int(surface.get_height() * scale_factor))
    small_surface = pg.transform.smoothscale(surface, small_size)
    blurred_surface = pg.transform.smoothscale(small_surface, (surface.get_width(), surface.get_height()))
    return blurred_surface

def main():
    # Variables and constants
    FPS = 60
    run = True
    global score
    score = 0
    
    player = Player(SHIP_LOCATION[0], SHIP_LOCATION[1])
    enemy_manager = EnemyManager(player)
    player_vel = 2
    enemy_spawn_timer = 5000
    clock = pg.time.Clock()
    main_font = pg.font.SysFont("arial", 30)
    last_enemy_time = pg.time.get_ticks()
    upgrades_menu_manager = UpgradeMenuManager()
    # Updates the window
    # Redraw inside the main function so that we can access all the variables without using paramiters.
    
    def action_button_1():
        print("Button 1 action!")

    def action_button_2():
        print("Button 2 action!")
    
    button_1 = Button((50, 24, 128, 72), "DAMAGE", 100, "1 -> 2", action_button_1)
    button_2 = Button((236, 24, 128, 72), "LASER CD", 100, "2500 -> 2250", action_button_2)
    button_3 = Button((422, 24, 128, 72), "HEAL", 100, "Times Heald: 0")
    
    def redraw_window():
        main_surface.blit(BG, (0, 0))
        player.draw_score(main_surface)
        player.draw(main_surface)
        enemy_manager.draw_enemies(main_surface)
        player.draw_bullets(main_surface)
        player.update_player()
        scaled_surface = surface_scale(main_surface, 1)
        screen.blit(scaled_surface, (0, 0))
        
        upgrades_menu_manager.draw_surface(screen, 100, 200)
        upgrades_menu_manager.draw_buttons()

        pg.display.update() # Makes all of these updates actually happen. 


    while run:
        # Max Fps - Makes it consistent.
        clock.tick(FPS)
        current_time = pg.time.get_ticks()
        redraw_window()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            upgrades_menu_manager.button_interaction(event)    
            
                     
        keys = pg.key.get_pressed()
    
        if keys[pg.K_a] and player.x - player_vel > 0:
            player.x -= player_vel
            
        if keys[pg.K_d] and player.x + player.ship_img.get_width() + player_vel < WIDTH:
            player.x += player_vel
            
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            click_x, click_y = event.pos
            player.player_shoot(click_x, click_y)

        enemy_manager.update_enemies()
        enemy_manager.check_bullet_hits(player.bullets)
        
        if current_time - last_enemy_time >= enemy_spawn_timer:
            enemy_manager.create_enemy()
            last_enemy_time = current_time 
            
    pg.quit()

    
if __name__ == "__main__":
    main()
