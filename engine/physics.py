from math import *

from pyglet.gl.gl import GL_LINES
from utility.extramaths import *
from itertools import combinations

from pyglet import graphics
from pyglet.gl import GL_TRIANGLE_STRIP
from scipy.constants import G

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
        texture = list(self.color)

        total_texts = []

        for latiLayerAngle in latiLayerAngles:
            textures = []
            texture[colorToBeModified] += dColorPerLayer

            for longLayerAngle in floatRange(-180, 180, 360/resolution):
                textures += texture
                textures += texture
            total_texts.append(textures)
        
        return total_texts

    def getGravForceTo(self, body):
        pos1, pos2 = self.position, body.position
        # offset_x, offset_y, offset_z = pos1[0]-pos2[0], pos1[1]-pos2[1], pos1[2]-pos2[2]

        # if dz < 0:
        #     ax = -ax

        distance = sqrt((pos1[0]-pos2[0])**2 + (pos1[2]-pos2[2])**2 + (pos1[1]-pos2[1])**2)     # meters
        force = G * ((self.mass*body.mass)/(distance**2))       # absolute value

        return force

    def getVectorTo(self, towards_body):
        sbp,tbp = towards_body.position, self.position
        offset_x,offset_y,offset_z = sbp[0]-tbp[0], sbp[1]-tbp[1], sbp[2]-tbp[2]

        try:
            ay = atan(offset_y/sqrt((offset_x**2)+(offset_z**2)))
        except ZeroDivisionError:
            ay = 0

        dy = sin(ay) * (
            self.radius
            + self.getGravForceTo(towards_body) * 10000000000
            # + sqrt(offset_x**2 + offset_y**2 + offset_z**2)*0.1
        )

        try: dx = (dy/offset_y)*offset_x
        except ZeroDivisionError: dx = offset_x
        try: dz = (dy/offset_y)*offset_z
        except ZeroDivisionError: dz = offset_z

        return list(
            self.position + [
                self.position[0] + dx,
                self.position[1] + dy,
                self.position[2] + dz
            ]
        )

    def __init__(self, mass:float, position:list, color:list, dcolor:int, radius:float=None, density:float=None):
        self.mass = mass
        self.color = color
        self.batch = graphics.Batch() # sprite.Sprite()
        self.layers, self.vectors = [], {}
        self.velocity = [0,0,0]

        if len(position) == 3: self.position = position 
        else: raise ValueError("Expected 3 values, got "+str(len(position)))

        if radius != None: self.radius = radius
        else:
            if density == None: self.density = mass; self.radius = (3*(mass/(4*pi)))**1/3
            else: self.density = density; self.radius = (3*((mass*density)/(4*pi))**1/3)
        
        verts = self.getSphereVertices(); texts = self.getSphereColors(colorToBeModified=dcolor)
        for layer in verts:
            l = self.batch.add(
                int(len(layer)/3), GL_TRIANGLE_STRIP, None,
                ('v3f', tuple(layer)), ('c3B', tuple(texts[verts.index(layer)]))
            )
            self.layers.append(l)

        for other_body in cosmos.objects:
            self.vectors[other_body] = (self.batch.add(
                2,GL_LINES,None,
                ('v3f',tuple(self.getVectorTo(other_body))),
                ('c3B',tuple(other_body.color + other_body.color))
            ))
            other_body.vectors[self] = (other_body.batch.add(
                2,GL_LINES,None,
                ('v3f',tuple(other_body.getVectorTo(self))),
                ('c3B',tuple(self.color + self.color))
            ))

        cosmos.objects.append(self)

    def draw(self):
        for layer in self.layers:
            layer.vertices[:] = self.getSphereVertices()[self.layers.index(layer)]

        for targetObj in self.vectors:
            self.vectors[targetObj].vertices[:] = self.getVectorTo(targetObj)

        self.batch.draw()

    def setVelocity(self, value:list):
        # DEBUG ONLY
        
        self.velocity = value

class cosmos:
    objects = []
    play_speed = 1
    vectors = []

    obj_combinations = list(combinations(objects, 2))

    @classmethod
    def update(cls, dt):
        tdt = cls.play_speed * dt

        for bpair in cls.obj_combinations:
            pass
            # for body in bpair:
            #     delta_vector = [
            #         dx/body.mass,
            #         dy/body.mass,
            #         dz/body.mass
            #     ]

            #     for vec_pos in body.velocity:
            #         body.velocity[body.velocity.index(vec_pos)] += delta_vector[body.velocity.index(vec_pos)]
                
        for body in cls.objects:
            if body.velocity != [0,0,0]:
                for coordinate in body.position:
                    body.position[body.position.index(coordinate)] += body.velocity[body.position.index(coordinate)]*tdt