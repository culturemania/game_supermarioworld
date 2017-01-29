__author__ = 'ESTEBAN'

import pygame
from pygame.locals import *
import random


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        self.position = Rect(x, y, w, h)

    def inscreen(self, level):
        return level.camera.rect.colliderect(self.position)

    def action(self, level, ticks):
        pass

    def draw(self, level):
        pass


class Drawable(Object):
    def __init__(self, image, x, y, w, h, nbframes=1, blitx=0, blity=0):
        Object.__init__(self, x, y, w, h)
        pygame.sprite.Sprite.__init__(self)
        self.surface = pygame.Surface((w, h))
        self.surface.set_colorkey(Color(255, 0, 255, 255), RLEACCEL)
        self.image = image
        self.nbframes = nbframes
        self.frame = 0
        self.lastupdateframe = pygame.time.get_ticks()
        self.updateframetime = random.randrange(50, 2000)
        self.blitx = blitx
        self.blity = blity
        self.active = True
        self.isalive = False
        self.value = 0

    def update(self, level):
        if self.inscreen(level) and self.nbframes > 1:
            self.updateframe(level)

    def updateframe(self, level):
        ticks = pygame.time.get_ticks()
        if ticks - self.lastupdateframe > self.updateframetime:
            self.lastupdateframe = ticks
            self.updateframetime = 50
            if self.frame == self.nbframes - 1:
                self.frame = 0
                self.updateframetime = 4000
            else:
                self.frame += 1

    def action(self, level, ticks):
        Object.action(self, level)
        level.mario.coins += self.value
        level.objects.remove(self)
        level.bonuses.remove(self)

    def draw(self, level):
        self.surface.blit(self.image, (0, 0), (self.frame*self.position.width + self.blitx, self.blity, self.position.width, self.position.height))
        xcam = level.camera.rect.left
        ycam = level.camera.rect.top
        screen = pygame.display.get_surface()
        screen.blit(self.surface, self.position.move(-xcam, -ycam))