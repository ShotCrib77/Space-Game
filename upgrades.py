import pygame as pg
import os
import random
from pygame.locals import *
import time
import math

pg.font.init()
pg.init()

# Colors
GREY = "#b9b9b5"
BLACK = "#262626"
WHITE = "#FFFFFF"
RED = "#FF0000"

upgrade_font = pg.font.SysFont("verdana", 18)
upgrade_effect_font = pg.font.SysFont("verdana", 12)

def action_button_1():
  print("Meow")

def action_button_2():
  print("Woof")

def action_button_3():
  print("MUU")

class Button:
  def __init__(self, rect:tuple, upgrade_type:str, price:int, upgrade_effect="", action=None) -> None:
    self.rect = pg.Rect(rect)  # rect is a tuple (x, y, width, height)
    self.upgrade_type = upgrade_type
    self.upgrade_effect = upgrade_effect
    self.price = price
    self.action = action

  def draw(self, surface:pg.Surface) -> None:
    
    button_rectangle = pg.draw.rect(surface, BLACK, self.rect)
    button_info = upgrade_font.render(self.upgrade_type, True, WHITE)
    button_effect = upgrade_effect_font.render(self.upgrade_effect, True, WHITE)
    button_price = upgrade_effect_font.render("Price: " + str(self.price), True, RED)

    text_rect_info = button_info.get_rect(center=(self.rect.centerx, self.rect.centery - 20))
    text_rect_effect = button_effect.get_rect(center=(self.rect.centerx, self.rect.centery))
    text_rect_price = button_price.get_rect(center=(self.rect.centerx, self.rect.centery + 20))

    surface.blit(button_info, text_rect_info)
    surface.blit(button_effect, text_rect_effect)
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
    self.button_1 = Button((50, 24, 128, 72), "DAMAGE", 100, "1 -> 2", action_button_1)
    self.button_2 = Button((236, 24, 128, 72), "LASER CD", 100, "2500 -> 2250", action_button_2)
    self.button_3 = Button((422, 24, 128, 72), "HEAL", 100, "Times Heald: 0")
    
    self.buttons = [self.button_1, self.button_2, self.button_3]
    
    # Makes a grey 600x400 screen (widthxheight).
    self.upgrade_menu_surface = pg.Surface((600, 400))
    self.upgrade_menu_surface.fill(GREY)
  
  def draw_surface(self, screen:pg.display, start_x:int, start_y:int) -> None:
    screen.blit(self.upgrade_menu_surface, (start_x, start_y))
  
  def draw_buttons(self) -> None:
    [button.draw(self.upgrade_menu_surface) for button in self.buttons]
    
  def button_interaction(self, event:pg.event) -> None:
    [button.is_clicked(event) for button in self.buttons]