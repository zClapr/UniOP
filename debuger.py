# DEBUGGER DOES CURRENTLY WORK

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from UniversalOperator import window

window.close()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev=17, azim=-108)
ax.set_xlabel('X');ax.set_ylabel('Y');ax.set_zlabel('Z')

pos = window.player.pos
window.close()
ax.scatter(pos[1], pos[0], pos[2], c='r', marker='o')
ax.plot([5, 10], [5, 10], [5, 10])

plt.show()
