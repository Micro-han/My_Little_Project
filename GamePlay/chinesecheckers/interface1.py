import pygame

import help
import interface2


def window1():
    color_light = (202, 203, 213 )

    # dark shade of the button
    color_dark = (2, 6, 145)
    pygame.init()
    window =pygame.display.set_mode((900, 600))
    pygame.display.set_caption('Chinese Checkers')

    image = pygame.image.load("imgs/back.png")
    image = image.convert()
    smallfont1 = pygame.font.Font('fonts/december-holidays.ttf', 100)
    text1 = smallfont1.render('CHINESE CHECKERS', True, (5, 8, 119 ))
    textRect1 = text1.get_rect()
    textRect1.center = (460, 120)

    #button
    def quit():
        window.distroy()

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
    running = True
    while running:
        window.blit(pygame.transform.scale(image, (900, 600)), (0, 0))
        window.blit(text1, textRect1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        button("Play Game", 380, 270, 150, 50, color_dark, color_light,interface2.window2)
        button("Quit", 10, 400, 88, 30, color_dark, color_light, quit)
        # button("Help", 10, 450, 88, 30, color_dark, color_light, help.help)
        rect = pygame.draw.rect(window, color_dark, pygame.Rect(374, 264, 162, 62), 6, 20)
        rect2 = pygame.draw.rect(window, color_dark, pygame.Rect(4, 394, 100, 42), 6, 20)
        #rect3 = pygame.draw.rect(window, color_dark, pygame.Rect(4, 444, 100, 42), 6, 20)
        pygame.display.update()
        pygame.display.flip()


    pygame.quit()
window1()