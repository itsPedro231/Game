import pygame

class Weapon(pygame.sprite.Sprite):
  def __init__(self, player, groups):
    super().__init__(groups)
    self.spriteType = 'weapon'
    direction = player.lastSide
    
    fullPath = f'graphics/test/weapons/{player.weapon}/{direction}.png'

    self.image = pygame.image.load(fullPath).convert_alpha()
    
    if direction == 'right':
      self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))
    elif direction == 'left':
      self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16))
    elif direction == 'down':
      if player.lastSide == 'right':
        self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))
      elif player.lastSide == 'left':
        self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16))
    elif direction == 'up':
      if player.lastSide == 'right':
        self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))
      elif player.lastSide == 'left':
        self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16))

    else:
      self.rect = self.image.get_rect(center = player.rect.center)