import time
import pygame
import math
from Physics import *

baseStarter = 750
b1 = body(500, 0, 0)
b2 = body(500, baseStarter, 0)
b3 = body(500, (baseStarter/2), (math.sqrt(baseStarter**2 - (baseStarter/2)**2)))
activeBodys = [b1, b2, b3]

pygame.init()
pyGameInfoObj = pygame.display.Info()
screen = pygame.display.set_mode((pyGameInfoObj.current_w, pyGameInfoObj.current_h))
on = True

while on:
    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (event.type == pygame.QUIT):
            on = False
    screen.fill((0, 0, 0))

    for celestialBody in activeBodys:
        #celestialBody.update()
        pygame.draw.circle(screen, (0,150,0), (celestialBody.x, celestialBody.y), celestialBody.radius)
    
    pygame.display.flip()

    time.sleep(0.1)