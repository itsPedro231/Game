import pygame
from support import importFolder

class PlayerAnimation:
  def __init__(self):
    self.frames = {
			# magic
			'flame': importFolder('graphics/test/particles/flame/frames'),
			'aura': importFolder('graphics/test/particles/aura'),
			'heal': importFolder('graphics/test/particles/heal/frames'),
			
			# attacks 
			'claw': importFolder('graphics/test/particles/claw'),
			'slash': importFolder('graphics/test/particles/slash'),
			'stest/parkle': importFolder('graphics/test/particles/stest/parkle'),
			'leaf_attack': importFolder('graphics/test/particles/leaf_attack'),
			'thunder': importFolder('graphics/test/particles/thunder'),

			# monster deaths
			'squid': importFolder('graphics/test/particles/smoke_orange'),
			'raccoon': importFolder('graphics/test/particles/raccoon'),
			'spirit': importFolder('graphics/test/particles/nova'),
			'bamboo': importFolder('graphics/test/particles/bamboo'),
			}

  def createParticles(self, animationType, pos, groups):
    animationFrames = self.frames[animationType]
    ParticleEffect(pos, animationFrames, groups)




class ParticleEffect(pygame.sprite.Sprite):
  def __init__(self, pos, animationFrames, groups):
    super().__init__(groups)
    self.spriteType = 'magic'
    self.frameIndex = 0
    self.animationSpeed = 0.15
    self.frames = animationFrames
    self.image = self.frames[self.frameIndex]
    self.rect = self.image.get_rect(center = pos)

  
  
  def animate(self):
    self.frameIndex += self.animationSpeed
    if self.frameIndex >= len(self.frames):
      self.kill()
    else:
      self.image = self.frames[int(self.frameIndex)]  

  def update(self):
    self.animate()    