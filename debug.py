import pygame
pygame.init()
font = pygame.font.Font(None, 30)

def debug(info, y = 10, x = 10):
  displaySurface = pygame.display.get_surface()
  debugSurf = font.render(str(info), True, 'White')
  debugRect = debugSurf.get_rect(topleft = (x,y))
  pygame.draw.rect(displaySurface, 'Black', debugRect)
  displaySurface.blit(debugSurf, debugRect)