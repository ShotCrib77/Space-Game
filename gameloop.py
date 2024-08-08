import pygame as pg
from ship import EnemyManager
from upgrades import UpgradeMenuManager
import os
from pygame.locals import *


pg.font.init()
pg.init()

# Constants
WIDTH = 800
HEIGHT = 1000

# Images
BG = pg.transform.scale(pg.image.load(os.path.join("assets", "background_space.png")), (WIDTH, HEIGHT))

def surface_scale(surface, scale_factor): # Scales everyhting on the screen (1 being default (normal scale)). A lower or higher scale will result in a blury feel - Used for upgrade menu
  small_size = (int(surface.get_width() * scale_factor), int(surface.get_height() * scale_factor))
  small_surface = pg.transform.smoothscale(surface, small_size)
  blurred_surface = pg.transform.smoothscale(small_surface, (surface.get_width(), surface.get_height()))
  return blurred_surface

class GameLoopManager:
  
  def __init__(self, screen:pg.display, main_surface:pg.Surface, upgrades_menu_manager: UpgradeMenuManager, enemy_manager: EnemyManager) -> None:
    self.screen = screen
    self.main_surface = main_surface
    self.upgrades_menu_manager = upgrades_menu_manager
    self.enemy_manager = enemy_manager
  
  def draw_upgrades(self) -> None:
    self.enemy_manager.remove_enemies()
    scaled_surface = surface_scale(self.main_surface, 0.35)
    self.screen.blit(scaled_surface, (0, 0))
    self.upgrades_menu_manager.draw_surface(self.screen, 100, 200)
    self.upgrades_menu_manager.draw_buttons()
    
    
    
    
  
  # Redraw inside the main function so that we can access all the variables without using paramiters.