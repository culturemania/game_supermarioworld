__author__ = 'ESTEBAN'

from level import Level
import os
from game.object.ennemy import *


class Castle(Level):
    def __init__(self, game, name):
        Level.__init__(self, game, name)
        self.speed = 1
        self.ytile = 16
        self.bgcolor = (96, 105, 120)

    def loadcontent(self):
        Level.loadcontent(self)

    def start(self, mario):
        Level.start(self, mario)
        musicfilepath = "game\\assets\\musics\\hautedhouse.mp3".format(self.name)
        if os.path.exists(musicfilepath):
            pygame.mixer.music.load(musicfilepath)
            pygame.mixer.music.play()

    def draw(self, game):
        game.screen.fill(self.bgcolor)
        self.fond.draw(self)
        Level.draw(self, game)


class Castle01(Castle):
    def __init__(self, game, name):
        Castle.__init__(self, game, name)

    def loadcontent(self):
        Level.loadcontent(self)

    def draw(self, game):
        game.screen.fill(self.bgcolor)
        Level.draw(self, game)

