from prisionescape import configuration
from prisionescape.geometry import Rectangle, Vector
from pyglet.graphics import Batch, draw
from pyglet.resource import image
from pyglet.sprite import Sprite
from pyglet.window import key
from pyglet.gl.gl import GL_POINTS, glColor4f
import itertools


class Character(object):

    batch = Batch()

    def __init__(self, map):
        self.rect = Rectangle()
        self.map = map
        self._sprite = None

    def draw(self):
        self.sprite.draw()

        if configuration.DEBUG:
            glColor4f(1, 0, 0, 1)
            draw(4, GL_POINTS, ('v2i', self.rect.points))

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
        self.sprite.position = self.rect.bottomleft.xy


class Prisioner(Character):

    batch = Batch()

    frame_files = {
        'left':  ['prisioner_left_1.png',
                  'prisioner_left_2.png',
                  'prisioner_left_push.png'],

        'right': ['prisioner_right_1.png',
                  'prisioner_right_2.png',
                  'prisioner_right_push.png'],

        'down':  ['prisioner_front_1.png',
                  'prisioner_front_2.png',
                  'prisioner_front_push.png'],

        'up':    ['prisioner_back_1.png',
                  'prisioner_back_2.png',
                  'prisioner_back_push.png']
    }

    def __init__(self, map):
        super(Prisioner, self).__init__(map)

        self._load_images()
        self.sprite = Sprite(self.images['down'][1], batch=Prisioner.batch)
        self.speed = 3
        self.frame_step = itertools.cycle([0] * 10 + [1] * 10)

        self.rect.go_to(40, 40)
        self._adjust_rectangle()

    def update(self, window):
        direction = Vector(0, 0)
        pushing = False
        if window.keys[key.LEFT]:
            direction.x = -1
        if window.keys[key.RIGHT]:
            direction.x = 1
        if window.keys[key.UP]:
            direction.y = 1
        if window.keys[key.DOWN]:
            direction.y = -1
        if window.keys[key.SPACE]:
            pushing = True

        self._update_frame(direction, pushing)
        if direction != Vector(0, 0):
            direction = direction * self.speed
            self.rect.move(direction.x, direction.y)
            self._check_map_collision(direction.x, direction.y)
            self._adjust_rectangle()

    def _check_map_collision(self, direction_x, direction_y):
        rect = self.rect
        speed = self.speed
        if direction_x > 0:
            tile1 = self.map.get_tile_at(rect.right + 1, rect.top - speed)
            tile2 = self.map.get_tile_at(rect.right + 1, rect.center.y)
            tile3 = self.map.get_tile_at(rect.right + 1, rect.bottom + speed)
            tile = tile1 or tile2 or tile3
            if tile is not None:
                rect.right = tile.rect.left - 1
        if direction_x < 0:
            tile1 = self.map.get_tile_at(rect.left - 1, rect.top - speed)
            tile2 = self.map.get_tile_at(rect.left - 1, rect.center.y)
            tile3 = self.map.get_tile_at(rect.left - 1, rect.bottom + speed)
            tile = tile1 or tile2 or tile3
            if tile is not None:
                rect.left = tile.rect.right + 1
        if direction_y < 0:
            tile1 = self.map.get_tile_at(rect.left + speed, rect.bottom - 1)
            tile2 = self.map.get_tile_at(rect.right - speed, rect.bottom - 1)
            tile = tile1 or tile2
            if tile is not None:
                rect.bottom = tile.rect.top + 1
        if direction_y > 0:
            tile1 = self.map.get_tile_at(rect.left + speed, rect.top + 1)
            tile2 = self.map.get_tile_at(rect.right - speed, rect.top + 1)
            tile = tile1 or tile2
            if tile is not None:
                rect.top = tile.rect.bottom - 1

    def _update_frame(self, direction, pushing=False):
        side = None
        if direction.x > 0:
            side = 'right'
        if direction.x < 0:
            side = 'left'
        if direction.y > 0:
            side = 'up'
        if direction.y < 0:
            side = 'down'

        if side is not None:
            step = next(self.frame_step) if not pushing else 2
            self.sprite.image = self.images[side][step]

    def _load_images(self):
        self.images = {}
        for category, files in self.frame_files.iteritems():
            self.images[category] = [image(file) for file in files]
