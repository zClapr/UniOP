from math import *
from typing import Coroutine

from pyglet.gl.gl import GL_LINES
from utility.extramaths import *
from itertools import combinations
from sys import getsizeof

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

    def getForceVectorTo(self, towards_body, arrow_mode:bool = True):
        sbp,tbp = towards_body.position, self.position
        offset_x,offset_y,offset_z = sbp[0]-tbp[0], sbp[1]-tbp[1], sbp[2]-tbp[2]
        distance = sqrt((tbp[0]-sbp[0])**2 + (tbp[2]-sbp[2])**2 + (tbp[1]-sbp[1])**2)
        force = G * ((self.mass*towards_body.mass)/(distance**2))

        try:
            ay = atan(offset_y/sqrt((offset_x**2)+(offset_z**2)))
        except ZeroDivisionError:
            if offset_y < 0:
                ay = radians(90)
            elif offset_y > 0:
                ay = radians(-90)
            else:
                ay = 0

        if arrow_mode:
            dy = sin(ay) * (
                self.radius
                -log10(force / self.mass)
            )
        else:
            dy = (sin(ay)*(force/self.mass))**1

        try:
            try: 
                dx = (dy/offset_y)*offset_x
            except ZeroDivisionError:
                ax = atan(offset_x/offset_z)

                if offset_z < 0:
                    dx = sin(ax)*(force/self.mass)
                elif offset_z > 0:
                    dx = -(sin(ax)*(force/self.mass))
                else:
                    dx = offset_x
            try: 
                dz = (dy/offset_y)*offset_z
            except ZeroDivisionError: 
                if offset_z < 0:
                    dz = cos(ax)*(force/self.mass)
                elif offset_z > 0:
                    dz = -(cos(ax)*(force/self.mass))
                else:
                    dz = offset_z
        except ZeroDivisionError:
            dx = offset_x
            dz = offset_z

        if arrow_mode:
            return list(
                self.position + [
                    self.position[0] + dx,
                    self.position[1] + dy,
                    self.position[2] + dz
                ]
            )
        else:
            return [dx, dy, dz]

    def __init__(self, mass:float, position:list, color:list, dcolor:int, radius:float=None, density:float=None):
        self.mass = mass
        self.color = color
        self.batch = graphics.Batch()
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
                ('v3f',tuple(self.getForceVectorTo(other_body))),
                ('c3B',tuple(other_body.color + other_body.color))
            ))
            other_body.vectors[self] = (other_body.batch.add(
                2,GL_LINES,None,
                ('v3f',tuple(other_body.getForceVectorTo(self))),
                ('c3B',tuple(self.color + self.color))
            ))

        cosmos.objects.append(self)

    def draw(self):
        for layer in self.layers:
            layer.vertices[:] = self.getSphereVertices()[self.layers.index(layer)]

        for targetObj in self.vectors:
            self.vectors[targetObj].vertices[:] = self.getForceVectorTo(targetObj)

        self.batch.draw()

    def setVelocity(self, value:list):
        self.velocity = value

class cosmos:
    objects = []
    vectors = []
    viewingTime = 0
    timeline = {}
    obj_combinations = list(combinations(objects, 2))
    fps = 10
    topRenderedTime = float()
    playspeed = 1

    @classmethod
    def update(cls, dt):
        cls.updateToTime(cls.viewingTime)
        if cls.viewingTime < cls.topRenderedTime:
            cls.viewingTime += (dt*cls.time_accuracy*cls.fps*cls.playspeed)
        else:
            print('MAXIMUM RENDERED TIME REACHED, CHANGE SCRIPT SETTINGS IF MORE WISH TO BE VIEWED', end='\r')

    @classmethod
    def updateToTime(cls, time):
        if cls.viewingTime != time:
            cls.viewingTime = time

        roundedTime = closest(list(cls.timeline.keys()), time)

        for body in cls.objects:
            pos_data = cls.timeline[roundedTime][cls.objects.index(body)]
            body.position = pos_data

    @classmethod
    def calc(cls, timePer, maxTime):
        cls.topRenderedTime = maxTime
        print('CALCULATION STARTED, PLEASE WAIT...')

        sPos,sVel = [], []
        for sBody in cls.objects:
            sPos.append(list(sBody.position))
            sVel.append(list(sBody.velocity))

        time = 0
        positionsAtTheTime = []
        for body in cls.objects:
            positionsAtTheTime.append(list(body.position))

        while (time < maxTime) or ((time+timePer) <= maxTime):
            for body in cls.objects:
                if body.velocity != [0,0,0]:
                    for c in body.position:
                        i = body.position.index(c)
                        body.position[i] += body.velocity[i]*timePer

                for other_body in list(body.vectors.keys()):
                    dPos = list(body.getForceVectorTo(other_body, arrow_mode=False))
                    for dPosIndicator in dPos:
                        body.velocity[dPos.index(dPosIndicator)] += (dPosIndicator*timePer)

                positionsAtTheTime[cls.objects.index(body)] = list(body.position)

            cls.timeline[float(time)] = list(positionsAtTheTime)
            time += timePer

        for body in cls.objects:
            body.position = sPos[cls.objects.index(body)]

        # with open('timeline.json', 'w+') as f:
        #     import json
        #     json.dump(cls.timeline, f)

        print(
            'SIMULATION READY!!! \n' 
            + str(byteSimplify(getsizeof(cls.timeline))) + ' total memory cached for timeline \n'
            + str(len(cls.timeline)) + ' frames are loaded, playing at ' + str(cls.fps) + ' (default) frames per second \n'
            + str(len(cls.timeline)/cls.fps) + 's of simulation is rendered, resembling ' 
            + str(display_time(cls.topRenderedTime))
        )