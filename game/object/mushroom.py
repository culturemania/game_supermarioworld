__author__ = 'ESTEBAN'

from character import Character
from game.tools import Vector2


class Mushroom(Character):
    def __init__(self, image, x, y):
        Character.__init__(self, image, x, y, 16, 16, 1, 0, 484)
        self.speed = 1
        self.value = 1
        self.direction = Vector2(1, 0)

    def update(self, game):
        Character.update(self, game)

    def action(self, level):
        level.mario.setBig(True)

        level.objects.remove(self)
        level.bonuses.remove(self)
