# Modules/Libraries
import pygame as pg
import os
from pygame.locals import *
import math

pg.font.init()

# Colors
GREY = "#636262"
BLACK = "#262626"
WHITE = "#F6F6F6"
RED = "#FF0000"

# Fonts
upgrade_font = pg.font.SysFont("verdana", 18)
upgrade_effect_font = pg.font.SysFont("verdana", 12)
material_font = pg.font.SysFont("Arial", 16)
main_font = pg.font.SysFont("arial", 36)

# Images
MATERIAL_IMAGE_T1 = pg.image.load(os.path.join("assets", "materials", "material_t1.png"))
MATERIAL_IMAGE_T2 = pg.image.load(os.path.join("assets", "materials", "material_t2.png"))
MATERIAL_IMAGE_T3 = pg.image.load(os.path.join("assets", "materials", "material_t3.png"))
MATERIAL_IMAGE_T4 = pg.image.load(os.path.join("assets", "materials", "material_t4.png"))

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

  def is_clicked(self, event, right_click=False) -> bool:
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 or right_click == True:
      adjusted_event_pos = (event.pos[0] - 100, event.pos[1] - 200)
      if self.rect.collidepoint((adjusted_event_pos)):
        if self.action:
          self.action()
          return True
    return False
  
  def is_right_clicked(self, event):
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
      for i in range(5):
        self.is_clicked(event, right_click=True)
  

