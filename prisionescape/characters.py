from prisionescape.geometry import Position
from pyglet.resource import image
from pyglet.graphics import Batch
from pyglet.sprite import Sprite


class Character(object):

    batch = Batch()

    def __init__(self):
        self.position = Position()
        self.sprite = None

    def draw(self):
        self.sprite.draw()

    def update(self):
        pass


class Prisioner(Character):

    images = [image('prisioner0.png')]

    def __init__(self):
        super(Prisioner, self).__init__()

        self.sprite = Sprite(Prisioner.images[0])
