# Modules
import pygame as pg
import os
import random

# Initalizes pygame
pg.init()

# ---------
# Constants
# ---------
WIDTH = 800
HEIGHT = 1000
SHIP_LOCATION = 250, 750 # Ship width = 140px Ship height = 160px
# Colors
BLACK = (0, 0, 0)

BG = pg.image.load(os.path.join("Assets", "Space_Background.png"))
SHIP = pg.image.load(os.path.join("Assets", "Rocket_Ship.png"))

# ------
# Screen
# ------
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Space Game")


def main():
    # Variables
    run = True
    FPS = 60
    clock = pg.time.Clock()
    # Mainloop
    while run:
        # Max Fps - Makes it consitent no matter what system you're using
        clock.tick(FPS)
        for event in pg.event.get():  # Breaks out of the while loop if the window gets closed
            if event.type == pg.QUIT:
                run = False

        screen.fill(BLACK)
        screen.blit(BG, (0, 0))
        screen.blit(SHIP, (SHIP_LOCATION))
        pg.display.update()
    pg.quit()


if __name__ == "__main__":
    main()
