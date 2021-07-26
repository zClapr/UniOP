import math
import pyglet
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse

from Physics import *

baseStarter = 750
b1 = body(500, 0, 0)
b2 = body(500, baseStarter, 0)
b3 = body(500, (baseStarter/2), (math.sqrt(baseStarter**2 - (baseStarter/2)**2)))
activeBodies = [b1, b2, b3]

userScreen = pyglet.canvas.Display().get_default_screen()
screenWidth, screenHeight = userScreen.width, userScreen.height
window = pyglet.window.Window(screenWidth*0.8, screenHeight*0.8, (__file__.split('/')[-1]), True)
window.set_minimum_size(screenWidth*0.4, screenHeight*0.4)

on = True

fps = 60
cameraOffset = [0,0]
cameraZoom = 100
camPos = [0,0,-20]
camRotX = 0
camRotY = 0

text_cameraOffset = pyglet.text.Label(f'Camera Offset: {cameraOffset}', font_name='Courier New', font_size=30, x=10, y=10)
text_cameraZoom = pyglet.text.Label(f'Camera Zoom: {cameraZoom}%', font_name='Courier New', font_size=30, x=10, y=40)

@window.event
def on_draw():
    window.clear()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 1, 0.1, 100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glTranslatef(*camPos)
    glRotatef(camRotY, 1, 0, 0)
    glRotatef(camRotX, 0, 1, 0)

    glBegin(GL_POLYGON)
    for body in activeBodies:
        for point in body.draw():
            glVertex3f(point[0], point[1], point[2])
    glEnd()

    glFlush()

@window.event
def on_key_press(s,m):
    global camRotX, camRotY

    if s == (pyglet.window.key.W or pyglet.window.key.UP):
        camRotY -= 10
    if s == (pyglet.window.key.S or pyglet.window.key.DOWN):
        camRotY += 10
    if s == (pyglet.window.key.A or pyglet.window.key.LEFT):
        camRotX += 10
    if s == (pyglet.window.key.D or pyglet.window.key.RIGHT):
        camRotX -= 10

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global camRotX, camRotY

    if buttons & mouse.LEFT:
        camRotX -= dx
        camRotY += dy

#pyglet.clock.schedule_interval(update,1/60.0)
pyglet.app.run()