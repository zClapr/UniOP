import pyglet

from framework.window import mainWindow, screenWidth, screenHeight
from engine.physics import celestrial_body

window = mainWindow(
    width=int(screenWidth*0.8), height=int(screenHeight*0.8), 
    caption=(__file__.split('/')[-1]), resizable=True, vsync=False
)

# basic solar system
star = celestrial_body(500, [0,0,0], [255,0,0], 0, radius=20)
planet = celestrial_body(1, [200,1,1], [0,255,0], 1, radius=8)
moon = celestrial_body(0.0001, [200,31,11], [0,0,255], 2, radius=5)

planet.setVelocity([0,0,300])
moon.setVelocity([0,10,150])

pyglet.app.run()