import pygame
from settings import *
from random import randint

class Tile(pygame.sprite.Sprite):
  def __init__(self, pos, groups, type):
    super().__init__(groups)
    
    PNG = randint(0,10)
    yOffset = HITBOX_OFFSET['object']
    
    if PNG >=4:
      self.image = pygame.image.load('graphics/test/tree.png').convert_alpha()
      self.rect = self.image.get_rect(topleft = pos)
      if type == 0:
        self.hitbox = self.rect.inflate(0, -70)
      else: 
        self.hitbox = self.rect.inflate(0,0)
    else:
      self.image = pygame.image.load('graphics/test/rock.png').convert_alpha()
      self.rect = self.image.get_rect(topleft = pos)
      self.hitbox = self.rect.inflate(0, -30)