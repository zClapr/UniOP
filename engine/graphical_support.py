from pyglet.gl import *
from pyglet import graphics
from pyglet import image
import itertools
from utility.extramaths import *
from math import *

def get_texure(file):
    tex = image.load(file).get_texture()
    glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
    return graphics.TextureGroup(tex)

def draw_axis(batch:graphics.Batch, rotation:str, color:tuple, color2:tuple=None, axis_length:float=25.0, tip_size:float=None):
    if not tip_size:
        tip_size = axis_length/50
    arrow_base = axis_length-(tip_size*3)
    arrow_points=[(axis_length+(tip_size/10),0,0), (arrow_base,tip_size,tip_size), (arrow_base,tip_size,-tip_size),(arrow_base,-tip_size,0)]
    line_points=[(axis_length,0,0), (-axis_length,0,0)]

    if rotation=='y':
        temp,temp2 = [],[]
        for point in arrow_points:
            temp.append((point[2],point[0],point[1]))
        arrow_points = temp

        for point in line_points:
            temp2.append((point[2],point[0],point[1]))
        line_points = temp2
    elif rotation=='z':
        temp,temp2 = [],[]
        for point in arrow_points:
            temp.append((point[1],point[2],point[0]))
        arrow_points = temp
        
        for point in line_points:
            temp2.append((point[1],point[2],point[0]))
        line_points = temp2
    elif rotation!='x':
        raise ValueError('An axis must be draw in the direction of either x, y, or z')

    arrow_triangles = list(itertools.combinations(arrow_points, 3))

    for triangle in arrow_triangles:
        batch.add(
            3,GL_TRIANGLES,None,
            ('c3B', (color[0],color[1],color[2], color[0],color[1],color[2], color[0],color[1],color[2])), 
            ('v3f', (triangle[0][0],triangle[0][1],triangle[0][2], triangle[1][0],triangle[1][1],triangle[1][2], triangle[2][0],triangle[2][1],triangle[2][2]))
        )
    
    if not color2:
        temp=[]
        for positional_color in color:
            temp.append(positional_color)
        color2 = tuple(temp)
    glLineWidth(50)
    batch.add(
        2,GL_LINES,None,
        ('c3B', (color[0],color[1],color[2], color2[0],color2[1],color2[2])),
        ('v3f', (line_points[0][0],line_points[0][1],line_points[0][2], line_points[1][0],line_points[1][1],line_points[1][2]))
    )

def draw_cube(batch:graphics.Batch, coordinates:tuple):
    side = get_texure('./assets/dirt.png')
    coords = ('t2f',coordinates)

    x,y,z = -0.5, -0.5, -0.5
    X,Y,Z = x+1,y+1,z+1
    rx,ry,rz = 0,0,0

    batch.add(4,GL_QUADS,side,('v3f',(x,y,z, x,y,Z, x,Y,Z, x,Y,z, )),coords)
    batch.add(4,GL_QUADS,side,('v3f',(X,y,Z, X,y,z, X,Y,z, X,Y,Z, )),coords)
    batch.add(4,GL_QUADS,side,('v3f',(x,y,z, X,y,z, X,y,Z, x,y,Z, )),coords)
    batch.add(4,GL_QUADS,side,('v3f',(x,Y,Z, X,Y,Z, X,Y,z, x,Y,z, )),coords)
    batch.add(4,GL_QUADS,side,('v3f',(X,y,z, x,y,z, x,Y,z, X,Y,z, )),coords)
    batch.add(4,GL_QUADS,side,('v3f',(x,y,Z, X,y,Z, X,Y,Z, x,Y,Z, )),coords)

def draw_sphere(batch:graphics.Batch, coordinates:list, radius:float, resolution:float, color:list):
    semispherical_points = []
    def sortByY(x):
        return x[1]

    for yDeg_segment in floatRange(0,180,180/resolution):
        x = radius * cos(radians(0)) * sin(radians(yDeg_segment))
        y = radius * cos(radians(yDeg_segment))
        z = radius * sin(radians(0)) * sin(radians(yDeg_segment))
        semispherical_points.append([
            x + coordinates[0],
            y + coordinates[1],
            z + coordinates[2]
        ])

    semispherical_points_sortedByY = sorted(semispherical_points, key=sortByY)
    points = []
    for point in semispherical_points_sortedByY:
        xAlignedPoints = []
        xAlignedPoints.append(point)

        if point != (semispherical_points_sortedByY[0] or semispherical_points_sortedByY[-1]):
            r = sqrt(point[0]**2 + point[2]**2)

            for xDegSegment in floatRange(0+(180/resolution), 360, 180/resolution):
                x = r * cos(radians(xDegSegment))
                z = r * sin(radians(xDegSegment))
                xAlignedPoints.append([
                    x + coordinates[0],
                    point[1] + coordinates[1],
                    z + coordinates[2]
                ])
        
        points.append(xAlignedPoints)

    quads = []
    for xAlignedPoints in points:
        for point in xAlignedPoints:
            if point != (xAlignedPoints[0] or xAlignedPoints[-1]):

                cXaPoints_index = points.index(xAlignedPoints)
                cPoint_index = xAlignedPoints.index(point)

                try:
                    quad_vertices = point + xAlignedPoints[cPoint_index+1]
                except IndexError:
                    quad_vertices = point + xAlignedPoints[0]

                try:
                    quad_vertices += points[cXaPoints_index+1][cPoint_index] + points[cXaPoints_index+1][cPoint_index+1]
                except IndexError:
                    pass
                
                quads.append(quad_vertices)

    # for xAlignedPoints in points:
    #     for point in xAlignedPoints:
    #         batch.add(
    #             1,GL_POINTS,None,
    #             ('c3B', (color[0],color[1],color[2])),
    #             ('v3f',(point[0],point[1],point[2]))
    #         )

    for quad in quads:
        batch.add(
            4,GL_QUADS,None,
            ('c3B', (color[0],color[1],color[2])),
            ('v3f',tuple(quad))
        )