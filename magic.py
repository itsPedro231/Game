import pygame
from settings import *
from random import randint

class MagicPlayer:
  def __init__(self, playerAnimation):
    self.playerAnimation = playerAnimation

  def heal(self, player, strength, cost, groups):
    if player.energy >= cost:
      player.health += strength
      player.energy -= cost
      if player.health >= player.stats['health']:
        player.health = player.stats['health']
      self.playerAnimation.createParticles('aura', player.rect.center, groups)
      self.playerAnimation.createParticles('heal', player.rect.center + pygame.math.Vector2(0, -60), groups)
          
  def flame(self, player, cost, groups):
    if player.energy >= cost:
      player.energy -= cost

      if player.status.split('_')[0] == 'right': direction = pygame.math.Vector2(1, 0)    
      elif player.status.split('_')[0] == 'left': direction = pygame.math.Vector2(-1, 0) 
      elif player.status.split('_')[1] == 'right': direction = pygame.math.Vector2(1, 0)
      elif player.status.split('_')[1] == 'left': direction = pygame.math.Vector2(-1, 0)      

     

      for i in range(1, 6):
        if direction.x:
          offsetX = (direction.x * i) * TILESIZE
          x = player.rect.centerx + offsetX
          y = player.rect.centery
          self.playerAnimation.createParticles('flame', (x,y), groups)

        else: pass  