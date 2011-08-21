from prisionescape.geometry import Vector, Rectangle
from pyglet import resource
from pyglet.graphics import Batch
from pyglet.sprite import Sprite
import json


class Tile(Sprite):

    def __init__(self, image, batch):
        super(Tile, self).__init__(image, batch=batch)
        self.solid = True

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
        self.camera_position = Vector()

    def load_from_file(self, filename):
        mapfile = resource.file(filename)
        data = json.load(mapfile)

        self._load_images(data['images'])

        self.tiles = []
        for line in reversed(data['tiles']):
            tile_line = []
            for tile_number in line:
                image = self.tile_images[tile_number]
                tile = Tile(image=image, batch=self._batch)
                tile.solid = image.solid
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

    def get_solid_tiles(self, tiles):
        for tile in tiles:
            if tile.solid:
                return tile

    def _adjust_position(self):
        x, y = self.camera_position.xy
        for pos_y, line in enumerate(self.tiles):
            for pos_x, tile in enumerate(line):
                if tile is not None:
                    tile.x = pos_x * self.tile_width - x
                    tile.y = pos_y * self.tile_height - y

    def _load_images(self, tiles):
        self.tile_images = []
        for path, solid in tiles:
            image = resource.image(path)
            image.solid = solid
            self.tile_images.append(image)

        self.tile_width = max(image.width for image in self.tile_images)
        self.tile_height = max(image.height for image in self.tile_images)


class LevelMap(TileMap):

    def __init__(self):
        super(LevelMap, self).__init__()
        self.load_from_file('scene1.tiles')
