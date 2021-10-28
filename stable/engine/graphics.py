from pyglet import graphics
from engine.graphical_support import *
from engine.physics import cosmos

class Model:
    def __init__(self):
        self.basicBatch = graphics.Batch()
        self.firstRender = True

    def draw(self):
        draw_axis(self.basicBatch, 'x', (165,0,0))
        draw_axis(self.basicBatch, 'y', (0,165,0))
        draw_axis(self.basicBatch, 'z', (65,65,185))

        self.basicBatch.draw()

        for cb in cosmos.objects:
            cb.draw()