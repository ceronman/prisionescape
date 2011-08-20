from pyglet import resource


DEBUG = True


def configure():
    resource.path.append(u'data')
    resource.reindex()
