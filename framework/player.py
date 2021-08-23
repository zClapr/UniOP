from pyglet.window import key
from math import *

class Player:
    def __init__(self,pos=(0,0,0),rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot)
        self.oriRot = [0,0]

    def debug(self):
        pass

    def cam_rotate(self,dx,dy):
        self.rot[0]+=dy
        self.rot[1]-=dx

        if self.rot[0]>=360:self.rot[0]=0
        if self.rot[0]<=-360:self.rot[0]=0
        if self.rot[1]>=360:self.rot[0]=0
        if self.rot[1]<=-360:self.rot[0]=0
    
    def encircular_rotate(self,dx,dy):
        self.oriRot[0] += dx
        self.oriRot[1] += dy

        spherical_radius = sqrt(self.pos[0]**2 + self.pos[1]**2 + self.pos[2]**2)
        dAngleDx = self.oriRot[0] / spherical_radius
        dAngleDy = self.oriRot[1] / spherical_radius

        self.pos[0] = spherical_radius * cos(dAngleDy) * sin(dAngleDx)
        self.pos[2] = spherical_radius * cos(dAngleDx)
        self.pos[1] = spherical_radius * sin(dAngleDy) * sin(dAngleDx)
    
    def zoom(self, dy):
        self.pos[0] *= (1+dy)
        self.pos[1] *= (1+dy)
        self.pos[2] *= (1+dy)

    def update(self,dt,keys):
        s = dt*10
        rotY = -self.rot[1]/180*pi
        dx = s*sin(rotY)
        dz = s*cos(rotY)
        
        if keys[key.W]: 
            self.pos[0]+=dx
            self.pos[2]-=dz
        if keys[key.S]: 
            self.pos[0]-=dx
            self.pos[2]+=dz
        if keys[key.A]: 
            self.pos[0]-=dz
            self.pos[2]-=dx
        if keys[key.D]: 
            self.pos[0]+=dz
            self.pos[2]+=dx

        if keys[key.SPACE]: 
            self.pos[1]+=s
        if keys[key.LSHIFT]: 
            self.pos[1]-=s
        
        if self.pos[1] <= 0:
            self.rot[0] = degrees(atan(abs(self.pos[1]) / sqrt(self.pos[0]**2 + self.pos[2]**2)))
        else:
            self.rot[0] = - degrees(atan(abs(self.pos[1]) / sqrt(self.pos[0]**2 + self.pos[2]**2)))

        if self.pos[2] >= 0:
            self.rot[1] = degrees(atan(self.pos[0]/self.pos[2]))
        else:
            self.rot[1] = degrees(atan(self.pos[0]/self.pos[2])) + 180