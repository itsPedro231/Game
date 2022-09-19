import pygame
import sys
from settings import *
from level import Level



class Game:
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    pygame.display.set_caption("Pedro's game")
    self.clock = pygame.time.Clock()
    
    self.level = Level()

    self.menu()
    
    

    

  def run(self):
    while True:
      for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_m:
            self.level.toggleMenu()

      self.screen.fill('black')

      self.level.run()
      self.clock.tick(FPS)   
      pygame.display.update()
      
      


  def menu(self):

    width = self.screen.get_width()
  
    height = self.screen.get_height()
    
    font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

    text1 = font.render('quit -> 3', True, TEXT_COLOUR)
    text2 = font.render('start -> 1', True, TEXT_COLOUR)
    text3 = font.render('help -> 2', True, TEXT_COLOUR)
    text4 = font.render('score -> 4', True, TEXT_COLOUR)

    self.screen.fill((25,25,25)) 
      
    self.screen.blit(text1, (width/2, height/2 + 80)) #quit
    self.screen.blit(text2, (width/2, height/2 - 80))
    self.screen.blit(text3, (width/2, height/2))
    self.screen.blit(text4, (width/2, height/2 + 160))

    pygame.display.update() 

    

    E = True
    while E:      
              
      events = pygame.event.get()
      for event in events:
        if event.type == pygame.QUIT:
          pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_3:
              pygame.quit()
            if event.key == pygame.K_1:
              self.run()
            if event.key == pygame.K_2:
              self.help()  
            if event.key == pygame.K_4:
              self.score()  
                  
  def help(self):
    width = self.screen.get_width()
    height = self.screen.get_height()

    self.screen.fill((25,25,25))
    font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
    text1 = font.render('KEYS: (press B to go back) ', True, TEXT_COLOUR)
    text2 = font.render('W -> up // A -> left // S -> down // D -> right', True, TEXT_COLOUR)   
    text3 = font.render('SPACE -> melee attack // CTRL -> magic attack', True, TEXT_COLOUR)   
    text4 = font.render('Q -> switch melee weapon // E -> switch magic', True, TEXT_COLOUR) 
    text5 = font.render('M -> Pause and upgrade stats', True, TEXT_COLOUR)   
    text6 = font.render('On pause:', True, TEXT_COLOUR)   
    text7 = font.render('left and right arrows -> switch status', True, TEXT_COLOUR)   
    text8 = font.render('space -> upgrade selected status (consumes exp)', True, TEXT_COLOUR)   

    text9 = font.render("Death disabled! Enemy damage is not fair", True, TEXT_COLOUR) 


                           
    self.screen.blit(text1, (10, 20))
    self.screen.blit(text2, (10, 60))
    self.screen.blit(text3, (10, 90))
    self.screen.blit(text4, (10, 120))
    self.screen.blit(text5, (10, 150))
    self.screen.blit(text6, (10, 210))
    self.screen.blit(text7, (10, 240))
    self.screen.blit(text8, (10, 270))
    self.screen.blit(text9, (10, 300))
    pygame.display.update()

    while True:
      events = pygame.event.get()
      for event in events:
        if event.type == pygame.QUIT:
          pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
              self.menu()
  
  def score(self):
    
    self.screen.fill((25,25,25))
    font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

    with open('score.txt', 'r') as file: 
      lines = file.readlines()
      

    text9 = font.render(str(lines), True, TEXT_COLOUR)                 
    self.screen.blit(text9, (10, 20))
    pygame.display.update()

    while True:
      events = pygame.event.get()
      for event in events:
        if event.type == pygame.QUIT:
          pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
              self.menu()
      
if __name__ == '__main__':
  game = Game()
  game.run()