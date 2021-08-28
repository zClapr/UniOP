import pyglet
from pyglet.gl import *

from framework.window import mainWindow, screenWidth, screenHeight

window = mainWindow(screenWidth*0.8, screenHeight*0.8, (__file__.split('/')[-1]), True, vsync=True)

glClearColor(0.04, 0.07, 0.17, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_CULL_FACE)
glEnable(GL_TEXTURE_2D)
glPointSize(20)

pyglet.app.run()