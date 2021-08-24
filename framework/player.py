import pyglet
from pyglet.window import key
from pyglet.window import mouse as m
from math import *

class Player:
    def __init__(self,pos=(0,0,0),rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot)

    def debug(self):
        pass

    def cam_rotate(self,dx,dy):
        self.rot[0]+=dy
        self.rot[1]-=dx

        if self.rot[0]>=360:self.rot[0]=0
        if self.rot[0]<=-360:self.rot[0]=0
        if self.rot[1]>=360:self.rot[0]=0
        if self.rot[1]<=-360:self.rot[0]=0

    def update_byKeys(self,dt,keys):

        In = dt*10
        rotX = radians(-self.rot[1])
        rotY = radians(-self.rot[0])

        lOriginToXZ = cos(rotY)*In
        dy = In*tan(rotY)
        dx = lOriginToXZ*sin(rotX)
        dz = lOriginToXZ*cos(rotX)

        if keys[key.W]: 
            self.pos[0]+=dx
            self.pos[1]+=dy
            self.pos[2]-=dz
        if keys[key.S]: 
            self.pos[0]-=dx
            self.pos[1]-=dy
            self.pos[2]+=dz
        if keys[key.A]: 
            self.pos[0]-=dz
            self.pos[2]-=dx
        if keys[key.D]: 
            self.pos[0]+=dz
            self.pos[2]+=dx
        
        if self.pos[1] < 0:
            self.rot[0] = degrees(atan(abs(self.pos[1]) / sqrt(self.pos[0]**2 + self.pos[2]**2)))
        elif self.pos[1] > 0:
            self.rot[0] = - degrees(atan(abs(self.pos[1]) / sqrt(self.pos[0]**2 + self.pos[2]**2)))

        if self.pos[2] > 0:
            self.rot[1] = degrees(atan(self.pos[0]/self.pos[2]))
        elif self.pos[2] < 0:
            self.rot[1] = degrees(atan(self.pos[0]/self.pos[2])) + 180