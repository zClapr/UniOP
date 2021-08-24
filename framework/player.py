import pyglet
from pyglet.window import key
from pyglet.window import mouse as m
from math import *

class Player:
    def __init__(self,pos=(0,0,0),rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot)
        self.dx,self.dy = 0,0

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

        if keys[key.W]:
            self.dy = -dt
        if keys[key.S]:
            self.dy = dt
        if keys[key.A]:
            self.dx = dt
        if keys[key.D]:
            self.dx = -dt

        spherical_radius = sqrt(self.pos[0]**2 + self.pos[1]**2 + self.pos[2]**2)
        ay = acos(self.pos[1]/spherical_radius) + self.dy
        ax = atan(self.pos[2]/self.pos[0]) + self.dx

        self.pos[1] = spherical_radius * cos(ay)

        if self.pos[0] <= 0:
            self.pos[0] = -spherical_radius * cos(ax) * sin(ay)
            self.pos[2] = -spherical_radius * sin(ax) * sin(ay)
        else:
            self.pos[0] = spherical_radius * cos(ax) * sin(ay)
            self.pos[2] = spherical_radius * sin(ax) * sin(ay)
        
        if self.pos[1] < 0:
            self.rot[0] = degrees(atan(abs(self.pos[1]) / sqrt(self.pos[0]**2 + self.pos[2]**2)))
        elif self.pos[1] > 0:
            self.rot[0] = - degrees(atan(abs(self.pos[1]) / sqrt(self.pos[0]**2 + self.pos[2]**2)))

        if self.pos[2] > 0:
            self.rot[1] = degrees(atan(self.pos[0]/self.pos[2]))
        elif self.pos[2] < 0:
            self.rot[1] = degrees(atan(self.pos[0]/self.pos[2])) + 180
        
        self.dx,self.dy = 0,0