from prisionescape.geometry import Rectangle
from pyglet.graphics import Batch
from pyglet.resource import image
from pyglet.sprite import Sprite
from pyglet.window import key


class Character(object):

    batch = Batch()

    def __init__(self, map):
        self.rect = Rectangle()
        self.map = map
        self._sprite = None

    def draw(self):
        self.sprite.draw()

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, sprite):
        self._sprite = sprite
        self.rect.x = sprite.x
        self.rect.y = sprite.y
        self.rect.width = sprite.width
        self.rect.height = sprite.height

    def _adjust_rectangle(self):
        self.sprite.position = self.rect.topleft.xy


class Prisioner(Character):


    def __init__(self, map):
        super(Prisioner, self).__init__(map)

        self.sprite = Sprite(image('prisioner0.png'),
                             batch=Character.batch)

        self.speed = 3

        self.rect.go_to(40, 40)
        self._adjust_rectangle()

    def update(self, window):
        pass


