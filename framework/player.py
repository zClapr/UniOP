from pyglet.window import key
from math import *

class Player:
    def __init__(self,pos=(0,0,0),rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot)

    def cam_rotate(self,dx,dy):
        self.rot[0]+=dy
        self.rot[1]-=dx
        print(self.rot)
    
    def encircular_rotate(self,dx,dy):
        dx = -dx
        dy = -dy

        flat_radius = sqrt(self.pos[1]**2 + self.pos[0]**2)
        deep_radius = sqrt(self.pos[1]**2 + self.pos[2]**2)
        current_flat_angle = atan(self.pos[1]/self.pos[0])
        current_deep_angle = atan(self.pos[1]/self.pos[2])

        if self.pos[0] < 0:
            current_flat_angle += pi

        self.pos[1] = sin(dx/flat_radius + current_flat_angle) * flat_radius
        self.pos[0] = cos(dx/flat_radius + current_flat_angle) * flat_radius
        self.pos[2] = cos(dy/deep_radius + current_deep_angle) * deep_radius

        #self.rot[0] = degrees(atan(self.pos[0]/sqrt(self.pos[1]**2 + self.pos[2]**2)))
        #self.rot[1] = degrees(atan(self.pos[2]/self.pos[0]))
        #print(self.rot)
    
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