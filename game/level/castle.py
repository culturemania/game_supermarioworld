__author__ = 'ESTEBAN'
from level import Level


class Castle(Level):
    def __init__(self, game, name):
        Level.__init__(self, game, name)
        self.speed = 1
        self.ytile = 16
        self.bgcolor = (96, 105, 120)

    def loadcontent(self):
        Level.loadcontent(self)


class Castle01(Castle):
    def __init__(self, game, name):
        Castle.__init__(self, game, name)

    def loadcontent(self):
        Level.loadcontent(self)

    def draw(self, game):
        game.screen.fill(self.bgcolor)
        Level.draw(self, game)

