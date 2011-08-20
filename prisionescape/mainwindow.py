from prisionescape.tilemap import LevelMap
from pyglet import clock
from pyglet.window import Window, key


class MainWindow(Window):

    def __init__(self):
        super(MainWindow, self).__init__(800, 600)
        self.set_caption(u'Pyglet Test')

        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)

        clock.schedule_interval(self.update, 1.0/60)
        self.map = LevelMap()

    def update(self, dt):
        if self.keys[key.LEFT]:
            self.map.move_camera(-1, 0)
        if self.keys[key.RIGHT]:
            self.map.move_camera(1, 0)
        if self.keys[key.UP]:
            self.map.move_camera(0, 1)
        if self.keys[key.DOWN]:
            self.map.move_camera(0, -1)

    def on_draw(self):
        self.clear()
        self.map.draw()
