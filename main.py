# Modules/Libraries
from ship import Ship, Player, Enemy, EnemyManager, Bullet
import pygame as pg
from pygame.locals import *
import os
import random
import time


pg.font.init()
pg.init()

WIDTH = 800
HEIGHT = 1000
SHIP_LOCATION = 250, 750 # Ship width = 140px Ship height = 160px
ENEMY_Y_SPAWN = 0

# Image loads
BG = pg.transform.scale(pg.image.load(os.path.join("Assets", "backgroundSpace.png")), (WIDTH, HEIGHT) )
PLAYER_SHIP = pg.image.load(os.path.join("Assets", "RocketShip.png"))
ENEMY_SHIP = pg.image.load(os.path.join("Assets", "EnemyShip.png"))
BULLET_IMAGE = pg.image.load(os.path.join("Assets", "laser2.png"))

# Screen
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Space Game")

def main():
    # ---------
    # Variables
    # ---------
    FPS = 60
    run = True
    global score
    score = 0
    
    player = Player(SHIP_LOCATION[0], SHIP_LOCATION[1])
    enemy_manager = EnemyManager(player)
    player_vel = 2
    enemy_spawn_timer = 5000
    clock = pg.time.Clock()
    last_enemy_time = pg.time.get_ticks()
    # Updates the window
    # Redraw inside the main function so that we can access all the variables without using paramiters.
    def redraw_window():
        screen.blit(BG, (0, 0)) # Clears the screen
        main_font = pg.font.SysFont("arial", 30)
        player.draw_score(screen)
        player.draw(screen)
        enemy_manager.draw_enemies(screen)
        player.draw_bullets(screen)
        player.update_player()
        pg.display.update() # Makes all of these updates actually happen.


    while run:
        # Max Fps - Makes it consistent.
        clock.tick(FPS)
        current_time = pg.time.get_ticks()
        redraw_window()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                
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
