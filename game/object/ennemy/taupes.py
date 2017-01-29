__author__ = 'Vincent'

from game.object.character import Character


class Taupe(Character):
    def __init__(self, image, x, y, w, h, nbframes):
        Character.__init__(self, image, x, y, w, h, nbframes, 0, 92)
        self.speed = 1
        self.score = 1000

    def update(self, game):
        #if math.fabs(game.mario.position.x - self.position.x) < 100:
        #    self.speed = 2
        #else:
        #    self.speed = 1
        Character.update(self, game)
