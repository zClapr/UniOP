import math

def floatRange(start, end, step):
    result = []
    tempVar = start

    while tempVar <= end:
        result.append(tempVar)
        tempVar += step
    
    return result

class body:
    def __init__(self, mass, x, y, radius=None, density=None, resolution=20):
        self.mass = mass
        self.x = x
        self.y = y
        self.resolution = resolution

        if radius != None:
            self.radius = radius
        else:
            if density == None:
                self.density = mass
                self.radius = (3*(mass/(4*math.pi)))**1/3
            else:
                self.density = density
                self.radius = (3*((mass*density)/(4*math.pi))**1/3)

    def draw(self):
        points = []
        crossedLines = floatRange(0, self.radius*2, (self.radius*2)/self.resolution)
        # get all float-numbers between 0 and diameter with step diameter/crossSectionsWanted

        for x in crossedLines:
            for y in crossedLines:
                try:
                    z = math.sqrt(self.radius**2 - x**2 - y**2)
                    point = [x, y, z]
                    points.append(point)
                except ValueError:
                    pass
        
        return points
    
    def update():
        pass