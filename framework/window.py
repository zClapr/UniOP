from pyglet.canvas import Display
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse

from framework.user_input import user
from engine.graphics import Model
from setup import active

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
        self.set_minimum_size(screenWidth*0.4, screenHeight*0.4)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)

        self.model = Model()
        self.user = user(pos=(5,5,-10),rot=(-30,150))

    def on_key_press(self,KEY,MOD):
        if KEY == key.Q: self.close()
        if KEY == key.FUNCTION: self.user.debug()
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        multi = 0.2
        if buttons == mouse.MIDDLE:
            self.user.cam_rotate(dx*multi,dy*multi)

    def update(self,dt):
        self.user.move(dt,self.keys)

    def on_draw(self):
        self.clear()
        self.set3d()
        self.push(self.user.pos,self.user.rot)

        self.model.draw() # includes all shapes
        glPopMatrix()
        glFlush()
    
    def on_resize(self, width, height):
        glViewport(0, 0, int(width*2), int(height*2))