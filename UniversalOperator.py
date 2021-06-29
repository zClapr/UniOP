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
pygame.font.init()

pyGameInfoObj = pygame.display.Info()
pygame.display.set_caption(__file__.split('/')[-1])
screen = pygame.display.set_mode((pyGameInfoObj.current_w, pyGameInfoObj.current_h))
on = True

fps = 60
cameraOffset = [0,0]
cameraZoom = 100
cameraChangeSpeed = 5
keyInputs = []
mouseStartPos = None
mouseEndPos = None

while on:
    #start = time.time()
    for event in pygame.event.get():
        type = event.type
        if (type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (event.type == pygame.QUIT):
            on = False
        elif type == pygame.KEYDOWN:
            keyInputs.append(event.key)
        elif type == pygame.KEYUP:
            keyInputs.remove(event.key)
        elif type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouseStartPos = event.pos
                mouseEndPos = event.pos
            elif event.button == 4:
                cameraZoom += cameraChangeSpeed
            elif event.button == 5:
                cameraZoom -= cameraChangeSpeed
        elif type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouseStartPos = None
        elif event.type == pygame.MOUSEMOTION and mouseStartPos != None:
            mouseStartPos = mouseEndPos
            mouseEndPos = event.pos
            cameraOffset[0] -= (mouseEndPos[0] - mouseStartPos[0])*(100/cameraZoom)
            cameraOffset[1] -= (mouseEndPos[1] - mouseStartPos[1])*(100/cameraZoom)
    
    if pygame.K_LEFT in keyInputs:
        cameraOffset[0] -= cameraChangeSpeed*(100/cameraZoom)
    if pygame.K_RIGHT in keyInputs:
        cameraOffset[0] += cameraChangeSpeed*(100/cameraZoom)
    if pygame.K_UP in keyInputs:
        cameraOffset[1] -= cameraChangeSpeed*(100/cameraZoom)
    if pygame.K_DOWN in keyInputs:
        cameraOffset[1] += cameraChangeSpeed*(100/cameraZoom)

    screen.fill((0, 0, 0))

    font_CSMS = pygame.font.SysFont('Comic Sans MS', 30)
    text_cameraOffset = font_CSMS.render(f'Camera Offset: {cameraOffset}', True, pygame.Color('white'), None)
    text_cameraZoom = font_CSMS.render(f'Camera Zoom: {cameraZoom}%', True, pygame.Color('white'), None)

    for celestialBody in activeBodys:
        #celestialBody.update()
        pygame.draw.circle(screen, (0,150,0), ((celestialBody.x*(cameraZoom/100))-(cameraOffset[0]*(cameraZoom/100)), 
                                              (celestialBody.y*(cameraZoom/100))-(cameraOffset[1]*(cameraZoom/100))), 
                                              celestialBody.radius*(cameraZoom/100))

    screen.blit(text_cameraOffset, (10, 10))
    screen.blit(text_cameraZoom, (10, 40))

    pygame.display.flip()

    #end = time.time()
    #elapsed = end-start

    time.sleep(1/fps)