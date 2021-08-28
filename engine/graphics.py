from pyglet import graphics
from engine.graphical_support import *

class Model:

    def __init__(self):
        self.batch = graphics.Batch()

    def draw(self):
        draw_cube(self.batch, (0,0, 1,0, 1,1, 0,1))
        draw_axis(self.batch, 'x', (165,0,0))
        draw_axis(self.batch, 'y', (0,165,0))
        draw_axis(self.batch, 'z', (65,65,185))
        draw_sphere(self.batch, [0,0,0], 5, 10, [0,255,0])

        self.batch.draw()