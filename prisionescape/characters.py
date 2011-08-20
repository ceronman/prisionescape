from prisionescape.geometry import Position
from pyglet.graphics import Batch
from pyglet.resource import image
from pyglet.sprite import Sprite
from pyglet.window import key


class Character(object):

    batch = Batch()

    def __init__(self, map):
        self.position = Position()
        self.sprite = None
        self.map = map

    def draw(self):
        self.sprite.draw()

    def update(self, window):
        if window.keys[key.LEFT]:
            self.position.move(-1, 0)
        if window.keys[key.RIGHT]:
            self.position.move(1, 0)
        if window.keys[key.UP]:
            self.position.move(0, 1)
        if window.keys[key.DOWN]:
            self.position.move(0, -1)
        self._adjust_position()

    def _adjust_position(self):
        self.sprite.position = self.position.xy


class Prisioner(Character):


    def __init__(self, map):
        super(Prisioner, self).__init__(map)

        self.sprite = Sprite(image('prisioner0.png'),
                             batch=Character.batch)

        self.position.set(40, 40)
