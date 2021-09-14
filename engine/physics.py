from math import *
from utility.extramaths import *
from pyglet import graphics
from pyglet import sprite
from pyglet.gl import GL_TRIANGLE_STRIP

import random

class celestrial_body:
    def __init__(self, mass:float, position:list, radius:float=None, density:float=None, color:list=[56, 163, 42]):
        self.mass = mass
        self.color = color
        self.batch = graphics.Batch() # sprite.Sprite()
        self.layers = []

        if len(position) == 3:
            self.position = position
        else:
            raise ValueError("Expected 3 values, got "+str(len(position)))

        if radius != None:
            self.radius = radius
        else:
            if density == None:
                self.density = mass
                self.radius = (3*(mass/(4*pi)))**1/3
            else:
                self.density = density
                self.radius = (3*((mass*density)/(4*pi))**1/3)
    
    def get_layers(self):
        resolution = 10
        coordinates = []
        layers = []
        
        for c in self.position:
            coordinates.append(c)

        for latiLayerAngle in floatRange(-90, 90, 180/resolution):
            vertices, textures = [], []

            self.color[self.color.index(max(self.color))] += 15

            for longLayerAngle in floatRange(-180, 180, 360/resolution):
                x = -cos(radians(latiLayerAngle)) * cos(radians(longLayerAngle)) * self.radius + coordinates[0]
                y = sin(radians(latiLayerAngle)) * self.radius + coordinates[1]
                z = cos(radians(latiLayerAngle)) * sin(radians(longLayerAngle)) * self.radius + coordinates[2]

                vertices += [x,y,z]
                textures += self.color

                x = -cos(radians((latiLayerAngle+(180/resolution)))) * cos(radians(longLayerAngle)) * self.radius + coordinates[0]
                y = sin(radians((latiLayerAngle+(180/resolution)))) * self.radius + coordinates[1]
                z = cos(radians((latiLayerAngle+(180/resolution)))) * sin(radians(longLayerAngle)) * self.radius + coordinates[2]
                
                vertices += [x,y,z]
                textures += self.color
            
            layers.append([vertices, textures])

        return layers

    def draw(self):
        for c in self.position:
            self.position[self.position.index(c)] += random.randint(-5,5)

        if self.layers ==[]:
            for layer in self.get_layers():
                vertices, textures = layer[0], layer[1]

                l = self.batch.add(
                    int(len(vertices)/3), GL_TRIANGLE_STRIP, None,
                    ('v3f', tuple(vertices)), ('c3B', tuple(textures))
                )

                self.layers.append(l)
        else:
            for layer_number in range(0, len(self.layers)-1):
                self.layers[layer_number].vertices[:] = self.get_layers()[layer_number][0]
            
        self.batch.draw()
    
    def update(self, dt=None):
        pass