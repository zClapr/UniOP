import math
from engine.physics import body

baseStarter = 750
b1 = body(500, 0, 0)
b2 = body(500, baseStarter, 0)
b3 = body(500, (baseStarter/2), (math.sqrt(baseStarter**2 - (baseStarter/2)**2)))

active = [b1, b2, b3]