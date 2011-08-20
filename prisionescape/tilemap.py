from prisionescape.geometry import Position, Rectangle
from pyglet import resource
from pyglet.graphics import Batch
from pyglet.sprite import Sprite


class Tile(Sprite):

    def __init__(self, image, batch):
        super(Tile, self).__init__(image, batch=batch)

    @property
    def rect(self):
        return Rectangle(self.x, self.y, self.width, self.height)


class TileMap(object):

    def __init__(self):
        self._batch = Batch()
        self.tile_images = []
        self.tiles = []
        self.tile_width = 0
        self.tile_height = 0
        self.camera_position = Position()

    def load_tiles(self, *args):
        self.tile_images = []
        for path in args:
            image = resource.image(path)
            self.tile_images.append(image)

        self.tile_width = max(image.width for image in self.tile_images)
        self.tile_height = max(image.height for image in self.tile_images)

    def load_from_string(self, map):
        self.tiles = []

        for line in reversed(map.splitlines()):
            tile_line = []
            for char in line:
                if char.isdigit():
                    image = self.tile_images[int(char)]
                    tile = Tile(image=image, batch=self._batch)
                else:
                    tile = None
                tile_line.append(tile)
            self.tiles.append(tile_line)

        self.set_camera_position(0, 0)

    def draw(self):
        self._batch.draw()

    def set_camera_position(self, x, y):
        self.camera_position.set(x, y)
        self._adjust_position()

    def move_camera(self, x, y):
        self.camera_position.move(x, y)
        self._adjust_position()

    def get_tile_at(self, x, y):
        tile_x = x / self.tile_width
        tile_y = y / self.tile_height
        return self.tiles[tile_y][tile_x]

    def _adjust_position(self):
        x, y = self.camera_position.xy
        for pos_y, line in enumerate(self.tiles):
            for pos_x, tile in enumerate(line):
                if tile is not None:
                    tile.x = pos_x * self.tile_width - x
                    tile.y = pos_y * self.tile_height - y


class LevelMap(TileMap):

    def __init__(self):
        super(LevelMap, self).__init__()
        self.load_tiles(u'tile1.png', u'tile2.png', u'tile3.png')
        self.load_from_string(TEST_MAP)


TEST_MAP = """\
0000000000000000000000000000000000000000000000000000000000000000000000000000000
0                                                                             0
0                                                                             0
0                                                                             0
0    222222222222222222222222222222222222222222222222222222                   0
0                                                                             0
0    1      1   1   111   1   1 1     1                                       0
0    1      1   1   1  1  1   1 11   11                                       0
0    1      1   1   1  1  1   1 1 1 1 1                                       0
0    1      1   1   1  1  1   1 1  1  1                                       0
0    1      1   1   1 1   1   1 1     1                                       0
0    11111  11111   11    11111 1     1                                       0
0                                                                             0
0                                                                             0
0                                                                             0
0000000000000000000000000000000000000000000000000000000000000000000000000000000
"""
