__author__ = 'Vincent'

from game.object.character import Character
import pygame
import random


class Goomba(Character):
    def __init__(self, image, x, y):
        Character.__init__(self, image, x, y, 16, 16, 2, 0, 576)
        self.speed = 1
        self.score = 200
        self.iswalking = True

    def update(self, game):
        ticks = pygame.time.get_ticks()
        if ticks - self.lastupdatejump > self.randomevent:
            self.randomevent = random.randint(100, 3000)
            self.lastupdatejump = ticks
            if self.iswalking:
                self.frame = 5
            elif self.direction.x > 0:
                self.frame = 2
            else:
                self.frame = 0
            self.iswalking = not self.iswalking

        if self.iswalking or self.isdying:
            Character.update(self, game)
