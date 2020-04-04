# example here: https://realpython.com/lessons/basic-pygame-program/

import pygame
import numpy as np
import my_classes
from my_classes import Population

# setup
WIDTH = my_classes.WIDTH
HEIGHT = my_classes.HEIGHT

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Viral outbreak simulator")
running = True

creatures = Population(200)

while running:
    # handle quitting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # clear screen
    screen.fill((255, 255, 255))

    creatures.update()
    creatures.draw(screen)

    pygame.display.flip()

pygame.quit()
