__author__ = 'Vincent'
from game.object.character import Character
import pygame
import random


class Tortoise(Character):
    def __init__(self, image, x, y):
        Character.__init__(self, image, x, y, 16, 28, 2, 0, 64)
        self.speed = 1
        self.score = 200


class TortoiseJumpy(Character):
    def __init__(self, image, x, y):
        Character.__init__(self, image, x, y, 17, 28, 2, 0, 188)
        self.speed = 1
        self.score = 300

    def update(self, game):
        Character.update(self, game)
        ticks = pygame.time.get_ticks()
        if (ticks - self.lastupdatejump) > self.randomevent:
            self.lastupdateframe = ticks
            self.randomevent = random.randint(1000, 5000)
            if self.direction.y == 0:
                self.jump(-12, ticks)
