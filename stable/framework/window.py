from pyglet.canvas import Display
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse

from framework.user_input import user
from engine.graphics import Model
from engine.physics import cosmos

import platform
from math import sqrt

userScreen = Display().get_default_screen()
screenWidth, screenHeight = userScreen.width, userScreen.height

class mainWindow(pyglet.window.Window):
    def push(self,pos,rot): 
        glPushMatrix()
        glRotatef(-rot[0],1,0,0); glRotatef(-rot[1],0,1,0)
        glTranslatef(-pos[0],-pos[1],-pos[2],)

    def Projection(self): 
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    def Model(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set3d(self): 
        self.Projection()
        gluPerspective(70,self.width/self.height,0.05,1000)
        self.Model()

    def setLock(self,state): self.lock = state; self.set_exclusive_mouse(state)
    lock = False; inputLock = property(lambda self:self.lock,setLock)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)

        glClearColor(0.04, 0.07, 0.17, 1)
        glEnable(GL_DEPTH_TEST)
        glLineWidth(3)
        glEnable(GL_LINE_SMOOTH)

        self.set_minimum_size(int(screenWidth*0.4), int(screenHeight*0.4))

        self.keydowns = []
        self.model = Model()
        self.user = user(pos=(175,125,200))

        self.updating = False
        pyglet.clock.schedule(self.update)
        if self.updating == True:
            pyglet.clock.schedule(cosmos.update)
    
    def update(self,dt):
        self.user.keyStateUpdate(dt, self.keys)

    def on_key_press(self,KEY,MOD):
        if KEY == key.P:
            if self.updating == False:
                pyglet.clock.schedule(cosmos.update)
                self.updating = True
            else:
                pyglet.clock.unschedule(cosmos.update)
                self.updating = False

        if KEY == key.F1:
            print('POSITION:             ' + str(self.user.pos))
            print('VIEW ANGLE:           ' + str(self.user.rot))
            print('DISTANCE FROM ORIGIN: ' + str(
                sqrt(self.user.pos[0]**2 + self.user.pos[1]**2 + self.user.pos[2]**2)
            ))

        if KEY == key.Q: self.close()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons == mouse.LEFT:
            self.user.cam_rotate(dx*0.2,dy*0.2)
        if buttons == mouse.RIGHT:
            self.user.manual_change(dx = dx*0.01, dy = dy*0.01)
            self.user.move_update()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if scroll_y:
            self.user.zoom(1 + (-scroll_y / 10))

    def on_draw(self):
        self.clear()
        self.set3d()
        self.push(self.user.pos,self.user.rot)

        self.model.draw()

        glPopMatrix()
        glFlush()

    def on_resize(self, width, height):
        if platform.system() == 'Darwin':
            glViewport(0, 0, int(width*2), int(height*2))
        else:
            glViewport(0, 0, int(width), int(height))