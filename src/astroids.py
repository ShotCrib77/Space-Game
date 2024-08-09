# Modules/Libraries
from ship import Player
import pygame as pg
from pygame.locals import *
import os
import random


# Image
ASTROID_T1_IMAGE = pg.image.load(os.path.join("assets", "astroids", "astroid_t1.png"))
ASTROID_T2_IMAGE = pg.image.load(os.path.join("assets", "astroids", "astroid_t2.png"))
ASTROID_T3_IMAGE = pg.image.load(os.path.join("assets", "astroids", "astroid_t3.png"))
ASTROID_T4_IMAGE = pg.image.load(os.path.join("assets", "astroids", "astroid_t4.png"))


class Astroid:
  def __init__(self, surface, astroid_image:pg.image, player:Player) -> None:
    self.surface = surface
    self.x = random.randint(0, 650)
    self.alive = True
    self.y = 0
    self.image = astroid_image
    self.rect = pg.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
    self.mask = pg.mask.from_surface(self.image)
    if self.x <= 400:
      self.velx = random.randint(1, 2)
    if self.x >= 400:
      self.velx = random.randint(-2, -1)
    self.vely = 1
    self.player = player
    self.last_mined = 0
  
    if astroid_image == ASTROID_T1_IMAGE:
      self.material_tier = "Metiorite Stone"
      self.astroid_health = 2
      self.material_amount = random.randint(1,3) * self.astroid_health 
    elif astroid_image == ASTROID_T2_IMAGE:
      self.material_tier = "Malachite"
      self.astroid_health = 5
      self.material_amount = random.randint(1,3) * 2 * self.astroid_health // 5
    elif astroid_image == ASTROID_T3_IMAGE:
      self.material_tier = "Blue Crystal"
      self.astroid_health = 10
      self.material_amount = random.randint(1,3) * self.astroid_health // 5
    elif astroid_image == ASTROID_T4_IMAGE:
      self.material_tier = "Magma Stone"
      self.astroid_health = 20
      self.material_amount = random.randint(1,3) * self.astroid_health // 10
    
    
    
  def update_astroids(self):
    self.x += self.velx
    self.y += self.vely

    if  self.x < 0 or self.x > 850 or self.y > 1000:
      self.alive = False
     
    
    else:
      self.mask = pg.mask.from_surface(self.image)
    
  def draw_astroid(self):
    self.surface.blit(self.image, (self.x, self.y))
    
  def draw_mask_on_screen(self, mask, offset_x=0, offset_y=0): # Debug
    mask_width, mask_height = mask.get_size()
    mask_surface = pg.Surface((mask_width, mask_height), pg.SRCALPHA)
    
    for y in range(mask_height):
      for x in range(mask_width):
        if mask.get_at((x, y)):
          mask_surface.set_at((x, y), (255, 255, 255, 128))  # Semi-transparent white for mask
    
    self.surface.blit(mask_surface, (offset_x, offset_y))
  
  def add_material(self, materials_list):
    materials_list[self.material_tier] += self.material_amount
  
  
  
  def astroid_mining(self, mining_laser_cooldown, current_time) -> None:
    if (current_time - self.last_mined) >= mining_laser_cooldown:
      original_center = self.rect.center
      if self.material_tier == "Metiorite Stone":
        self.image = pg.transform.scale_by(self.image, 0.65)
      elif self.material_tier == "Malachite":
        self.image = pg.transform.scale_by(self.image, 0.85)
      elif self.material_tier == "Blue Crystal":
        self.image = pg.transform.scale_by(self.image, 0.93)
      elif self.material_tier == "Magma Stone":
        self.image = pg.transform.scale_by(self.image, 0.975)
      self.rect = self.image.get_rect(center=original_center)
      self.astroid_health -= 1
      self.last_mined = current_time
      
 
  


class AstroidsManager:
  def __init__(self, surface, player:Player, materials_list:dict):
    self.surface = surface
    self.astroids = []
    self.player = player
    self.materials_list = materials_list
    self.mining_laser_beam_cooldown = player.mining_laser_beam_cooldown
    
    
  def spawn_astroid(self):
    astroid_type = random.randint(1, 100)
    if astroid_type <= 50: 
      astroid_image = ASTROID_T1_IMAGE
    elif  50 < astroid_type <= 75:
      astroid_image = ASTROID_T2_IMAGE
    elif  75 < astroid_type < 95:
      astroid_image = ASTROID_T3_IMAGE
    elif astroid_type >= 95:
      astroid_image = ASTROID_T4_IMAGE
      
    astroid = Astroid(self.surface, astroid_image, self.player)
    self.astroids.append(astroid)
  
  def manage_astroids(self):
    for astroid in self.astroids:
      astroid.draw_astroid()
      astroid.update_astroids()

  def check_astroids_hit(self, current_time):
    for astroid in self.astroids:
      if astroid.alive:
        offset_x = int((astroid.x)- (self.player.mining_laser_beam_rect.x))
        offset_y = int((astroid.y) - (self.player.mining_laser_beam_rect.y))
        # Checks for collision
        
        if self.player.mining_laser_beam_mask.overlap(astroid.mask, ((offset_x+40), offset_y)):
          astroid.astroid_mining(self.mining_laser_beam_cooldown, current_time)
          if astroid.astroid_health <= 0:
            self.astroids.remove(astroid)
            astroid.add_material(self.materials_list)
      else:
        self.astroids.remove(astroid)
        
  def remove_astroids(self):
    self.astroids = []