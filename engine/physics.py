from math import *
from utility.extramaths import *
from pyglet import graphics
from pyglet import sprite
from pyglet.gl import GL_TRIANGLE_STRIP

import random

def getSphericalLayer(layerNumber:int, r:float, pos:list, texture:list, resolution:int=10, dColorPerLayer:int=5):
    layers = []
    latiLayerAngles = floatRange(-90, 90, 180/resolution)

    for latiLayerAngle in latiLayerAngles:
        vertices, textures = [], []
        dColor = int((latiLayerAngles.index(latiLayerAngle)/len(latiLayerAngles)-0.5)*dColorPerLayer)
        texture[texture.index(max(texture))] += dColor

        for longLayerAngle in floatRange(-180, 180, 360/resolution):
            x = -cos(radians(latiLayerAngle)) * cos(radians(longLayerAngle)) * r + pos[0]
            y = sin(radians(latiLayerAngle)) * r + pos[1]
            z = cos(radians(latiLayerAngle)) * sin(radians(longLayerAngle)) * r + pos[2]

            vertices += [x,y,z]
            textures += texture

            x = -cos(radians((latiLayerAngle+(180/resolution)))) * cos(radians(longLayerAngle)) * r + pos[0]
            y = sin(radians((latiLayerAngle+(180/resolution)))) * r + pos[1]
            z = cos(radians((latiLayerAngle+(180/resolution)))) * sin(radians(longLayerAngle)) * r + pos[2]
            
            vertices += [x,y,z]
            textures += texture
        
        layers.append([vertices, textures])

    return layers[layerNumber-1]

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
        
        for layerNumber in range(1,11):
            layer = getSphericalLayer(layerNumber, self.radius, self.position, self.color)
            vertices, textures = layer[0], layer[1]

            l = self.batch.add(
                int(len(vertices)/3), GL_TRIANGLE_STRIP, None,
                ('v3f', tuple(vertices)), ('c3B', tuple(textures))
            )

            self.layers.append(l)

    def draw(self):
        for c in self.position:
            self.position[self.position.index(c)] += random.randint(-1,1)

        for layerNumber in range(0, len(self.layers)-1):
            self.layers[layerNumber].vertices[:] = getSphericalLayer(
                layerNumber, self.radius, self.position, self.color
            )[0]
            
        self.batch.draw()
    
    def update(self, dt=None):
        pass