import pygame as pg
import os
import random
from pygame.locals import *
import time
import math

PLAYER_SHIP = pg.image.load(os.path.join("Assets", "RocketShip.png"))
ENEMY_SHIP = pg.image.load(os.path.join("Assets", "EnemyShip.png"))
BULLET_IMAGE = pg.image.load(os.path.join("Assets", "laser2.png"))
clock = pg.time.Clock()

FPS = 60
class Ship:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.ship_img = None
    self.cool_down_counter = 0
  
  # Drawing ships (takes image and cordinates)
  def draw(self, window):
    window.blit(self.ship_img, (self.x, self.y))

class Player(Ship):
  def __init__(self, x, y):
    super().__init__(x, y)
    self.last_shot_time = 0
    self.cooldown = 500
    self.ship_img = PLAYER_SHIP
    self.mask = pg.mask.from_surface(self.ship_img)
    self.bullets = []

  def player_shoot(self, click_x, click_y):
    current_time = pg.time.get_ticks()
    if (current_time - self.last_shot_time) >= self.cooldown:
      # Calculate relative positions
      shot_x = click_x - (self.x + 125)
      shot_y = click_y - (self.y + 25)

      # Calculate the angle in radians
      angle_radians = math.atan2(shot_y, shot_x)

      # Set bullet speed
      bullet_speed = 4  # You can adjust this speed as needed

      # Calculate velocity components based on the angle
      vel_x = bullet_speed * math.cos(angle_radians)
      vel_y = bullet_speed * math.sin(angle_radians)
      
      # Create a new bullet instance
      new_bullet = Bullet((self.x + 125), (self.y + 30), vel_x, vel_y)
      self.bullets.append(new_bullet)  # Add bullet to list
      self.last_shot_time = current_time

  def update_player(self):
    # Update all bullets
    new_bullets = []
    for bullet in self.bullets:
      bullet.update_bullet()
      if bullet.alive:
        new_bullets.append(bullet)
    self.bullets = new_bullets  # Only keep bullets that are still 'alive'
  
  def draw_bullets(self, window):
    # Draw all bullets
    for bullet in self.bullets:
      bullet.draw_bullet(window)  # Assuming the Bullet class has a draw_bullet method


  
class Bullet:
  def __init__(self, x, y, vx, vy):
    self.x = x
    self.y = y
    self.vx = vx
    self.vy = vy
    self.bullet_image = BULLET_IMAGE
    self.angle_degrees = 90 + math.degrees(math.atan2(-vy, vx))
    self.alive = True  # This flag checks if the bullet is still active
    
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
      
  def draw_bullet(self, window):
    rect = self.rotated_image.get_rect(center=(self.x, self.y))
    window.blit(self.rotated_image, rect)
    
  
    
class Enemy(Ship):
  def __init__(self, x, y, enemy_vel_y):
    super().__init__(x, y)
    self.ship_img = ENEMY_SHIP
    self.enemy_vel_y = enemy_vel_y
    self.enemy_vel_x = 0
    self.mask = pg.mask.from_surface(self.ship_img)
    self.last_update_time = pg.time.get_ticks()
  
  def move(self):
    current_time = pg.time.get_ticks()
    if current_time - self.last_update_time >= 1000:
      self.enemy_vel_x = random.randint(-1, 1)
      self.last_update_time = current_time
      
    self.y += self.enemy_vel_y
    self.x += self.enemy_vel_x
      
class EnemyManager:
  def __init__(self, player):
    self.enemies = []
    self.player = player
  
  def create_enemy(self):
    x_spawn = random.randint(100, 600)
    new_enemy = Enemy(x_spawn, 0, 2)
    self.enemies.append(new_enemy)
    
  def update_enemies(self):
    for enemy in self.enemies:
      enemy.move()
      if enemy.y > 800 or enemy.x < -50 or enemy.x > 650:
        self.enemies.remove(enemy)
  
  def draw_enemies(self, window):
    for enemy in self.enemies:
      window.blit(enemy.ship_img, (enemy.x, enemy.y))
  
  def check_bullet_hits(self, bullets):
    for bullet in bullets:
      if bullet.alive:
        for enemy in self.enemies:
          # Calculate offsets for mask overlap
          offset_x = int((bullet.x + 20 )- (enemy.x))
          offset_y = int((bullet.y + 10) - (enemy.y))
          # Check for collision
          if enemy.mask.overlap(bullet.mask, (offset_x, offset_y)):
            print("Hit detected!")
            bullets.remove(bullet)
            self.enemies.remove(enemy)
            break  # Exit the loop as bullet is no longer active