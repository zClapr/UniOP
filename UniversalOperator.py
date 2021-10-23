import pyglet

from framework.window import mainWindow, screenWidth, screenHeight
from engine.physics import celestrial_body

window = mainWindow(
    width=int(screenWidth*0.8), height=int(screenHeight*0.8), 
    caption=(__file__.split('/')[-1]), resizable=True, vsync=False
)

b1 = celestrial_body(150, [110,10,10], [255,0,0], 0, radius=10)
b2 = celestrial_body(300, [10,110,10], [0,255,0], 1, radius=20)
b3 = celestrial_body(500, [10,10,110], [0,0,255], 2, radius=30)

pyglet.app.run()