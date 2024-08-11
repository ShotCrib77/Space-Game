# Modules/Libraries
import pygame as pg
import os
import random
from pygame.locals import *
import math

from upgrades import UpgradeMenuManager

pg.font.init()

# Constants
WIDTH = 800

# Colors
RED = "#FF0000"

# Images
PLAYER_SHIP = pg.image.load(os.path.join("assets", "player", "rocket_ship.png"))
ENEMY_SHIP_IMAGE_NORMAL = pg.image.load(os.path.join("assets", "enemies", "enemy_ship_normal.png"))
ENEMY_SHIP_IMAGE_SMALL = pg.image.load(os.path.join("assets", "enemies", "enemy_ship_small.png"))
ENEMY_SHIP_IMAGE_TANK = pg.image.load(os.path.join("assets", "enemies", "enemy_ship_tank.png"))
ENEMY_SHIP_IMAGE_BOSS = pg.image.load(os.path.join("assets", "enemies", "enemy_ship_boss.png"))


BULLET_IMAGE = pg.image.load(os.path.join("assets", "player", "laser2.png"))

MINING_LASER_IMAGE_FRAME_1 = pg.image.load(os.path.join("assets", "player", "laser_beam", "mining_laser_v6_frame_1.png"))
MINING_LASER_IMAGE_FRAME_2 = pg.image.load(os.path.join("assets", "player", "laser_beam", "mining_laser_v6_frame_2.png"))
MINING_LASER_IMAGE_FRAME_3 = pg.image.load(os.path.join("assets", "player", "laser_beam", "mining_laser_v6_frame_3.png"))
MINING_LASER_IMAGE_FRAME_4 = pg.image.load(os.path.join("assets", "player", "laser_beam", "mining_laser_v6_frame_4.png"))
MINING_LASER_IMAGE_FRAME_5 = pg.image.load(os.path.join("assets", "player", "laser_beam", "mining_laser_v6_frame_5.png"))

# Fonts
ship_info_font = pg.font.SysFont("arial", 30)

# Variables
clock = pg.time.Clock()



class Ship:
  def __init__(self, x:int, y:int, surface:pg.Surface):
    self.x = x
    self.y = y
    self.ship_img = None
    self.cool_down_counter = 0
    self.surface = surface
  
  def draw(self):
    self.surface.blit(self.ship_img, (self.x, self.y))

