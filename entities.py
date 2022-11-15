import pygame
import config as cf

class Entity:
  '''
  Base class for all entities
  was gonna implement but I don't really need it
  '''
  pass
  
class Human(Entity):
  def __init__(self, colour, xywh, velocity):
    self.x,self.y,self.w,self.h = xywh
    self.colour = colour
    self.velocity = velocity
    self.invincible = False
    self.boost = cf.PLAYER_BOOST
    self.lives = cf.PLAYER_LIVES

  def draw(self, win, colour=None, xywh=None):
    if colour is None:
      colour = self.colour
    if xywh is None:
      xywh = (self.x,self.y,self.w,self.h)
    pygame.draw.rect(win, colour, xywh)

  def walk(self, keys):
    # dashing
    vel = self.velocity
    if keys[pygame.K_SPACE]:
      if self.boost > 0:
        vel = self.velocity * 2
        self.invincible = True
        self.boost -= cf.PLAYER_BOOST_DECAY
        self.colour = (0,0,255)
      else:
          self.invincible = False
          self.colour = (255,0,0)
    else:
      vel = self.velocity
      self.invincible = False
      if self.boost < cf.PLAYER_BOOST:
        self.boost += cf.PLAYER_BOOST_REGEN
      self.colour = (255,0,0)

    # Player walking considers boundaries.
    
    if keys[pygame.K_LEFT]: 
      self.x -= vel
      if self.x < 0:
        self.x = 0
    
    if keys[pygame.K_RIGHT] and self.x < cf.SCREEN_WIDTH - cf.PLAYER_WIDTH - self.velocity:
      self.x += vel

    if keys[pygame.K_UP]:
      self.y -= vel
      if self.y < 0:
        self.y = 0
        
    if keys[pygame.K_DOWN] and self.y < cf.SCREEN_HEIGHT - cf.PLAYER_HEIGHT - self.velocity:
      self.y += vel

class CircleProjectile(Entity):
  def __init__(self,colour,center,radius,velocity,dir):
    self.colour = colour
    self.x,self.y = center
    self.rad = radius
    self.velocity = velocity
    self.dir = dir
    
  def draw(self,win,colour=None,center=None,radius=None):
    if colour is None:
      colour = self.colour
    if center is None:
      center = (self.x,self.y)
    if radius is None:
      radius = self.rad
    pygame.draw.circle(win,colour,center,radius)

  def move(self):
    self.x += self.velocity
    self.y += self.dir

  def on_screen(self):
    if self.x < 0 - self.rad or self.x > cf.SCREEN_WIDTH or self.y < 0 - self.rad or self.y > cf.SCREEN_WIDTH:
      return True
    else:
      return False