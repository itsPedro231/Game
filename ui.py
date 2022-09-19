from turtle import screensize
import pygame
from settings import *

class UI:
  def __init__(self):
    
    self.displaySurface = pygame.display.get_surface()
    self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

    self.healthBarRect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
    self.energyBarRect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

    self.weaponGraphics = []
    for weapon in weaponData.values():
      path = weapon['graphic']
      weapon = pygame.image.load(path).convert_alpha()
      self.weaponGraphics.append(weapon)

    self.magicGraphics = []
    for magic in magicData.values():
      magic = pygame.image.load(magic['graphic']).convert_alpha()
      self.magicGraphics.append(magic)

  def showBar(self, current, maxAmount, bgRect, colour):
    pygame.draw.rect(self.displaySurface, UI_BG_COLOUR, bgRect)

    ratio = current / maxAmount
    currentWidth = bgRect.width * ratio
    currentRect = bgRect.copy()
    currentRect.width = currentWidth

    pygame.draw.rect(self.displaySurface, colour, currentRect)
    pygame.draw.rect(self.displaySurface, UI_BORDER_COLOUR, bgRect, 3)
  
  def showExp(self, exp):
    
    x = self.displaySurface.get_size()[0] - 20
    y = self.displaySurface.get_size()[1] - 20

    textSurf = self.font.render(str(int(exp)), False, TEXT_COLOUR)
    textRect = textSurf.get_rect(bottomright = (x,y))

    pygame.draw.rect(self.displaySurface, UI_BG_COLOUR, textRect.inflate(10,10))
    pygame.draw.rect(self.displaySurface, UI_BORDER_COLOUR, textRect.inflate(10,10), 3)


    self.displaySurface.blit(textSurf, textRect)

  def selectionBox(self, left, top, switched):
    bgRect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)  
    pygame.draw.rect(self.displaySurface, UI_BG_COLOUR, bgRect)
    pygame.draw.rect(self.displaySurface, UI_BORDER_COLOUR, bgRect, 3)
    if not switched:
      pygame.draw.rect(self.displaySurface, UI_BORDER_COLOUR_ACTIVE, bgRect, 3)
    else:  
      pygame.draw.rect(self.displaySurface, UI_BORDER_COLOUR, bgRect, 3)


    return bgRect

  def weaponOverlay(self, weaponIndex, switched):
    y = self.displaySurface.get_size()[1] - 90
    bgRect = self.selectionBox(10, y, switched)
    weaponSurf = self.weaponGraphics[weaponIndex]
    weaponRect = weaponSurf.get_rect(center = bgRect.center)

    self.displaySurface.blit(weaponSurf, weaponRect)

  def magicOverlay(self, magicIndex, switched):
    y = self.displaySurface.get_size()[1] - 90
    bgRect = self.selectionBox(80, y + 5, switched)
    magicSurf = self.magicGraphics[magicIndex]
    magicRect = magicSurf.get_rect(center = bgRect.center)

    self.displaySurface.blit(magicSurf, magicRect)

  def display(self, player):
    self.showBar(player.health, player.stats['health'], self.healthBarRect, HEALTH_COLOUR)
    self.showBar(player.energy, player.stats['energy'], self.energyBarRect, ENERGY_COLOUR)

    self.showExp(player.exp)

    self.weaponOverlay(player.weaponIndex, player.weaponSwitch)
    self.magicOverlay(player.magicIndex, player.magicSwitch)
    

