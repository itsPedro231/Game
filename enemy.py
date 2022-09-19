import pygame
from settings import *
from entity import Entity
from support import *

class Enemy(Entity):
  def __init__(self, monsterName, pos, groups, obstacleSprites, damagePlayer, deathParticles, addXp):

    super().__init__(groups)
    self.spriteType = 'enemy'

    self.importGraphics(monsterName)
    self.status = 'idle'
    self.image = self.animations[self.status][self.frameIndex]
    
    self.rect = self.image.get_rect(topleft = pos)
    self.hitbox = self.rect.inflate(0, -10)
    self.obstacleSprites = obstacleSprites

    self.monsterName = monsterName
    monsterInfo = monsterData[self.monsterName]
    self.health = monsterInfo['health']
    self.exp = monsterInfo['exp']
    self.speed = monsterInfo['speed']
    self.attackDamage = monsterInfo['damage']
    self.resistance = monsterInfo['resistance']
    self.attackRadius = monsterInfo['attack_radius']
    self.noticeRadius = monsterInfo['notice_radius']
    self.attackType = monsterInfo['attack_type']

    self.attack = True
    self.attackTime = None
    self.attackCd = 400
    self.damagePlayer = damagePlayer
    self.deathParticles = deathParticles
    self.addXp = addXp

    self.vulnerable = True
    self.timeHit = None
    self.invincibilityDuration = 300

  def importGraphics(self, name):
    self.animations = {'idle': [], 'move': [], 'attack': []}
    mainPath = f'graphics/test/monsters/{name}/'
    for animation in self.animations.keys():
      self.animations[animation] = importFolder(mainPath + animation)

  def playerDistance(self, player):
    enemyVec = pygame.math.Vector2(self.rect.center) 
    playerVec = pygame.math.Vector2(player.rect.center) 
    distance = (playerVec - enemyVec).magnitude()

    if distance > 0:
      direction = (playerVec - enemyVec).normalize()
    else:
      direction = pygame.math.Vector2()

    return (distance, direction)
  
  def getStatus(self, player):
    distance = self.playerDistance(player)[0]

    if distance <= self.attackRadius and self.attack:
      if self.status != 'attack':
        self.frameIndex = 0
      self.status = 'attack'
    elif distance <= self.noticeRadius:
      self.status = 'move'
    else:
      self.status = 'idle'     

  def actions(self, player):
    if self.status == 'attack':
      self.attackTime = pygame.time.get_ticks()
      self.damagePlayer(self.attackDamage, self.attackType)
    elif self.status == 'move':
      self.direction = self.playerDistance(player)[1]
    else:
      self.direction = pygame.math.Vector2()
  
  def animate(self):
    animation = self.animations[self.status]
    
    self.frameIndex += self.animationSpeed
    if self.frameIndex >= len(animation):
      if self.status == 'attack':
        self.attack = False
      self.frameIndex = 0

    self.image = animation[int(self.frameIndex)]
    self.rect = self.image.get_rect(center = self.hitbox.center)

    if not self.vulnerable:
      alpha = self.waveValue()
      self.image.set_alpha(alpha)
    else:
      self.image.set_alpha(255)
 
  def cooldown(self):
    currentTime = pygame.time.get_ticks()
    if not self.attack:
      if currentTime - self.attackTime >= self.attackCd:
        self.attack = True

    if not self.vulnerable:
      if currentTime - self.timeHit >= self.invincibilityDuration:
        self.vulnerable = True

  def getDamage(self, player, attackType):
    if self.vulnerable:
      self.direction = self.playerDistance(player)[1]
      if attackType == 'weapon':
        self.health -= player.getFullDamage()
      else:
        self.health -= player.magicDamage()
        
    self.timeHit = pygame.time.get_ticks()  
    self.vulnerable = False    

  def checkDeath(self):
    if self.health <= 0:
      self.kill()
      self.deathParticles(self.rect.center, self.monsterName)  
      self.addXp(self.exp)

  def hitReaction(self):
    if not self.vulnerable:
      self.direction *= -self.resistance

  def update(self):
    self.hitReaction()
    self.move(self.speed)
    self.animate()
    self.cooldown()
    self.checkDeath()

  def enemyUpdate(self, player):
    self.getStatus(player)
    self.actions(player)
      