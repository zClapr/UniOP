import time
import pygame
import math

class pBody:
    def __init__(self, mass, x, y):
        self.mass = mass
        self.x = x
        self.y = y
    def update(self, speed, mc):
        self.x += speed*(mc.x - self.x)
        self.y += speed*(mc.y - self.y)

class massCenter:
    x = []
    y = []
    def update(mc):
        massTimesX = []
        massTimesY = []
        massTotal = int()
        for n in activeBodys:
            massTimesX.append(n.x*n.mass)
            massTimesY.append(n.y*n.mass)
            massTotal += n.mass
        mc.x = sum(massTimesX) / massTotal
        mc.y = sum(massTimesY) / massTotal

baseStarter = 500
b1 = pBody(5.972*(10**24), 0, 0)
b2 = pBody(1.989*(10**30), baseStarter, 0)
b3 = pBody(1, (baseStarter/2), (math.sqrt(baseStarter**2 - (baseStarter/2)**2)))
activeBodys = [b1, b2, b3]

pygame.init()
screen = pygame.display.set_mode([500,500])
on = True

while on:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                on = False
        elif event.type == pygame.QUIT:
            on = False
    screen.fill((255, 255, 255))

    massCenter.update(massCenter)
    for n in activeBodys:
        n.update(0.1, massCenter)
        pygame.draw.circle(screen, (0,0,255), (n.x, n.y), n.mass**(1/3))
    #print([[b1.x, b1.y], [b2.x, b2.y], [b3.x, b3.y], [massCenter.x, massCenter.y]])
    
    pygame.display.flip()

    time.sleep(0.1)