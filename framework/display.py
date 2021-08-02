from pyglet.gl import *


class Model:

    def get_tex(self,file):
        tex = pyglet.image.load(file).get_texture()
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)

    def __init__(self):

        self.side = self.get_tex('./assets/dirt.png')

        self.batch = pyglet.graphics.Batch()

        tex_coords = ('t2f',(0,0, 1,0, 1,1, 0,1, ))

        x,y,z = 0,0,0
        X,Y,Z = x+1,y+1,z+1
        rx,ry,rz = 0,0,0

        self.batch.add(4,GL_QUADS,self.side,('v3f',(x,y,z, x,y,Z, x,Y,Z, x,Y,z, )),tex_coords)
        self.batch.add(4,GL_QUADS,self.side,('v3f',(X,y,Z, X,y,z, X,Y,z, X,Y,Z, )),tex_coords)
        self.batch.add(4,GL_QUADS,self.side,('v3f',(x,y,z, X,y,z, X,y,Z, x,y,Z, )),tex_coords)
        self.batch.add(4,GL_QUADS,self.side,('v3f',(x,Y,Z, X,Y,Z, X,Y,z, x,Y,z, )),tex_coords)
        self.batch.add(4,GL_QUADS,self.side,('v3f',(X,y,z, x,y,z, x,Y,z, X,Y,z, )),tex_coords)
        self.batch.add(4,GL_QUADS,self.side,('v3f',(x,y,Z, X,y,Z, X,Y,Z, x,Y,Z, )),tex_coords)


    def draw(self):
        self.batch.draw()