from math import *
from utility.extramaths import *
from pyglet import graphics
from pyglet import sprite
from pyglet.gl import GL_TRIANGLE_STRIP

import random

class celestrial_body:

    def getSphereVertices(self, resolution:int=10):
        latiLayerAngles = floatRange(-90, 90, 180/resolution)

        total_verts = []

        for latiLayerAngle in latiLayerAngles:
            vertices = []

            for longLayerAngle in floatRange(-180, 180, 360/resolution):
                x = -cos(radians(latiLayerAngle)) * cos(radians(longLayerAngle)) * self.radius + self.position[0]
                y = sin(radians(latiLayerAngle)) * self.radius + self.position[1]
                z = cos(radians(latiLayerAngle)) * sin(radians(longLayerAngle)) * self.radius + self.position[2]

                vertices += [x,y,z]

                x = -cos(radians((latiLayerAngle+(180/resolution)))) * cos(radians(longLayerAngle)) * self.radius + self.position[0]
                y = sin(radians((latiLayerAngle+(180/resolution)))) * self.radius + self.position[1]
                z = cos(radians((latiLayerAngle+(180/resolution)))) * sin(radians(longLayerAngle)) * self.radius + self.position[2]
                
                vertices += [x,y,z]
            
            total_verts.append(vertices)
            
        return total_verts

    def getSphereColors(self, resolution:int=10, dColorPerLayer:int=25, colorToBeModified:int=1):
        latiLayerAngles = floatRange(-90, 90, 180/resolution)
        texture = self.color

        total_texts = []

        for latiLayerAngle in latiLayerAngles:
            textures = []
            texture[colorToBeModified] += dColorPerLayer

            for longLayerAngle in floatRange(-180, 180, 360/resolution):
                textures += texture
                textures += texture
            total_texts.append(textures)
        
        return total_texts

    def __init__(self, mass:float, position:list, color:list, radius:float=None, density:float=None):
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
        
        verts = self.getSphereVertices()
        texts = self.getSphereColors()

        for layer in verts:
            l = self.batch.add(
                int(len(layer)/3), GL_TRIANGLE_STRIP, None,
                ('v3f', tuple(layer)), ('c3B', tuple(texts[verts.index(layer)]))
            )
            self.layers.append(l)

    def draw(self):
        for c in self.position:
            self.position[self.position.index(c)] += random.randint(-1,1)

        n = 0
        for layer in self.layers:
            layer.vertices[:] = self.getSphereVertices()[n]
            n += 1

        self.batch.draw()
    
    def update(self, dt=None):
        pass