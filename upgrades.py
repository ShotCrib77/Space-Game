import pygame as pg
import os
import random
from pygame.locals import *
import time
import math

pg.font.init()
pg.init()


global upgrade_menu_active

# Colors
GREY = "#636262"
BLACK = "#262626"
WHITE = "#F6F6F6"
RED = "#FF0000"

# Fonts
upgrade_font = pg.font.SysFont("verdana", 18)
upgrade_effect_font = pg.font.SysFont("verdana", 12)
main_font = pg.font.SysFont("arial", 36)


def action_button_1():
  print("Meow")

def action_button_2():
  print("Woof")

def action_button_3():
  print("MUU")


class Button:
  def __init__(self, rect:tuple, upgrade_type:str, price:int, upgrade_effect:str, color:str, action=None) -> None:
    self.rect = pg.Rect(rect)  # rect is a tuple (x, y, width, height)
    self.upgrade_type = upgrade_type
    self.upgrade_effect = upgrade_effect
    self.price = price
    self.action = action
    self.color = color
    
  def draw(self, surface:pg.Surface) -> None:
    button_rectangle = pg.draw.rect(surface, self.color, self.rect)
    if self.upgrade_type != None:
      button_info = upgrade_font.render(self.upgrade_type, True, WHITE)
      text_rect_info = button_info.get_rect(center=(self.rect.centerx, self.rect.centery - 20))
      surface.blit(button_info, text_rect_info)
    if self.upgrade_effect != None:
      button_effect = upgrade_effect_font.render(self.upgrade_effect, True, WHITE)
      text_rect_effect = button_effect.get_rect(center=(self.rect.centerx, self.rect.centery))
      surface.blit(button_effect, text_rect_effect)
    if self.price != None:
      button_price = upgrade_effect_font.render("Price: " + str(self.price), True, RED)
      text_rect_price = button_price.get_rect(center=(self.rect.centerx, self.rect.centery + 20))
      surface.blit(button_price, text_rect_price)

  def is_clicked(self, event):
    if event.type == pg.MOUSEBUTTONDOWN:
      adjusted_event_pos = (event.pos[0] - 100, event.pos[1] - 200)
      if self.rect.collidepoint((adjusted_event_pos)):
        if self.action:
          self.action()
          return True
    return False
  

class UpgradeMenuManager:
  def __init__(self) -> None:
    # Initialize buttons
    self.button_dmg = Button((50, 72, 128, 92), "DAMAGE", 100, "1 -> 2", GREY, action_button_1)
    self.button_lasercd = Button((236, 72, 128, 92), "LASER CD", 100, "2500 -> 2250", GREY, action_button_2)
    self.button_heal = Button((422, 72, 128, 92), "HEAL", 100, "Times Heald: 0", GREY, action_button_3)
    self.button_done = Button((236, 320, 128, 92), "Done", None, None, BLACK, self.done_button)
    
    self.upgrade_menu_active = False
    self.buttons = [self.button_dmg, self.button_lasercd, self.button_heal, self.button_done]
    self.score_for_next_level = 3
    # Makes a grey 600x400 screen (widthxheight).
    self.upgrade_menu_surface = pg.Surface((600, 400))
    
    # Upgrade Header
    self.upgrade_menu_surface.fill(BLACK)
    self.upgrade_header_rect = pg.Rect(236, 24, 128, 64)
    self.upgrade_header = main_font.render("Upgrades", True, WHITE)
    self.upgrade_header_text = self.upgrade_header.get_rect(center=(self.upgrade_header_rect.centerx, self.upgrade_header_rect.centery - 20))
    self.upgrade_menu_surface.blit(self.upgrade_header, self.upgrade_header_text)
    
  def draw_surface(self, screen:pg.display, start_x:int, start_y:int) -> None:
    screen.blit(self.upgrade_menu_surface, (start_x, start_y))
  
  def set_upgrade_menu_active(self, state:bool) -> None:
    self.upgrade_menu_active = state
  
  def draw_buttons(self) -> None:
    [button.draw(self.upgrade_menu_surface) for button in self.buttons]

  def button_interaction(self, event:pg.event) -> None:
    [button.is_clicked(event) for button in self.buttons]
    
  def done_button(self) -> None:
    self.score_for_next_level = math.ceil(self.score_for_next_level * 3)
    self.set_upgrade_menu_active(False)