class UpgradeMenuManager:
  def __init__(self, player) -> None:
    self.player = player
    self.enemy_manager = None
    self.upgrade_menu_active = False
    self.score_for_next_level = 10
    self.times_healed = 0
    self.money = 0
    self.upgrade_materials = {"Metiorite Stone": 0, "Malachite": 0, "Blue Crystal": 0, "Magma Stone": 0}
    # Initialize buttons
    self.button_damage = Button((50, 72, 128, 92), "DAMAGE", 100, str(self.player.damage) + " -> " + str(self.player.damage + 1) , GREY, self.damage_button_action)
    self.button_lasercd = Button((236, 72, 128, 92), "LASER CD", 100, str(self.player.laser_cooldown) + " -> " + str(math.ceil((self.player.laser_cooldown * 0.8))), GREY, self.lasercd_button_action)
    self.button_heal = Button((422, 72, 128, 92), "HEAL", 100, "Times Heald: " + str(self.times_healed), GREY, self.heal_button_action)
    self.button_done = Button((236, 320, 128, 92), "Done", None, None, BLACK, self.done_button_action)
    self.button_sell_t1 = Button((130, 275, 25, 25), None, None, None, BLACK, self.create_sell_material_action("Metiorite Stone"))
    self.button_sell_t2 = Button((230, 275, 25, 25), None, None, None, BLACK, self.create_sell_material_action("Malachite"))
    self.button_sell_t3 = Button((330, 275, 25, 25), None, None, None, BLACK, self.create_sell_material_action("Blue Crystal"))
    self.button_sell_t4 = Button((430, 275, 25, 25), None, None, None, BLACK, self.create_sell_material_action("Magma Stone"))
    
    self.buttons = [
      self.button_damage,
      self.button_lasercd,
      self.button_heal,
      self.button_done,
      self.button_sell_t1,
      self.button_sell_t2,
      self.button_sell_t3,
      self.button_sell_t4,
    ]
    
    # Makes a grey 600x400 screen (width, height).
    self.upgrade_menu_surface = pg.Surface((600, 400))
    
    # Upgrade Header
    self.upgrade_menu_surface.fill(BLACK)
    self.upgrade_header_rect = pg.Rect(236, 24, 128, 64)
    self.upgrade_header = main_font.render("Upgrades", True, WHITE)
    self.upgrade_header_text = self.upgrade_header.get_rect(center=(self.upgrade_header_rect.centerx, self.upgrade_header_rect.centery - 20))
    self.upgrade_menu_surface.blit(self.upgrade_header, self.upgrade_header_text)
    
    # Sell text
    self.sell_info_rect = pg.Rect(240, 240, 128, 64)
    self.sell_info = upgrade_effect_font.render("Left click: Sell 1, Right click: Sell 5", True, RED)
    self.sell_info_text = self.sell_info.get_rect(center=(self.sell_info_rect.centerx, self.sell_info_rect.centery - 20))
    self.upgrade_menu_surface.blit(self.sell_info, self.sell_info_text)
    
    # Money text rect
    self.money_rect = pg.Rect(230, 200, 128, 25)
    self.money_info = upgrade_effect_font.render("Money: " + str(self.money), True, RED)
    self.money_info_text = self.money_info.get_rect(center=(self.money_rect.centerx, self.money_rect.centery))
    self.upgrade_menu_surface.blit(self.money_info, self.money_info_text)
  
  def import_enemy_manager(self, enemy_manager):
    self.enemy_manager = enemy_manager
  
  def draw_upgrade_menu(self):
    self.clear_display_areas()

    self.redraw_material(MATERIAL_IMAGE_T1, "Metiorite Stone", 130, 275)
    self.redraw_material(MATERIAL_IMAGE_T2, "Malachite", 230, 275)
    self.redraw_material(MATERIAL_IMAGE_T3, "Blue Crystal", 330, 275)
    self.redraw_material(MATERIAL_IMAGE_T4, "Magma Stone", 430, 275)
    
    # Money
    self.money_info = upgrade_effect_font.render("Money: " + str(self.money), True, RED)
    self.money_info_text = self.money_info.get_rect(center=(self.money_rect.centerx, self.money_rect.centery))
    self.upgrade_menu_surface.blit(self.money_info, self.money_info_text)
    
  def clear_display_areas(self):
    # Clear money display area
    self.upgrade_menu_surface.fill(BLACK, self.money_rect)
    
    # Clear material display areas
    self.upgrade_menu_surface.fill(BLACK, (130, 275, 100, 25))  # Clear area for Metiorite Stone
    self.upgrade_menu_surface.fill(BLACK, (230, 275, 100, 25))  # Clear area for Malachite
    self.upgrade_menu_surface.fill(BLACK, (330, 275, 100, 25))  # Clear area for Blue Crystal
    self.upgrade_menu_surface.fill(BLACK, (430, 275, 100, 25))  # Clear area for Magma Stone

  def redraw_material(self, material_tier_image:pg.image, material_type:str, x:int, y:int) -> None:
    self.upgrade_menu_surface.blit(material_tier_image, (x, y))
    material_amount_label = material_font.render(str(self.upgrade_materials[material_type]), True, RED)
    self.upgrade_menu_surface.blit(material_amount_label, ((x+50), y))
    
  def draw_surface(self, screen:pg.display, start_x:int, start_y:int) -> None:
    screen.blit(self.upgrade_menu_surface, (start_x, start_y))
  
  def set_upgrade_menu_active(self, state:bool) -> None:
    self.upgrade_menu_active = state
  
  def draw_buttons(self) -> None:
    [button.draw(self.upgrade_menu_surface) for button in self.buttons]
    
  def button_interaction(self, event:pg.event) -> None:
    [button.is_clicked(event) for button in self.buttons]
    [button.is_right_clicked(event) for button in self.buttons]
        
  def done_button_action(self) -> None:
    self.score_for_next_level = math.ceil(self.score_for_next_level ** 1.5)
    self.set_upgrade_menu_active(False)
    self.enemy_manager.boss_active(False)
    
  def lasercd_button_action(self):
    if self.money >= self.button_lasercd.price:
      self.money -= self.button_lasercd.price
      self.player.laser_cooldown = math.ceil(self.player.laser_cooldown * 0.8)
      self.button_lasercd.upgrade_effect = str(self.player.laser_cooldown) + " -> " + str(math.ceil((self.player.laser_cooldown * 0.8)))
      self.button_lasercd.price = math.ceil(self.button_lasercd.price * 1.25) 
      
  def damage_button_action(self) -> None:
    if self.money >= self.button_damage.price:
      self.money -= self.button_damage.price
      self.player.damage += 1
      self.button_damage.upgrade_effect = str(self.player.damage) + " -> " + str(self.player.damage + 1)
      self.button_damage.price = math.ceil(self.button_damage.price * 2.5)
  
  def heal_button_action(self) -> None:
    if self.player.health < 10 and self.money >= self.button_heal.price:
      self.money -= self.button_heal.price
      self.player.health = 10
      self.times_healed += 1
      self.button_heal.upgrade_effect = "Times healed: " + str(self.times_healed)
      self.button_heal.price = math.ceil(self.button_heal.price * 5)
      
  def create_sell_material_action(self, material_tier: str):
    def sell_material() -> None:
      if self.upgrade_materials[material_tier] > 0:
        self.upgrade_materials[material_tier] -= 1
        if material_tier == "Metiorite Stone":
          self.add_money(10)
        elif material_tier == "Malachite":
          self.add_money(30)
        elif material_tier == "Blue Crystal":
          self.add_money(100)
        elif material_tier == "Magma Stone":
          self.add_money(500)
    return sell_material
  
  def add_money(self, amount:int) -> None:
    self.money += amount