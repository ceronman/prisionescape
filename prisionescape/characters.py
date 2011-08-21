from prisionescape import configuration
from prisionescape.geometry import Rectangle, Vector, Side
from pyglet.gl.gl import GL_POINTS, glColor4f
from pyglet.graphics import Batch, draw
from pyglet.resource import image
from pyglet.sprite import Sprite
from pyglet.window import key
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
        Side.LEFT:  ['prisioner_left_1.png',
                     'prisioner_left_2.png',
                     'prisioner_left_push.png'],

        Side.RIGHT: ['prisioner_right_1.png',
                     'prisioner_right_2.png',
                     'prisioner_right_push.png'],

        Side.DOWN:  ['prisioner_front_1.png',
                     'prisioner_front_2.png',
                     'prisioner_front_push.png'],

        Side.UP:    ['prisioner_back_1.png',
                     'prisioner_back_2.png',
                     'prisioner_back_push.png']
    }

    SCROLL_MARGIN = 100

    def __init__(self, map):
        super(Prisioner, self).__init__(map)

        self._load_images()
        self.speed = 5
        self.step = 0
        self.frame_steps = itertools.cycle([0] * 10 + [1] * 10)
        self.side = Side.DOWN
        self.pushing = False
        self.sprite = Sprite(self.images[Side.DOWN][0], batch=Prisioner.batch)

        self.rect.go_to(40, 40)
        self._adjust_rectangle()
        self._update_frame()

    def update(self, window):
        direction = Vector(0, 0)
        if window.keys[key.LEFT]:
            direction.x = -1
            self.side = Side.LEFT
            self._update_step()
        if window.keys[key.RIGHT]:
            direction.x = 1
            self.side = Side.RIGHT
            self._update_step()
        if window.keys[key.UP]:
            direction.y = 1
            self.side = Side.UP
            self._update_step()
        if window.keys[key.DOWN]:
            direction.y = -1
            self.side = Side.DOWN
            self._update_step()
        if window.keys[key.LSHIFT] or window.keys[key.RSHIFT]:
            self.speed = 2
        else:
            self.speed = 4
        self.pushing = bool(window.keys[key.SPACE])

        self._update_frame()
        if direction != Vector(0, 0):
            direction = direction * self.speed
            self.rect.move(direction.x, direction.y)
            self._check_map_collision(direction.x, direction.y)
            self._adjust_rectangle()
            self._update_camera(window)

    def _check_map_collision(self, direction_x, direction_y):
        rect = self.rect
        speed = self.speed
        if direction_x > 0:
            tile1 = self.map.get_tile_at(rect.right + 1, rect.top - speed)
            tile2 = self.map.get_tile_at(rect.right + 1, rect.center.y)
            tile3 = self.map.get_tile_at(rect.right + 1, rect.bottom + speed)
            tile = self.map.get_solid_tiles([tile1, tile2, tile3])
            if tile is not None:
                rect.right = tile.rect.left - 1
        if direction_x < 0:
            tile1 = self.map.get_tile_at(rect.left - 1, rect.top - speed)
            tile2 = self.map.get_tile_at(rect.left - 1, rect.center.y)
            tile3 = self.map.get_tile_at(rect.left - 1, rect.bottom + speed)
            tile = self.map.get_solid_tiles([tile1, tile2, tile3])
            if tile is not None:
                rect.left = tile.rect.right + 1
        if direction_y < 0:
            tile1 = self.map.get_tile_at(rect.left + speed, rect.bottom - 1)
            tile2 = self.map.get_tile_at(rect.right - speed, rect.bottom - 1)
            tile = self.map.get_solid_tiles([tile1, tile2])
            if tile is not None:
                rect.bottom = tile.rect.top + 1
        if direction_y > 0:
            tile1 = self.map.get_tile_at(rect.left + speed, rect.top + 1)
            tile2 = self.map.get_tile_at(rect.right - speed, rect.top + 1)
            tile = self.map.get_solid_tiles([tile1, tile2])
            if tile is not None:
                rect.top = tile.rect.bottom - 1

    def _update_frame(self):
        step = self.step if not self.pushing else 2
        self.sprite.image = self.images[self.side][step]

    def _update_step(self):
        self.step = next(self.frame_steps)

    def _update_camera(self, window):
        if (self.rect.left - window.camera_rect.left) < self.SCROLL_MARGIN:
            window.camera_rect.left = self.rect.left - self.SCROLL_MARGIN

        if (window.camera_rect.right - self.rect.right) < self.SCROLL_MARGIN:
            window.camera_rect.right = self.rect.right + self.SCROLL_MARGIN

        if (self.rect.bottom - window.camera_rect.bottom) < self.SCROLL_MARGIN:
            window.camera_rect.bottom = self.rect.bottom - self.SCROLL_MARGIN

        if (window.camera_rect.top - self.rect.top) < self.SCROLL_MARGIN:
            window.camera_rect.top = self.rect.top + self.SCROLL_MARGIN

    def _load_images(self):
        self.images = {}
        for category, files in self.frame_files.iteritems():
            self.images[category] = [image(file) for file in files]
