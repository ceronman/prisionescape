from prisionescape.configuration import configure
from prisionescape.mainwindow import MainWindow
from pyglet.app import run


def start():
    configure()
    MainWindow()
    run()
