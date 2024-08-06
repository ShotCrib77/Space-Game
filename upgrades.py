import pygame as pg
import os
import random
from pygame.locals import *
from ship import Player
import time
import math

pg.font.init()
pg.init()

# Colors
GREY = "#636262"
BLACK = "#262626"
WHITE = "#F6F6F6"
RED = "#FF0000"

# Fonts
upgrade_font = pg.font.SysFont("verdana", 18)
upgrade_effect_font = pg.font.SysFont("verdana", 12)
main_font = pg.font.SysFont("arial", 36)


class Button:
  def __init__(self, rect:tuple, upgrade_type:str, price:int, upgrade_effect:str, color:str, action=None) -> None:
    self.rect = pg.Rect(rect)  # rect is a tuple (x, y, width, height)
    self.upgrade_type = upgrade_type
    self.upgrade_effect = upgrade_effect
    self.price = price
    self.action = action
    self.color = color
    
  def draw(self, surface:pg.Surface) -> None:
    pg.draw.rect(surface, self.color, self.rect)
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
  def __init__(self, player:Player) -> None:
    self.player = player
    self.upgrade_menu_active = False
    self.score_for_next_level = 3
    self.times_heald = 0
    # Initialize buttons
    self.button_damage = Button((50, 72, 128, 92), "DAMAGE", 100, str(self.player.damage) + " -> " + str(self.player.damage + 1) , GREY, self.damage_button_action)
    self.button_lasercd = Button((236, 72, 128, 92), "LASER CD", 100, str(self.player.cooldown) + " -> " + str(math.ceil((self.player.cooldown * 0.8))), GREY, self.lasercd_button_action)
    self.button_heal = Button((422, 72, 128, 92), "HEAL", 100, "Times Heald: " + str(self.times_heald), GREY, self.heal_button_action)
    self.button_done = Button((236, 320, 128, 92), "Done", None, None, BLACK, self.done_button_action)
    
    self.buttons = [self.button_damage, self.button_lasercd, self.button_heal, self.button_done]
    
    # Makes a grey 600x400 screen (width, height).
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
    
  def done_button_action(self) -> None:
    self.score_for_next_level = math.ceil(self.score_for_next_level * 3)
    self.set_upgrade_menu_active(False)
    
  def lasercd_button_action(self):
    self.player.cooldown = math.ceil(self.player.cooldown * 0.8)
    self.button_lasercd.upgrade_effect = str(self.player.cooldown) + " -> " + str(math.ceil((self.player.cooldown * 0.8)))
    self.button_lasercd.price = math.ceil(self.button_lasercd.price * 1.25)
    
  def damage_button_action(self) -> None:
    self.player.damage += 1
    self.button_damage.upgrade_effect = str(self.player.damage) + " -> " + str(self.player.damage + 1)
    self.button_damage.price = math.ceil(self.button_damage.price * 2.5)
  
  def heal_button_action(self) -> None:
    if self.player.health < 10:
      self.player.health = 10
      self.times_heald += 1
      self.button_heal.upgrade_effect = "Times heald: " + str(self.times_heald)
      self.button_heal.price = math.ceil(self.button_heal.price * 5)