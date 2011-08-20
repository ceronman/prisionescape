class Position(object):

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


    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y + self.width()

    @property
    def topleft(self):
        return Position(self.left, self.top)

    @property
    def topright(self):
        return Position(self.right, self.top)

    @property
    def bottomleft(self):
        return Position(self.left, self.bottom)

    @property
    def bottomright(self):
        return Position(self.right, self.bottom)

    @property
    def center(self):
        return Position(self.x + self.width/2, self.y + self.height/2)

    @center.setter
    def center(self, x, y):
        self.x = x - self.width/2
        self.y = y - self.height/2
