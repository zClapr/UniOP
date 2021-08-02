import pyglet
from pyglet.gl import *

from framework.window import mainWindow, screenWidth, screenHeight

if __name__ == '__main__':
    window = mainWindow(screenWidth*0.8, screenHeight*0.8, (__file__.split('/')[-1]), True)

    glClearColor(0.5,0.7,1,1)
    glEnable(GL_DEPTH_TEST)
    #glEnable(GL_CULL_FACE)

    #pyglet.clock.schedule_interval(update,1/60.0)
    pyglet.app.run()