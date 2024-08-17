# Modules/Libraries
import pygame as pg
import os
from pygame.locals import *
import math
import random
from typing import Tuple, Callable

pg.font.init()

# Fonts
card_font = pg.font.SysFont("verdana", 18)
card_font2 = pg.font.SysFont("verdana", 16)

# Colors
RED = "#FF0000"
BLACK = "#262626"
WHITE = "#F6F6F6"

# Images
UPGRADE_CARD_IMAGE_T1 = pg.image.load(os.path.join("assets", "upgrade_cards", "upgrade_card_t1.png")) # 200 x 281
UPGRADE_CARD_IMAGE_T2 = pg.image.load(os.path.join("assets", "upgrade_cards", "upgrade_card_t2.png")) # 215 x 300
UPGRADE_CARD_IMAGE_T3 = pg.image.load(os.path.join("assets", "upgrade_cards", "upgrade_card_t3.png")) # 222 x 300
UPGRADE_CARD_IMAGE_T4 = pg.image.load(os.path.join("assets", "upgrade_cards", "upgrade_card_t4.png")) # 200 x 300
UPGRADE_CARD_IMAGE_T5 = pg.image.load(os.path.join("assets", "upgrade_cards", "upgrade_card_t5.png")) # 188 x 300

class UpgradeCard:
  def __init__(self, surface:pg.Surface, rarity:int, card_info:Tuple[str, str], x:int, player, y=75) -> None: # Rarity: 1 = Common, 2 = Uncommon, 3 = Rare, 4 = Epic, 5 = Legendary
    self.rarity = rarity
    self.surface = surface
    self.card_info, self.card_power = card_info
    self.x = x
    self.y = y
    self.player = player
    self.action = self.get_card_function
    if self.rarity == 1:
      self.image = UPGRADE_CARD_IMAGE_T1
    elif self.rarity == 2:
      self.image = UPGRADE_CARD_IMAGE_T2
    elif self.rarity == 3:
      self.image = UPGRADE_CARD_IMAGE_T3
    elif self.rarity == 4:
      self.image = UPGRADE_CARD_IMAGE_T4
    elif self.rarity == 5:
      self.image = UPGRADE_CARD_IMAGE_T5
    self.image_width = self.image.get_width()
    
    self.rect = pg.Rect(x, (y+95), self.image_width, self.image.get_height()) # **CORRECT RECT**
    
    self.mining_laser_beam_cooldown = 500 # Lower values => Better
    self.mining_laser_beam_cooldown_percent_mult = 1.0
    self.mining_laser_beam_cooldown_expo_mult = 1.0
    
    self.laser_cooldown = 2500 # Lower values => Better
    self.laser_cooldown_percent_mult = 1.0
    self.laser_cooldown_expo_mult = 1.0
    
    self.damage = 10 # Higher values => Better
    self.damage_percent_mult = 1.0
    self.damage_expo_mult = 1.0
    
    self.health = 10 
  
  def draw_card(self):
    self.surface.blit(self.image, (self.x, self.y))
    card_type_text_height = self.draw_text(self.card_info, ((self.x), (self.y + 100)), card_font, BLACK, self.image_width)
    self.draw_text(self.card_power, ((self.x), (self.y + 100 + card_type_text_height)), card_font2, RED, self.image_width)
  
  def get_card_function(self):
    if self.card_power[-1] == "%":
      upgrade_value = float(self.card_power[1:-1])
      self.player.stats[self.card_info]["percent_mult"] += (upgrade_value / 100) 
    elif self.card_power[-1] == "X":
      upgrade_value = float(self.card_power[:-1])
      self.player.stats[self.card_info]["expo_mult"] *= upgrade_value
    elif self.card_power[-1].isdigit():
      upgrade_value = int(self.card_power[1:])
      self.player.stats[self.card_info]["value"] += upgrade_value
      
    
  def check_click(self, mouse_pos, event, upgrades_menu):
    if self.rect.collidepoint(mouse_pos):
      if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        self.perform_action(upgrades_menu)

  def perform_action(self, upgrades_menu):
    if self.action:
      self.action()
      self.player.update_player_stats()
      upgrades_menu.done_upgrading()
  
  def draw_text(self, text, pos, font, color, max_width):
    words = text.split(' ')
    space = font.size(' ')[0]  # width of the space character
    x, y = pos
    line_spacing = font.get_linesize()  # spacing between lines
    current_line = []
    current_width = 0
    total_height = 0  # Initialize total height

    for word in words:
      word_width, word_height = font.size(word)
      if (current_width + word_width + 50) >= max_width:  # Check if the line needs to be wrapped
        # Render the current line and reset for the next line
        line_surface = font.render(' '.join(current_line), True, color)
        # Center the line
        line_x = x + (max_width - line_surface.get_width()) // 2
        self.surface.blit(line_surface, (line_x, y))
        y += line_spacing  # Move to the next line
        total_height += line_spacing  # Increment total height by line spacing
        current_line = []
        current_width = 0

      current_line.append(word)
      current_width += word_width + space

    # Render the last line if there's any words left
    if current_line:
      line_surface = font.render(' '.join(current_line), True, color)
      line_x = x + (max_width - line_surface.get_width()) // 2
      self.surface.blit(line_surface, (line_x, y))
      total_height += line_spacing  # Increment total height for the last line

    return total_height
  
  

