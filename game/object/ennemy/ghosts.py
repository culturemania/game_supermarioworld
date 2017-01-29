__author__ = 'Vincent'
from game.object.character import Character
from game.object.drawable import Drawable
from pygame.locals import *
import pygame
import random
import math


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


class LittleGhost(Character):
    def __init__(self, image, x, y):
        Character.__init__(self, image, x, y, 16, 16, 2, 0, 632)
        self.speed = 1
        self.scared = False
        self.opacity = random.randrange(30, 255)
        self.updatetime = 25
        self.lastupdate = pygame.time.get_ticks()

    def update(self, level):
        ticks = pygame.time.get_ticks()
        if ticks - self.lastupdate > self.updatetime:
            self.lastupdate = ticks

            self.scared = False
            if level.mario.position.x < self.position.x:
                # mario a gauche
                if level.mario.direction.x > 0 and self.direction.x < 0:
                    self.frame = 0
                    self.scared = True
            else:
                if level.mario.direction.x < 0 and self.direction.x > 0:
                    self.scared = True
                    self.frame = 3

            if self.scared is False:
                # Il fonce vers mario

                if level.mario.position.y < self.position.y:
                    self.direction.y = -1
                else:
                    self.direction.y = 1
                if level.mario.position.x < self.position.x:
                    self.frame = 1
                    self.direction.x = -1
                else:
                    self.frame = 2
                    self.direction.x = 1
                self.position = self.position.move(self.direction.x * self.speed, self.direction.y)
            else:
                self.frame = 0

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
        self.blit_alpha(screen, self.surface, self.position.move(-xcam, -ycam), self.opacity)


class EvilGhost(Character):
    def __init__(self, image, x, y):
        Character.__init__(self, image, x, y, 16, 16, 1, 0, 648)
        self.speed = 1


class RingGhost(Drawable):
    def __init__(self, image, x, y, nbghosts, radius, direction):
        Drawable.__init__(self, image, x, y, 16, 16, 4, 0, 32)
        self.ghosts = []
        self.angle = 0.0
        self.radius = radius
        self.position = Rect(x, y, radius*2, radius*2)
        self.lastupdateframe = pygame.time.get_ticks()
        self.updateframetime = 10
        self.nbghosts = nbghosts
        self.direction = direction

        ghostsize = 16
        for i in range(nbghosts-2):
            obj = EvilGhost(image, self.position.centerx-ghostsize/2 + math.cos(self.angle) * radius, self.position.centery-ghostsize/2 - math.sin(self.angle) * radius)
            self.ghosts.append(obj)
            self.angle += (2*math.pi)/nbghosts

    def update(self, level):
        ticks = pygame.time.get_ticks()
        if ticks - self.lastupdateframe > self.updateframetime:
            self.lastupdateframe = ticks
            self.angle += 0.03*self.direction.x  # regle le speed
            ghostangle = self.angle
            for ghost in self.ghosts:
                ghost.position.x = self.position.centerx-8 + math.cos(ghostangle) * self.radius
                ghost.position.y = self.position.centery-8 - math.sin(ghostangle) * self.radius
                ghostangle += (2*math.pi)/self.nbghosts

    def draw(self, game):
        for ghost in self.ghosts:
            ghost.draw(game)

    def action(self, level, ticks):
        for ghost in self.ghosts:
            if level.mario.position.colliderect(ghost.position):
                level.mario.hurt(level, ghost.strength, ticks)
