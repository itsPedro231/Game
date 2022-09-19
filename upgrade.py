import pygame
from settings import *

class Upgrade:
  def __init__(self, player):
    self.displaySurface = pygame.display.get_surface()
    self.player = player
    self.attNumber = len(player.stats)
    self.maxValues = list(player.maxStats.values())
    self.attNames = list(player.stats.keys())
    self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

    self.height = self.displaySurface.get_size()[1] * 0.8
    self.width = self.displaySurface.get_size()[0] // 6
    self.createItems()

    self.selectionIndex = 0
    self.selectionTime = None
    self.canMove = True


  def input(self):
    keys = pygame.key.get_pressed()

    if self.canMove:
      if keys[pygame.K_RIGHT] and self.selectionIndex < self.attNumber - 1:
        self.selectionIndex += 1
        self.canMove = False
        self.selectionTime = pygame.time.get_ticks()
      elif keys[pygame.K_LEFT] and self.selectionIndex >= 1:
        self.selectionIndex -= 1
        self.canMove = False
        self.selectionTime = pygame.time.get_ticks()

      if keys[pygame.K_SPACE]:
        self.canMove = False
        self.selectionTime = pygame.time.get_ticks()
        self.itemList[self.selectionIndex].trigger(self.player)
        


  def selectionCd(self):
    if not self.canMove:
      currentTime = pygame.time.get_ticks()
      if currentTime - self.selectionTime >= 300:
        self.canMove = True

  def createItems(self):
    self.itemList = []

    for item, index in enumerate(range(self.attNumber)):

      fullWidth = self.displaySurface.get_size()[0] 
      increment = fullWidth // self.attNumber
      left = (item * increment) + (increment - self.width) // 2
      
      top = self.displaySurface.get_size()[1] * 0.1


      item = Item(left, top, self.width, self.height, index, self.font)
      self.itemList.append(item)

  def display(self):
    self.input()
    self.selectionCd()

    for index, item in enumerate(self.itemList):

      name = self.attNames[index]
      value = self.player.getValue(index)
      maxValue = self.maxValues[index]
      cost = self.player.getCost(index)
      item.display(self.displaySurface, self.selectionIndex, name, value, maxValue, cost)

class Item:
  def __init__(self, l, t, w, h, index, font):    
    self.rect = pygame.Rect(l, t, w, h)
    self.index = index
    self.font = font

  def displayNames(self, surface, name, cost, selected):
    colour = TEXT_COLOUR_SELECTED if selected else TEXT_COLOUR
    titleSurface = self.font.render(name, False, colour)
    titleRect = titleSurface.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0, 20))  

    costSurface = self.font.render(f'{int(cost)}', False, colour)
    costRect = costSurface.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0, 20))

    surface.blit(titleSurface, titleRect)
    surface.blit(costSurface, costRect)

  def displayBar(self, surface, value, maxValue, selected):
    top = self.rect.midtop + pygame.math.Vector2(0, 60)
    bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)
    colour = BAR_COLOUR_SELECTED if selected else BAR_COLOUR

    fullHeight = bottom[1] - top[1]
    relativeNumber = (value / maxValue) * fullHeight
    valueRect = pygame.Rect(top[0] - 15, bottom[1] - relativeNumber, 30, 10)

    pygame.draw.line(surface, colour, top, bottom, 5)
    pygame.draw.rect(surface, colour, valueRect)

  def trigger(self, player):  
    attUpgrade = list(player.stats.keys())[self.index]
    print(attUpgrade) 

    if player.exp >= player.upgradeCost[attUpgrade] and player.stats[attUpgrade] < player.maxStats[attUpgrade]:
      player.exp -= player.upgradeCost[attUpgrade]
      player.stats[attUpgrade] *= 1.2
      player.upgradeCost[attUpgrade] *= 1.4

    if player.stats[attUpgrade] > player.maxStats[attUpgrade]:
      player.stats[attUpgrade] = player.maxStats[attUpgrade]

  
  def display(self, surface, selectionNum, name, value, maxValue, cost):
    if self.index == selectionNum:
      pygame.draw.rect(surface, UPGRADE_BG_COLOUR_SELECTED, self.rect)      
      pygame.draw.rect(surface, UI_BORDER_COLOUR, self.rect, 4)  
      
    else:
      pygame.draw.rect(surface, UI_BG_COLOUR, self.rect)      
      pygame.draw.rect(surface, UI_BORDER_COLOUR, self.rect, 4)  

    self.displayNames(surface, name, cost, self.index == selectionNum)
    self.displayBar(surface, value, maxValue, self.index == selectionNum)