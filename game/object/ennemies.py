__author__ = 'ESTEBAN'

from character import Character
import pygame
import random
import math


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


class Tortoise(Character):
    def __init__(self, image, x, y):
        Character.__init__(self, image, x, y, 16, 28, 2, 0, 64)
        self.speed = 1
        self.score = 200

    def update(self, game):
        Character.update(self, game)


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


class Dragon(Character):
    def __init__(self, image, x, y):
        Character.__init__(self, image, x, y, 20, 32, 2, 0, 601)
        self.speed = 1
        self.score = 2000

    def update(self, game):
        Character.update(self, game)


class Ghost(Character):
    def __init__(self, image, x, y):
        Character.__init__(self, image, x, y, 67, 64, 1, 0, 124)
        self.speed = 1
        self.score = 5000

    def update(self, level):

        if level.mario.position.x < self.position.x:
            self.direction.x = -1
            self.frame = 0
        else:
            self.direction.x = 1
            self.frame = 1

        if level.mario.position.y < self.position.y:
            self.direction.y = -1
        else:
            self.direction.y = 1
        self.position = self.position.move(self.direction.x * self.speed, self.direction.y)

    def action(self, level):
        pass

    def blit_alpha(self, target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        target.blit(temp, location)

    def draw(self, level):
        self.surface.blit(self.image, (0, 0), (self.frame*self.position.width + self.blitx, self.blity, self.position.width, self.position.height))
        xcam = level.camera.rect.left
        ycam = level.camera.rect.top
        screen = pygame.display.get_surface()
        self.blit_alpha(screen, self.surface, self.position.move(-xcam, -ycam), 128)
