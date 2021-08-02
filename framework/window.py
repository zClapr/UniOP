from pyglet.canvas import Display
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse

from framework.player import Player
from framework.display import Model
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
        self.player = Player((0.5,1.5,1.5),(-30,0))

    def on_mouse_motion(self,x,y,dx,dy):
        if self.inputLock: 
            self.player.mouse_motion(dx,dy)

    def on_key_press(self,KEY,MOD):
        if KEY == key.Q: self.close()
        elif KEY == key.ESCAPE and self.inputLock: self.inputLock = False
    
    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT and not self.inputLock: self.inputLock = True

    def update(self,dt):
        if self.inputLock:
            self.player.update(dt,self.keys)

    def on_draw(self):
        self.clear()
        self.set3d()
        self.push(self.player.pos,self.player.rot)

        self.model.draw() # includes all shapes
        glPopMatrix()
        glFlush()
    
    def on_resize(self, width, height):
        glViewport(0, 0, int(width*2), int(height*2))