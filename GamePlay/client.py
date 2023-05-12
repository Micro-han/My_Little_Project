import pygame
from network import Network

from reversi import *


def main():
    run = True
    clock = pygame.time.Clock()
    p = reversi.game_manager()
    n = Network()
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        p.play()


if __name__ == '__main__':
    main()