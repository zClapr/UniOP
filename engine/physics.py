from math import *
from utility.extramaths import *
from itertools import combinations

from pyglet import graphics
from pyglet.gl import GL_TRIANGLE_STRIP
from scipy.constants import G

from datetime import datetime

class cosmos:
    objects = []
    play_speed = 1

    @classmethod
    def update(cls, dt):
        tdt = cls.play_speed * dt
        print(tdt)

        for body_pairs in combinations(cls.objects, 2):
            b1, b2 = body_pairs[0], body_pairs[1]
            pos1, pos2 = b1.position, b2.position
            offset_x, offset_y, offset_z = pos1[0]-pos2[0], pos1[1]-pos2[1], pos1[2]-pos2[2]
            ay = atan(offset_y/sqrt(offset_x**2 + offset_z**2))

            # if dz < 0:
            #     ax = -ax

            distance = sqrt((pos1[0]-pos2[0])**2 + (pos1[2]-pos2[2])**2 + (pos1[1]-pos2[1])**2)     # meters
            force = G * ((b1.mass*b2.mass)/(distance**2))
            dy = cos(ay)*force
            try: dx = (dy/offset_y)*offset_x
            except ZeroDivisionError: dx = offset_x
            try: dz = (dy/offset_y)*offset_z
            except ZeroDivisionError: dz = offset_z

            for body in body_pairs:
                delta_vector = [
                    dx/body.mass,
                    dy/body.mass,
                    dz/body.mass
                ]

            #     for vec_pos in body.acceleration:
            #         body.acceleration[body.acceleration.index(vec_pos)] += delta_vector[body.acceleration.index(vec_pos)]
                
            for body in cls.objects:
                if body.acceleration != [0,0,0]:
                    for coordinate in body.position:
                        body.position[body.position.index(coordinate)] += body.acceleration[body.position.index(coordinate)]*tdt

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

    def __init__(self, mass:float, position:list, color:list, dcolor:int, radius:float=None, density:float=None):
        cosmos.objects.append(self)

        self.mass = mass
        self.color = color
        self.batch = graphics.Batch() # sprite.Sprite()
        self.layers = []
        self.acceleration = [0,0,0]

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
        texts = self.getSphereColors(colorToBeModified=dcolor)

        for layer in verts:
            l = self.batch.add(
                int(len(layer)/3), GL_TRIANGLE_STRIP, None,
                ('v3f', tuple(layer)), ('c3B', tuple(texts[verts.index(layer)]))
            )
            self.layers.append(l)

    def draw(self):
        n = 0
        for layer in self.layers:
            layer.vertices[:] = self.getSphereVertices()[n]
            n += 1

        self.batch.draw()