import time
import pygame
import math

class body:
    def __init__(self, mass, x, y, radius=None, density=None):
        self.mass = mass
        self.x = x
        self.y = y

        if radius != None:
            self.radius = radius
        else:
            if density == None:
                self.density = mass
                self.radius = (3*(mass/(4*math.pi)))**1/3
            else:
                self.density = density
                self.radius = (3*((mass*density)/(4*math.pi)))**1/3
    def update():
        #under construction
        pass

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