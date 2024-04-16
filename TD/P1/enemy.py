import pygame as pg
from pygame.math import Vector2
import math
import constants as c
from enemy_data import ENEMY_DATA
from freeze import *




class Enemy(pg.sprite.Sprite):
  def __init__(self, enemy_type, waypoints, images):
    pg.sprite.Sprite.__init__(self)
    self.waypoints = waypoints
    self.pos = Vector2(self.waypoints[0])
    self.target_waypoint = 1
    self.health = ENEMY_DATA.get(enemy_type)["health"]
    self.speed = ENEMY_DATA.get(enemy_type)["speed"]
    self.cost = ENEMY_DATA.get(enemy_type)["cost"]
    self.unfreeznes = ENEMY_DATA.get(enemy_type)["unfreeznes"]
    self.angle = 0
    self.freezing = 1
    self.original_image = images.get(enemy_type)
    self.image = pg.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect()
    self.rect.center = self.pos
    self.max_health = self.health
    self.HP_steal = ENEMY_DATA.get(enemy_type)["HP_steal"]
    self.nearest_wayp = None
    self.movement = Vector2(0, 0)
    self.target = Vector2(0, 0)

  def update(self, world):
    self.move(world)
    self.rotate()
    self.check_alive(world)
    if self.HP_steal == 5:
      self.find_nearest_wayp()

  def move(self, world):
    #define a target waypoint
    if self.target_waypoint < len(self.waypoints):
      self.target = Vector2(self.waypoints[self.target_waypoint])
      self.movement = self.target - self.pos
    else:
      #enemy has reached the end of the path
      self.kill()
      world.health -= self.HP_steal
      world.missed_enemies += 1

    #calculate distance to target
    dist = self.movement.length()
    #check if remaining distance is greater than the enemy speed
    if dist >= (self.speed * world.game_speed):
      self.pos += self.movement.normalize() * ( world.game_speed * (self.speed / self.freezing))
    else:
      if dist != 0:
        self.pos += self.movement.normalize() * dist
      self.target_waypoint += 1

  def rotate(self):
    #calculate distance to next waypoint
    dist = self.target - self.pos
    #use distance to calculate angle
    self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
    #rotate image and update rectangle
    self.image = pg.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect()
    self.rect.center = self.pos

  def check_alive(self, world):
    if self.health <= 0:
      world.killed_enemies += 1
      world.money += self.cost
      self.kill()
      


  def draw_health_bar(self, screen):
    health_bar_width = int(self.health / self.max_health * self.rect.width * 0.5)
    health_bar_height = 5
    health_bar_color = (255, 0, 0)
    health_bar_border_color = (0, 0, 0)
    health_bar_x = self.rect.centerx - self.rect.width // 4
    health_bar_y = self.rect.top - health_bar_height - 5
    health_bar_border_rect = pg.Rect(health_bar_x - 1, health_bar_y - 1, self.rect.width * 0.5 + 2, health_bar_height + 2)
    pg.draw.rect(screen, health_bar_border_color, health_bar_border_rect)
    health_bar_rect = pg.Rect(health_bar_x, health_bar_y, health_bar_width, health_bar_height)
    pg.draw.rect(screen, health_bar_color, health_bar_rect)

  def draw(self, screen):
    screen.blit(self.image, self.rect)

  def find_nearest_wayp(self):
    if self.HP_steal == 5:
        self.nearest_wayp = None
        min_dist = float('inf')
        for waypoint in self.waypoints:
            dist = math.dist(self.pos, waypoint)
            if dist < min_dist:
                min_dist = dist
                self.nearest_wayp = waypoint
        return self.nearest_wayp


    

