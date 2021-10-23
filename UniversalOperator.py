import pyglet

from framework.window import mainWindow, screenWidth, screenHeight
from engine.physics import celestrial_body

window = mainWindow(
    width=int(screenWidth*0.8), height=int(screenHeight*0.8), 
    caption=(__file__.split('/')[-1]), resizable=True, vsync=False
)

# b1 = celestrial_body(50, [0,10,0], [255,0,0], 0, radius=10)
# b2 = celestrial_body(60, [10,500,10], [0,255,0], 1, radius=8)
b1 = celestrial_body(100000, [50,10,10], [255,0,0], 0, radius=10)
b2 = celestrial_body(1, [15,15,15], [0,255,0], 1, radius=3)

pyglet.app.run()