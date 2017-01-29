__author__ = 'Vincent'

from game.object.character import Character


class Dragon(Character):
    def __init__(self, image, x, y):
        Character.__init__(self, image, x, y, 20, 32, 2, 0, 600)
        self.speed = 1
        self.score = 2000

    def update(self, level):
        Character.update(self, level)
