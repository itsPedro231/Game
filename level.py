import pygame
from particles import PlayerAnimation
from settings import *
from tile import Tile
from player import Player
from debug import debug
from weapon import Weapon
from ui import UI
from enemy import Enemy
from random import randint
from particles import PlayerAnimation
from magic import MagicPlayer
from upgrade import Upgrade

class Level:
  def __init__(self):

    self.displaySurface = pygame.display.get_surface()
    self.gamePaused = False

    self.visibleSprites = YCamera()
    self.obstacleSprites = pygame.sprite.Group()

    self.currentAttack = None
    self.attackSprites = pygame.sprite.Group()
    self.attackableSprites = pygame.sprite.Group()

    self.buildMap()

    self.ui = UI()
    self.upgrade = Upgrade(self.player)

    self.playerAnimation = PlayerAnimation()
    self.magicPlayer = MagicPlayer(self.playerAnimation)

  def buildMap(self):

    for idxy, row in enumerate(map):
      
      for idxx, col in enumerate(row): 
        x = idxx * TILESIZE
        y = idxy * TILESIZE
        if col == 'X':
          Tile((x,y),[self.visibleSprites, self.obstacleSprites], 0)
        if col == 'P':  
          self.player = Player(
            (x,y),
            [self.visibleSprites], 
            self.obstacleSprites, 
            self.createAttack, 
            self.destroyAttack, 
            self.createMagic)
        if col == 'Y':
          Tile((x,y),[self.visibleSprites, self.obstacleSprites], 1)

        if col == 'E':
          enemyType = randint(0,4)
          if enemyType == 0:
            monsterName = 'bamboo'
          elif enemyType == 1:
            monsterName = 'raccoon'
          elif enemyType == 2:
            monsterName = 'spirit'
          else:
            monsterName = 'squid'

          Enemy(
            monsterName, 
            (x, y), 
            [self.visibleSprites, self.attackableSprites], 
            self.obstacleSprites,
            self.damagePlayer,
            self.deathParticles, 
            self.addXp
            )
                  
  def createAttack(self):
    self.currentAttack = Weapon(self.player, [self.visibleSprites, self.attackSprites])

  def createMagic(self, style, strength, cost):
    if style == 'heal':
      self.magicPlayer.heal(self.player, strength, cost, [self.visibleSprites])
      
    if style == 'flame':
      self.magicPlayer.flame(self.player, cost, [self.visibleSprites, self.attackSprites])

  def destroyAttack(self):
    if self.currentAttack:
      self.currentAttack.kill()
    self.currentAttack = None  

  def playerAttack(self):
    if self.attackSprites:
      for attackSprite in self.attackSprites:
        collisionSprites = pygame.sprite.spritecollide(attackSprite, self.attackableSprites, False)
        if collisionSprites:
          for targetSprite in collisionSprites:
            targetSprite.getDamage(self.player, attackSprite.spriteType)

  def damagePlayer(self, amount, attackType):
    if self.player.vulnerable and self.player.health >= 1:
      self.player.health -= amount
      self.player.vulnerable = False
      self.player.hurtTime = pygame.time.get_ticks()

      self.playerAnimation.createParticles(attackType, self.player.rect.center, [self.visibleSprites])
    # elif self.player.health < 1: self.kill()  

  def deathParticles(self, pos, particleType):
    self.playerAnimation .createParticles(particleType, pos, [self.visibleSprites])
  
  def addXp(self, amount):
    self.player.exp += amount

  def toggleMenu(self):
    self.gamePaused = not self.gamePaused

  def run(self):
    self.visibleSprites.customDraw(self.player)
    self.ui.display(self.player)

    if self.gamePaused:
      self.upgrade.display()
    else:  
      self.visibleSprites.update()  
      self.visibleSprites.enemyUpdate(self.player)
      self.playerAttack()

    

class YCamera(pygame.sprite.Group):
  def __init__(self):
    super().__init__()

    self.displaySurface = pygame.display.get_surface()
    self.halfWidth = self.displaySurface.get_size()[0] // 2
    self.halfHeight = self.displaySurface.get_size()[1] // 2
    self.offset = pygame.math.Vector2()

    self.floorSurface = pygame.image.load('graphics/test/map.png').convert()
    self.floorRect = self.floorSurface.get_rect(topleft = (-10,-10))
               
  def customDraw(self, player):
    self.offset.x = player.rect.centerx - self.halfWidth
    self.offset.y = player.rect.centery - self.halfHeight

        
    floorOffset = self.floorRect.topleft - self.offset
    self.displaySurface.blit(self.floorSurface, floorOffset)
        
    for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
      offsetPos = sprite.rect.topleft - self.offset
      self.displaySurface.blit(sprite.image, offsetPos)      

  def enemyUpdate(self, player):
    enemySprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'spriteType') and sprite.spriteType == 'enemy']
    for enemy in enemySprites:
      enemy.enemyUpdate(player)    
