from pyglet import graphics
from engine.graphical_support import *
from setup import active

class Model:
    def __init__(self):
        self.basicBatch = graphics.Batch()
        self.firstRender = True

    def draw(self):
        draw_cube(self.basicBatch, (0,0, 1,0, 1,1, 0,1))
        draw_axis(self.basicBatch, 'x', (165,0,0))
        draw_axis(self.basicBatch, 'y', (0,165,0))
        draw_axis(self.basicBatch, 'z', (65,65,185))

        self.basicBatch.draw()

        for cb in active:
            cb.draw()