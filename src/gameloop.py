# Modules/Libraries
import pygame as pg
from ship import EnemyManager
from upgrades import UpgradeMenuManager
from astroids import AstroidsManager
import os
from pygame.locals import *

pg.font.init()

# Constants
WIDTH = 800
HEIGHT = 1000

# Images
BG = pg.transform.scale(pg.image.load(os.path.join("assets", "background_space.png")), (WIDTH, HEIGHT))

# Fonts
game_end_font = pg.font.SysFont("verdana", 48)

# Colors
RED = "#FF0000"

def surface_scale(surface, scale_factor): # Scales everyhting on the screen (1 being default (normal scale)). A lower or higher scale will result in a blury feel - Used for upgrade menu and game over screen :)
  small_size = (int(surface.get_width() * scale_factor), int(surface.get_height() * scale_factor))
  small_surface = pg.transform.smoothscale(surface, small_size)
  blurred_surface = pg.transform.smoothscale(small_surface, (surface.get_width(), surface.get_height()))
  return blurred_surface

class GameLoopManager:
  
  def __init__(self, screen:pg.display, main_surface:pg.Surface, upgrades_menu_manager: UpgradeMenuManager, enemy_manager: EnemyManager, astroids_manager:AstroidsManager) -> None:
    self.screen = screen
    self.main_surface = main_surface
    self.upgrades_menu_manager = upgrades_menu_manager
    self.enemy_manager = enemy_manager
    self.astroids_manager = astroids_manager
    self.game_over_active = False

    self.game_over_render = game_end_font.render("Game Over", True, RED)
    self.game_over_text = self.game_over_render.get_rect()
    self.game_over_text.center = (WIDTH // 2, HEIGHT // 2)
    
    
  def draw_upgrades(self) -> None:
    self.enemy_manager.remove_enemies()
    self.astroids_manager.remove_astroids()
    scaled_surface = surface_scale(self.main_surface, 0.35)
    self.screen.blit(scaled_surface, (0, 0))
    self.upgrades_menu_manager.draw_buttons()
    self.upgrades_menu_manager.draw_upgrade_menu()
    self.upgrades_menu_manager.draw_surface(self.screen, 100, 200)
    
  def game_over(self):
    self.enemy_manager.remove_enemies()
    self.astroids_manager.remove_astroids()
    scaled_surface = surface_scale(self.main_surface, 0.35)
    self.screen.blit(self.game_over_render, self.game_over_text)
    self.screen.blit(scaled_surface, (0, 0))
    self.screen.blit(self.game_over_render, self.game_over_text)
    
  def set_game_over_active(self, state:bool) -> None:
    self.game_over_active = state