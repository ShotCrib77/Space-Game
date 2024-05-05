# Modules/Libraries
from ship import Ship, Player, Enemy, EnemyManager, Bullet
import pygame as pg
from pygame.locals import *
import os
import random
import time

# Initalizes pygame
pg.font.init()
pg.init()

# ---------
# Constants
# ---------
WIDTH = 800 # Width of screen
HEIGHT = 1000 # Height of screen
SHIP_LOCATION = 250, 750 # Ship width = 140px Ship height = 160px
ENEMY_Y_SPAWN = 0
# Colors

# -----------
# Image loads
# -----------
BG = pg.transform.scale(pg.image.load(os.path.join("Assets", "backgroundSpace.png")), (WIDTH, HEIGHT) )
PLAYER_SHIP = pg.image.load(os.path.join("Assets", "RocketShip.png"))
ENEMY_SHIP = pg.image.load(os.path.join("Assets", "EnemyShip.png"))
BULLET_IMAGE = pg.image.load(os.path.join("Assets", "laser2.png"))

# ------
# Screen
# ------
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Space Game")

def main():
    # ---------
    # Variables
    # ---------
    FPS = 60
    run = True
    health = 10
    
    player = Player(SHIP_LOCATION[0], SHIP_LOCATION[1])
    enemy_manager = EnemyManager(player)
    enemy_manager.create_enemy()
    enemy_manager.create_enemy()
    player_vel = 2

    clock = pg.time.Clock()

    # Updates the window
    # We have redraw inside the main function so that we can access all the variables without using paramiters.
    def redraw_window():
        screen.blit(BG, (0, 0)) # Clears the screen
        # text
        main_font = pg.font.SysFont("comicsans", 30)
        health_label = main_font.render(f"Health: {health}", 1, (255, 0, 0))
        
        player.draw(screen)
        enemy_manager.draw_enemies(screen)
        player.draw_bullets(screen)
        player.update_player()
        screen.blit(health_label, (10, 925))  # Draws out the health_label (temporary??)
        pg.display.update() # Makes all of these updates actually happen


    # Mainloop
    while run:
        # Max Fps - Makes it consistent no matter what system you're using
        clock.tick(FPS)
        redraw_window()
        
        # Breaks out of the while loop if the window gets closed
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                
        # Let's you control the ship horizontally with a and d
        keys = pg.key.get_pressed()
        # left
        if keys[pg.K_a] and player.x - player_vel > 0:
            player.x -= player_vel
        # righta
        if keys[pg.K_d] and player.x + player.ship_img.get_width() + player_vel < WIDTH:
            player.x += player_vel
            
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            # Get the mouse position at the time of click
            click_x, click_y = event.pos
            player.player_shoot(click_x, click_y)
        

        enemy_manager.update_enemies()
        enemy_manager.check_bullet_hits(player.bullets)
            
    # Cleans up and uninitiliazes the pygame library and cleans up it's resources
    pg.quit()
    

if __name__ == "__main__":
    main()
