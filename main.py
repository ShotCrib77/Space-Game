# Modules
import pygame as pg
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
# Colors

# -----------
# Image loads
# -----------
BG = pg.transform.scale(pg.image.load(os.path.join("Assets", "background_space.png")), (WIDTH, HEIGHT) )
PLAYER_SHIP = pg.image.load(os.path.join("Assets", "Rocket_Ship.png"))

# ------
# Screen
# ------
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Space Game")


# Base Ship class
class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ship_img = None
        self.cool_down_counter = 0
    
    # Drawing ships (takes image and cordinates)
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        
# inherits Ship class
class Player(Ship): 
    def __init__(self, x, y):
        super().__init__(x, y) # Calls the innit method of the Ship class
        self.ship_img = PLAYER_SHIP
        self.mask = pg.mask.from_surface(self.ship_img)

def main():
    # ---------
    # Variables
    # ---------
    FPS = 60
    run = True
    health = 10
    
    player = Player(SHIP_LOCATION[0], SHIP_LOCATION[1])
    player_vel = 2

    clock = pg.time.Clock()
    

    # Updates the window
    # We have redraw inside the main function so that we can access all the variables without using paramiters.
    def redraw_window():
        screen.blit(BG, (0, 0)) # Clears the screen
        # text
        main_font = pg.font.SysFont("comicsans", 30)
        health_label = main_font.render(f"Health: {health}", 1, (255, 0, 0))
        
        player.draw(screen) # draws the player
        
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
        # right
        if keys[pg.K_d] and player.x + player.ship_img.get_width() + player_vel < WIDTH:
            player.x += player_vel
            
    # Cleans up and uninitiliazes the pygame library and cleans up it's resources
    pg.quit()




if __name__ == "__main__":
    main()
