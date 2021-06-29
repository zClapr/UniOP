import math

class body:
    def __init__(self, mass, x, y, radius=None, density=None):
        self.mass = mass
        self.x = x
        self.y = y

        if radius != None:
            self.radius = radius
        else:
            if density == None:
                self.density = mass
                self.radius = (3*(mass/(4*math.pi)))**1/3
            else:
                self.density = density
                self.radius = (3*((mass*density)/(4*math.pi)))**1/3
    def update():
        #under construction
        pass