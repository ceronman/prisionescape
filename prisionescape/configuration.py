from pyglet import resource


def configure():
    resource.path.append(u'data')
    resource.reindex()