class UpgradeCardsManager:
  def __init__(self, surface:pg.Surface, player) -> None:
    self.card_effects = ["Laser Damage", "Laser Cooldown Reduction", "Mining Beam Speed", "Xp Gain"]
    self.card_effects_power = {"Laser Damage": ["+5", "+10", "+25%", "1.25X"], "Laser Cooldown Reduction": ["+10%", "+20%", "+30%", "1.25X"], "Mining Beam Speed": ["+1", "+10%", "+25%", "1.25X"], "Xp Gain": ["+10%", "+25%", "+50%", "1.25X"]}
    self.surface = surface
    self.cards = []
    self.player = player

  def draw_cards(self):
    for card in self.cards:
      card.draw_card()

  def get_card(self, x):
    rarity = self.get_card_rarity()
    return UpgradeCard(self.surface, rarity, self.get_card_effect(rarity), x, self.player)

  def get_cards(self):
    self.cards = []
    card_1 = self.get_card(50)
    card_2 = self.get_card((100 + card_1.image_width))
    card_3 = self.get_card((card_1.image_width + card_2.image_width + 150))
    self.cards.extend([card_1, card_2, card_3])
      
  def get_card_rarity(self) -> int:
    rarity_roll = random.randint(1, 50) # **Change probabillity**
    
    if rarity_roll <= 30:
      rarity = 1 # Common
    if rarity_roll > 30 and rarity_roll <= 40:
      rarity = 2 # Uncommon
    if rarity_roll > 40 and rarity_roll <= 46:
      rarity = 3 # Rare
    if rarity_roll > 46 and rarity_roll <= 49:
      rarity = 4 # Epic
    if rarity_roll == 50:
      rarity = 5 # Legendary
    return rarity
  
  def get_card_effect(self, rarity:int) -> Tuple[str, str]:
    if rarity != 5:
      self.upgrade_type = random.choice(self.card_effects)
      self.upgrade_power = self.card_effects_power[self.upgrade_type][(rarity-1)]
      print(rarity, self.upgrade_type, self.upgrade_power)
    else:
      self.upgrade_type = "TEMP"
      self.upgrade_power = "99"
    
    return self.upgrade_type, self.upgrade_power
  
  def check_card_clicks(self, event:pg.event, upgrades_menu) -> None:
    mouse_pos = pg.mouse.get_pos()
    for card in self.cards:
      card.check_click(mouse_pos, event, upgrades_menu)
    
class UpgradesMenu:
  def __init__(self, screen:pg.display, player) -> None:
    self.screen = screen
    self.upgrade_cards_surface = pg.Surface((800, 450), pg.SRCALPHA)
    self.upgrade_cards_surface.fill((0, 0, 0, 0))
    self.upgrade_cards_manager = UpgradeCardsManager(self.upgrade_cards_surface, player)
    self.menu_active = False
    self.score_for_next_level = 10
    
  def update_score_for_next_level(self):
    self.score_for_next_level = math.ceil(self.score_for_next_level ** 1.15)
    
  def draw_menu(self) -> None:
    self.upgrade_cards_surface.fill((0, 0, 0, 0))
    self.upgrade_cards_manager.draw_cards()
    self.screen.blit(self.upgrade_cards_surface, (0, 100))

  def menu_functions(self, event:pg.event) -> None:
    self.upgrade_cards_manager.check_card_clicks(event, self)
    
  def init_menu(self) -> None:
    self.upgrade_cards_manager.get_cards()

  def activate_upgrades_menu(self, state:bool) -> None:
    self.menu_active = state
  
  def done_upgrading(self):
    self.update_score_for_next_level()
    self.activate_upgrades_menu(False)
    self.enemy_manager.boss_active(False)
  
  def import_enemy_manager(self, enemy_manager):
    self.enemy_manager = enemy_manager
    