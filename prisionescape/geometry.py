class Vector(object):

    def __init__(self, x=0, y=0):
        self.set(x, y)

    def move(self, x, y):
        self.x += x
        self.y += y

    def set(self, x, y):
        self.x = x
        self.y = y

    @property
    def xy(self):
        return (self.x, self.y)

    def __eq__(self, vector):
        return (vector.x == self.x and vector.y == self.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __str__(self):
        return 'Vector: (%d, %d)' % self.xy

class Rectangle(object):

    def __init__(self, x=0, y=0, width=0, height=0):
        self.set(x, y, width, height)

    def set(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def move(self, x, y):
        self.x += x
        self.y += y

    def go_to(self, x, y):
        self.x = x
        self.y = y

    @property
    def points(self):
        return (self.left, self.top,
                self.right, self.top,
                self.right, self.bottom,
                self.left, self.bottom)


    def get_left(self):
        return self.x
    def set_left(self, left):
        self.x = left
    left = property(get_left, set_left)

    def get_right(self):
        return self.x + self.width
    def set_right(self, right):
        self.x = right - self.width
    right = property(get_right, set_right)

    def get_bottom(self):
        return self.y
    def set_bottom(self, bottom):
        self.y = bottom
    bottom = property(get_bottom, set_bottom)

    def get_top(self):
        return self.y + self.height
    def set_top(self, top):
        self.y = top - self.height
    top = property(get_top, set_top)

    @property
    def topleft(self):
        return Vector(self.left, self.top)

    @property
    def topright(self):
        return Vector(self.right, self.top)

    @property
    def bottomleft(self):
        return Vector(self.left, self.bottom)

    @property
    def bottomright(self):
        return Vector(self.right, self.bottom)

    @property
    def center(self):
        return Vector(self.x + self.width/2, self.y + self.height/2)

    @center.setter
    def center(self, x, y):
        self.x = x - self.width/2
        self.y = y - self.height/2


class Direction(object):

    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
