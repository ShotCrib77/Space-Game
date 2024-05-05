import pygame as pg
import os
import random
from pygame.locals import *
import time
import math

PLAYER_SHIP = pg.image.load(os.path.join("Assets", "RocketShip.png"))
ENEMY_SHIP = pg.image.load(os.path.join("Assets", "EnemyShip.png"))
BULLET_IMAGE = pg.image.load(os.path.join("Assets", "pixel_laser_red.png"))
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
    self.ship_img = PLAYER_SHIP
    self.mask = pg.mask.from_surface(self.ship_img)
    self.bullets = []

  def player_shoot(self, click_x, click_y):
    # Calculate relative positions
    shot_x = click_x - (self.x + 125)
    shot_y = click_y - (self.y + 20)

    # Calculate the angle in radians
    angle_radians = math.atan2(shot_y, shot_x)

    # Set bullet speed
    bullet_speed = 4  # You can adjust this speed as needed

    # Calculate velocity components based on the angle
    vel_x = bullet_speed * math.cos(angle_radians)
    vel_y = bullet_speed * math.sin(angle_radians)
    
    # Create a new bullet instance
    new_bullet = Bullet((self.x+78), (self.y-10), vel_x, vel_y)
    self.bullets.append(new_bullet)  # Add bullet to list

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
    if not BULLET_IMAGE:
      print("Failed to load bullet image")
    self.alive = True  # This flag checks if the bullet is still active

  def update_bullet(self):
    self.x += self.vx
    self.y += self.vy

    if self.x < 0 or self.x > 800 or self.y < 0 or self.y > 1000:  # Assuming screen size 800x600
        self.alive = False
  
  def draw_bullet(self, window):
    window.blit(self.bullet_image, (self.x, self.y))
    self.mask = pg.mask.from_surface(self.bullet_image)
  
    
class Enemy(Ship):
  def __init__(self, x, y, enemy_vel_y, enemy_vel_x):
    super().__init__(x, y)
    self.ship_img = ENEMY_SHIP
    self.enemy_vel_y = enemy_vel_y
    self.enemy_vel_x = enemy_vel_x
    self.mask = pg.mask.from_surface(self.ship_img)
  
  def move(self):
    self.y += self.enemy_vel_y
    self.x += self.enemy_vel_x