from prisionescape import configuration
from prisionescape.geometry import Rectangle
from pyglet.graphics import Batch, draw
from pyglet.resource import image
from pyglet.sprite import Sprite
from pyglet.window import key
from pyglet.gl.gl import GL_POINTS, glColor4f


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


    def __init__(self, map):
        super(Prisioner, self).__init__(map)

        self.sprite = Sprite(image('prisioner0.png'),
                             batch=Character.batch)

        self.speed = 3

        self.rect.go_to(40, 40)
        self._adjust_rectangle()

    def update(self, window):
        direction_x = 0
        direction_y = 0
        if window.keys[key.LEFT]:
            direction_x = -1
        if window.keys[key.RIGHT]:
            direction_x = 1
        if window.keys[key.UP]:
            direction_y = 1
        if window.keys[key.DOWN]:
            direction_y = -1

        if (direction_x, direction_y) != (0, 0):
            self.rect.move(direction_x * self.speed, direction_y * self.speed)
            self._check_map_collision(direction_x, direction_y)
            self._adjust_rectangle()

    def _check_map_collision(self, direction_x, direction_y):
        rect = self.rect
        speed = self.speed
        if direction_x > 0:
            tile1 = self.map.get_tile_at(rect.right + 1, rect.top - speed)
            tile2 = self.map.get_tile_at(rect.right + 1, rect.bottom + speed)
            tile = tile1 or tile2
            if tile is not None:
                rect.right = tile.rect.left - 1
        if direction_x < 0:
            tile1 = self.map.get_tile_at(rect.left - 1, rect.top - speed)
            tile2 = self.map.get_tile_at(rect.left - 1, rect.bottom + speed)
            tile = tile1 or tile2
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

