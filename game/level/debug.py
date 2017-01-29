__author__ = 'Vincent'
from level import Level
from game.object import *

class DebugLevel(Level):
    def __init__(self, game, name):
        Level.__init__(self, game, name)
        self.speed = 1
        self.bgcolor = (120, 200, 225)

    def loadcontent(self):
        Level.loadcontent(self)
        obj = Asset(self.imageSprites, 160, 321, 43, 63, 345, 0)
        self.objects.append(obj)

        obj = Asset(self.imageSprites, 100, 257, 86, 128, 259, 0)
        self.objects.append(obj)

    def draw(self, game):
        game.screen.fill(self.bgcolor)
        Level.draw(self, game)
