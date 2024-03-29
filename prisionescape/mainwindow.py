from prisionescape.tilemap import LevelMap
from pyglet import clock, gl
from pyglet.window import Window, key
from prisionescape.characters import Prisioner
from pyglet.gl.gl import GL_MODELVIEW, glMatrixMode, glLoadIdentity,\
    glTranslatef
from prisionescape.geometry import Rectangle


class MainWindow(Window):

    def __init__(self):
        super(MainWindow, self).__init__(800, 600)
        self.set_caption(u'Pyglet Test')
        gl.glClearColor(0.5, 0.5, 0.5, 255)

        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)

        self.camera_rect = Rectangle(0, 0, self.width, self.height)

        clock.schedule_interval(self.update, 1.0/60)
        self.map = LevelMap()
        self.prisioner = Prisioner(self.map)

    def update(self, dt):
        self.prisioner.update(self)

    def on_draw(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(-self.camera_rect.x, -self.camera_rect.y, 0)
        self.clear()
        self.map.draw()
        self.prisioner.draw()
