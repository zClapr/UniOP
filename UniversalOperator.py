import pyglet
from pyglet.gl import *

from framework.window import mainWindow, screenWidth, screenHeight
from engine.physics import celestrial_body

window = mainWindow(
    width=int(screenWidth*0.8), height=int(screenHeight*0.8), 
    caption=(__file__.split('/')[-1]), resizable=True, vsync=False
)

b1 = celestrial_body(50, [10,10,10], [0,255,0], 1, radius=4)
b2 = celestrial_body(100, [5,-5,0], [255,0,0], 0, radius=8)
b3 = celestrial_body(50, [-10,-10,-10], [0,0,255], 2, radius=3)

pyglet.app.run()