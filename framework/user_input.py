from pyglet.window import key
from math import *

class user:
    def __init__(self,pos=(0,0,0)):
        self.pos = list(pos)
        self.rot = [0,0]
        self.cam_update()
        self.dx,self.dy = 0,0
    
    def keyStateUpdate(self, dt, keys):
        s = dt*250
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

    def cam_rotate(self,dx,dy):
        self.rot[0]+=dy
        self.rot[1]-=dx

        if self.rot[0]>=360:self.rot[0]=0
        if self.rot[0]<=-360:self.rot[0]=0
        if self.rot[1]>=360:self.rot[0]=0
        if self.rot[1]<=-360:self.rot[0]=0

    def cam_update(self):
        if self.pos[1] < 0:
            self.rot[0] = degrees(atan(abs(self.pos[1]) / sqrt(self.pos[0]**2 + self.pos[2]**2)))
        elif self.pos[1] > 0:
            self.rot[0] = - degrees(atan(abs(self.pos[1]) / sqrt(self.pos[0]**2 + self.pos[2]**2)))

        if self.pos[2] > 0:
            self.rot[1] = degrees(atan(self.pos[0]/self.pos[2]))
        elif self.pos[2] < 0:
            self.rot[1] = degrees(atan(self.pos[0]/self.pos[2])) + 180

    def manual_change(self, dx=None, dy=None):
        if dx:
            self.dx = dx
        if dy:
            self.dy = dy

    def move_update(self):
        spherical_radius = sqrt(self.pos[0]**2 + self.pos[1]**2 + self.pos[2]**2)
        try:
            ay = acos(self.pos[1]/spherical_radius) + self.dy
        except ZeroDivisionError:
            ay = 0
        try:
            ax = atan(self.pos[2]/self.pos[0]) + self.dx
        except ZeroDivisionError:
            ax = 0

        self.pos[1] = spherical_radius * cos(ay)

        if self.pos[0] <= 0:
            self.pos[0] = -spherical_radius * cos(ax) * sin(ay)
            self.pos[2] = -spherical_radius * sin(ax) * sin(ay)
        else:
            self.pos[0] = spherical_radius * cos(ax) * sin(ay)
            self.pos[2] = spherical_radius * sin(ax) * sin(ay)

        self.cam_update()

        self.dx,self.dy = 0,0

    def zoom(self, scale):
        ny = (sin(atan(self.pos[1] / sqrt(self.pos[0]**2 + self.pos[2]**2))) 
            * (sqrt(self.pos[0]**2 + self.pos[1]**2 + self.pos[2]**2)*scale)
        )

        self.pos[0] *= (ny/self.pos[1])
        self.pos[2] *= (ny/self.pos[1])
        self.pos[1] = ny