import pygame
from tkinter import *

import FourPlayers
import ThreePlayers
import TwoPlayers
import SixPlayers

def window2():
    color_light = (202, 203, 213)
    # dark shade of the button
    color_dark = (2, 6, 145)
    pygame.init()
    window=pygame.display.set_mode((900,600))
    pygame.display.set_caption('Chinese Checkers')
    image = pygame.image.load("imgs/back.png")
    image = image.convert()
    smallfont = pygame.font.Font('fonts/december-holidays.ttf',70)
    text = smallfont.render('CHOOSE NUMBER OF PLAYERS', True,(5, 8, 119 ))
    textRect=text.get_rect()
    textRect.center=(460,120)
    """def quit():
        window.distroy()"""
    #button
    def text_objects(text,font):
        textsurface =font.render(text,True , "white")
        return textsurface , textsurface.get_rect()
    def button(msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(window, ac, (x, y, w, h))

            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(window, ic, (x, y, w, h))
        smallText = pygame.font.SysFont("comicsansms", 20)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        window.blit(textSurf, textRect)
    running= True
    while running:
      events = pygame.event.get()
      window.blit(pygame.transform.scale(image, (900, 600)), (0, 0))
      window.blit(text,textRect)
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running= False
      button("2", 290, 300, 50, 30, color_dark, color_light, TwoPlayers.TwoPlayers)
      button("3", 360, 300, 50, 30, color_dark, color_light, ThreePlayers.TreePlayers)
      button("4", 430, 300, 50, 30, color_dark, color_light, FourPlayers.FoorPlayers)
      button("6", 500, 300, 50, 30, color_dark, color_light, SixPlayers.SixPlayers)
      button("Quit", 10, 400, 88, 30, color_dark, color_light, quit)
      #button("Help", 10, 450, 88, 30, color_dark, color_light, help.help)
      rect2 = pygame.draw.rect(window, color_dark, pygame.Rect(4, 394, 100, 42), 6, 20)
      #rect3 = pygame.draw.rect(window, color_dark, pygame.Rect(4, 444, 100, 42), 6, 20)
      rect4 = pygame.draw.rect(window, color_dark, pygame.Rect(284, 294, 62, 42), 6, 20)
      rect5 = pygame.draw.rect(window, color_dark, pygame.Rect(354, 294, 62, 42), 6, 20)
      rect6 = pygame.draw.rect(window, color_dark, pygame.Rect(424, 294, 62, 42), 6, 20)
      rect7 = pygame.draw.rect(window, color_dark, pygame.Rect(494, 294, 62, 42), 6, 20)
      pygame.display.update()
      pygame.display.flip()

    pygame.quit()





