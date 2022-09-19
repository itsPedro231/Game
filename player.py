import pygame
from settings import *
from support import importFolder
import time
from entity import Entity

class Player(Entity):
  def __init__(self, pos, groups, obstacleSprites, createAttack, destroyAttack, createMagic):
    super().__init__(groups)
        
    self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
    self.lastSide = 'right'

    self.rect = self.image.get_rect(topleft = pos)
    self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET['player'])

    self.playerAssets()
    self.status = 'right'
    
    self.attacking = False
    self.attackCd = 400
    self.attackTime = None
        
    self.obstacleSprites = obstacleSprites

    self.createAttack = createAttack
    self.destroyAttack = destroyAttack
    self.weaponIndex = 0
    self.weapon = list(weaponData.keys())[self.weaponIndex]
    self.weaponSwitch = True
    self.switchTime = None
    self.switchCd = 200
    

    self.createMagic = createMagic
    self.magicIndex = 0
    self.magic = list(magicData.keys())[self.magicIndex]
    self.magicSwitch = True
    self.magicSwitchTime = None


    self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 5}
    self.maxStats = {'health': 300, 'energy': 140, 'attack': 20, 'magic': 10, 'speed': 10}
    self.upgradeCost = {'health': 100, 'energy': 100, 'attack': 100, 'magic': 100, 'speed': 100}
    self.health = self.stats['health']
    self.energy = self.stats['energy']
    self.exp = 5000
    

    self.vulnerable = True
    self.hurtTime = None
    self.invulnerabilityDuration = 500

    self.wattackSound = pygame.mixer.Sound('audio/sword.wav')
    self.wattackSound.set_volume(0.4)


  def playerAssets(self):
    charPath = 'graphics/test/player/'
    self.animations = {
      'up_left': [], 
      'up_right': [], 
      'down_left': [], 
      'down_right': [], 
      'left': [], 
      'right': [], 
      'up_right_idle': [],
      'up_left_idle': [],
      'down_right_idle': [],
      'down_left_idle': [], 
      'left_idle': [], 
      'right_idle': [],
      'up_left_attack': [], 
      'up_right_attack': [],
      'down_left_attack': [],
      'down_right_attack': [],
      'left_attack': [], 
      'right_attack': []  
    }
    for animation in self.animations.keys():
      fullPath = charPath + animation
      self.animations[animation] = importFolder(fullPath)
    

  def input(self):
    keys = pygame.key.get_pressed() 

    if keys[pygame.K_d]:
      self.direction.x = 1
      self.status = 'right'
      self.lastSide = 'right'

    elif keys[pygame.K_a]:
      self.direction.x = -1
      self.status = 'left'
      self.lastSide = 'left'

    else:
      self.direction.x = 0    


    if keys[pygame.K_w]:
      self.direction.y = -1
      if self.lastSide == 'right':
        self.status = 'up_right'
      elif self.lastSide == 'left':
        self.status = 'up_left'
      else:
        print('invalid direction W!')    
          
    elif keys[pygame.K_s]:
      self.direction.y = 1
      if self.lastSide == 'right':
        self.status = 'down_right'
      elif self.lastSide == 'left':
        self.status = 'down_left'
      else:
        print('invalid direction S!')    
      
    else:
      self.direction.y = 0        
        

    if keys[pygame.K_SPACE] and not self.attacking:
      self.attacking = True
      self.attackTime = pygame.time.get_ticks()
      self.createAttack()
      # self.wattackSound.play()

    if keys[pygame.K_LCTRL] and not self.attacking:
      self.attacking = True
      self.attackTime = pygame.time.get_ticks()   
      style = list(magicData.keys())[self.magicIndex]
      strength = list(magicData.values())[self.magicIndex]['strength'] + self.stats['magic']
      cost =  list(magicData.values())[self.magicIndex]['cost']

      self.createMagic(style, strength, cost)  

    if keys[pygame.K_q] and self.weaponSwitch == True:
      self.weaponSwitch = False
      self.switchTime = pygame.time.get_ticks()
      if self.weaponIndex < len(list(weaponData.keys())[self.weaponIndex]):
        self.weaponIndex += 1
      else: 
        self.weaponIndex = 0
      self.weapon = list(weaponData.keys())[self.weaponIndex]

    if keys[pygame.K_e] and self.magicSwitch == True:
      self.magicSwitch = False
      self.magicSwitchTime = pygame.time.get_ticks()
      if self.magicIndex < len(list(magicData.keys())) - 1:
        self.magicIndex += 1
      else: 
        self.magicIndex = 0

      self.magic = list(magicData.keys())[self.magicIndex]  

  def getStatus(self):
    if self.direction.x == 0 and self.direction.y == 0:
      if not 'idle' in self.status and not 'attack' in self.status:
        self.status = self.status + '_idle'

    if self.attacking:
      self.direction.x = 0
      self.direction.y = 0
      if not 'attack' in self.status:
        if 'idle' in self.status:
          self.status = self.status.replace('_idle','_attack')
        else:  
          self.status = self.status + '_attack'
    else:
      if 'attack' in self.status:
        self.status = self.status.replace('_attack','')    

  def cooldowns(self):
    currentTime = pygame.time.get_ticks()   

    if self.attacking:
      if currentTime - self.attackTime >= self.attackCd + weaponData[self.weapon]['cooldown']:
        self.attacking = False
        self.destroyAttack()      

    if not self.weaponSwitch:
      if currentTime - self.switchTime >= self.switchCd:
        self.weaponSwitch = True    
    
    if not self.magicSwitch:
      if currentTime - self.magicSwitchTime >= self.switchCd:
        self.magicSwitch = True     

    if not self.vulnerable:
      if currentTime - self.hurtTime >= self.invulnerabilityDuration:
        self.vulnerable = True
                            
  def animate(self):
    animation = self.animations[self.status]
    
    self.frameIndex += self.animationSpeed
    if self.frameIndex >= len(animation):
      self.frameIndex = 0

    self.image = animation[int(self.frameIndex)]
    self.rect = self.image.get_rect(center = self.hitbox.center)

    if not self.vulnerable:
      alpha = self.waveValue()
      self.image.set_alpha(alpha)
    else:
      self.image.set_alpha(255)    

  def getFullDamage(self):
    baseDamage = self.stats['attack']
    weaponDamage = weaponData[self.weapon]['damage']
    return baseDamage + weaponDamage

  def magicDamage(self):
    baseDamage = self.stats['magic']
    spellDamage = magicData[self.magic]['strength']
    
    return baseDamage + spellDamage    

  def getValue(self, index):
    return list(self.stats.values())[index]

  def getCost(self, index):    
    return list(self.upgradeCost.values())[index]

  def energyRecovery(self):
    if self.energy < self.stats['energy']:
      self.energy += 0.01 * self.stats['magic']
    else:
      self.energy = self.stats['energy']  


  def update(self):
    self.input()
    self.cooldowns()
    self.getStatus()
    self.animate()
    self.move(self.stats['speed'])
    self.energyRecovery()