class Player(Ship):
  def __init__(self, x:int, y:int, surface:pg.Surface, player_vel:int):
    super().__init__(x, y, surface)
    self.last_shot_time = 0
    self.cooldown = 2500
    self.ship_img = PLAYER_SHIP
    self.mask = pg.mask.from_surface(self.ship_img)
    self.bullets = []
    self.score = 0
    self.damage = 1
    self.health = 10
    self.player_vel = player_vel
    self.surface = surface
    self.mining_power = 1
    self.mining_laser_beam_rect = pg.Rect((self.x + 115), (self.y - 605), 25, 650)
    self.mining_laser_beam_mask = pg.mask.from_surface(MINING_LASER_IMAGE_FRAME_1)
    self.mining_laser_beam_cooldown = 500
    
  def player_shoot(self, click_x, click_y):
    current_time = pg.time.get_ticks()
    if (current_time - self.last_shot_time) >= self.cooldown:
      # Calculate relative positions
      shot_x = click_x - (self.x + 125)
      shot_y = click_y - (self.y + 25)

      angle_radians = math.atan2(shot_y, shot_x)

      bullet_speed = 4 
    
      vel_x = bullet_speed * math.cos(angle_radians)
      vel_y = bullet_speed * math.sin(angle_radians)
      
      # Create a new bullet instance
      new_bullet = Bullet((self.x + 125), (self.y + 35), vel_x, vel_y, self.surface)
      self.bullets.append(new_bullet)
      self.last_shot_time = current_time
      
  def mining_laser(self, tick:pg.time) -> None:
    #pg.draw.rect(self.surface, RED, self.mining_laser_rect) # ** FOR TESTING **
    if (tick//500) % 5 == 4:
      self.surface.blit(MINING_LASER_IMAGE_FRAME_1, ((self.x + 80), (self.y - 605)))
    elif (tick//500) % 5 == 3: 
      self.surface.blit(MINING_LASER_IMAGE_FRAME_2, ((self.x + 80), (self.y - 605)))
    elif (tick//500) % 5 == 2: 
      self.surface.blit(MINING_LASER_IMAGE_FRAME_3, ((self.x + 80), (self.y - 605)))
    elif (tick//500) % 5 == 1: 
      self.surface.blit(MINING_LASER_IMAGE_FRAME_4, ((self.x + 80), (self.y - 605)))
    elif (tick//500) % 5 == 0: 
      self.surface.blit(MINING_LASER_IMAGE_FRAME_5, ((self.x + 80), (self.y - 605)))
  
  def update_player(self):
    new_bullets = []
    for bullet in self.bullets:
      bullet.update_bullet()
      if bullet.alive:
        new_bullets.append(bullet)
    self.bullets = new_bullets  # Only keep bullets that are still "alive". (change name?)
  
  def draw_bullets(self):
    for bullet in self.bullets:
      bullet.draw_bullet()
  
  def update_score(self, amount):
    self.score += amount
  
  def draw_ship_info(self):
    self.score_label = ship_info_font.render(f"Score: {self.score}", True, RED)
    self.health_label = ship_info_font.render(f"Health: {self.health}", True, RED)
    self.surface.blit(self.score_label, (10, 925))
    self.surface.blit(self.health_label, (650, 925))
  
  def move(self, keys, upgrades_menu_manager, player, moving: bool, left_mouse_button_down: bool):
    moving=False
    if keys[pg.K_a] and player.x - self.player_vel > 0 and not upgrades_menu_manager.upgrade_menu_active:
      player.x -= self.player_vel
      self.mining_laser_beam_rect[0] -= self.player_vel
      moving = True
      
    elif keys[pg.K_d] and player.x + player.ship_img.get_width() + self.player_vel < WIDTH and not upgrades_menu_manager.upgrade_menu_active:
      player.x += self.player_vel
      self.mining_laser_beam_rect[0] += self.player_vel
      moving = True
    
    return moving

  
class Bullet:
  def __init__(self, x, y, vx, vy, surface):
    self.x = x
    self.y = y
    self.vx = vx
    self.vy = vy
    self.bullet_image = BULLET_IMAGE
    self.angle_degrees = 90 + math.degrees(math.atan2(-vy, vx))
    self.alive = True
    self.surface = surface
    
    self.rotated_image = pg.transform.rotate(self.bullet_image, self.angle_degrees)
    self.mask = pg.mask.from_surface(self.rotated_image)
    
  def update_bullet(self):
    self.x += self.vx
    self.y += self.vy

    if self.x < 0 or self.x > 900 or self.y < 0 or self.y > 1000:
      self.alive = False
    
    else:
      self.rotated_image = pg.transform.rotate(self.bullet_image, self.angle_degrees)
      self.mask = pg.mask.from_surface(self.rotated_image)
      
  def draw_bullet(self):
    rect = self.rotated_image.get_rect(center=(self.x, self.y))
    self.surface.blit(self.rotated_image, rect)
    
    
class Enemy(Ship):

  def __init__(self,surface: pg.Surface, x: int, y: int, enemy_image: pg.image, health: int, damage: int, vel_y:int, enemy_type: int):
    super().__init__(x, y, surface)
    self.ship_img = enemy_image
    self.enemy_vel_y = vel_y
    self.enemy_vel_x = 0
    self.damage = damage
    self.health = health
    self.mask = pg.mask.from_surface(self.ship_img)
    self.last_update_time = pg.time.get_ticks()
    self.surface = surface
    self.enemy_type = enemy_type
  
  def move(self, direction=None):
    current_time = pg.time.get_ticks()
    if direction == None:
      if current_time - self.last_update_time >= 1000:
        self.enemy_vel_x = random.randint(-1, 1)
        self.last_update_time = current_time
        
    elif direction == "<MIN":
      self.enemy_vel_x = 1
      self.last_update_time = current_time
    
    elif direction == ">MAX":
      self.enemy_vel_x = -1
      self.last_update_time = current_time
      
    self.x += self.enemy_vel_x
    self.y += self.enemy_vel_y
      
class EnemyManager:
  def __init__(self, player:Player, surface:pg.Surface, upgrades_menu_manager:UpgradeMenuManager):
    self.enemies = []
    self.player = player
    self.upgrades_menu_manager = upgrades_menu_manager
    self.surface = surface
    self.active = False
    self.level = 1  # Current game level or score/time factor
    self.enemy_configs = {
      1: {'image': ENEMY_SHIP_IMAGE_NORMAL, 'base_health': 2, 'base_damage': 1, 'base_velocity_y': 1, "enemy_type": 1}, # Normal enemy
      2: {'image': ENEMY_SHIP_IMAGE_SMALL, 'base_health': 1, 'base_damage': 1, 'base_velocity_y': 2, "enemy_type": 2}, # Small enemy
      3: {'image': ENEMY_SHIP_IMAGE_TANK, 'base_health': 5, 'base_damage': 2, 'base_velocity_y': 0.5, "enemy_type": 3}, # Tank enemy
      4: {'image': ENEMY_SHIP_IMAGE_BOSS, 'base_health': 10, 'base_damage': 3, 'base_velocity_y': 0, "enemy_type": 4} # Boss enemy
    }
    
  def scale_attribute(self, base_value: int, scale_factor: int, attribute=None) -> int | float:
    if attribute == None:
      return int(base_value + scale_factor * self.level)
    else:
      return (base_value + scale_factor * self.level)

  def create_enemy(self, enemy_type: int):
    config = self.enemy_configs.get(enemy_type)
    if config:
      if enemy_type != 4:
        x_spawn = random.randint(100, 600)
      else:
        x_spawn = 300
        
      scaled_health = self.scale_attribute(config['base_health'], 0.5)  # Increase health by 0.5 per level
      scaled_damage = self.scale_attribute(config['base_damage'], 0.1)  # Increase damage by 0.1 per level
      scaled_velocity_y = self.scale_attribute(config['base_velocity_y'], 0.1, "base_velocity_y")  # Increase velocity by 0.1 per level
      new_enemy = Enemy(self.surface, x_spawn, 1, config['image'], scaled_health, scaled_damage, scaled_velocity_y, config["enemy_type"])
      self.enemies.append(new_enemy)

  def boss_active(self, state:bool) -> None:
    self.active = state
  
  def remove_enemies(self, enemy=None):
    if enemy is None:
      self.enemies = []
    
    elif enemy in self.enemies:
      self.enemies.remove(enemy)
    
  def update_enemies(self):
    for enemy in self.enemies:
      enemy.move()
      
      if enemy.y > 850:
        self.remove_enemies(enemy)
        self.player.health -= 1
        
      elif enemy.x < -25:
        enemy.move("<MIN")
              
      elif enemy.x > 700:
        enemy.move(">MAX")

  
  def draw_enemies(self):
    for enemy in self.enemies:
      self.surface.blit(enemy.ship_img, (enemy.x, enemy.y))
  
  def check_bullet_hits(self, bullets):
    for bullet in bullets:
      if bullet.alive:
        for enemy in self.enemies:
          offset_x = int((bullet.x)- (enemy.x))
          offset_y = int((bullet.y) - (enemy.y))
          # Checks for collision
          if enemy.mask.overlap(bullet.mask, (offset_x, offset_y)):
            bullets.remove(bullet)
            enemy.health -= self.player.damage
            if enemy.health <= 0:
              if enemy.enemy_type != 4:
                self.remove_enemies(enemy)
                self.player.update_score(1)
              else:
                self.remove_enemies(enemy)
                self.player.update_score(4)
                self.upgrades_menu_manager.set_upgrade_menu_active(True)
            break