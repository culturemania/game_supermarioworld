__author__ = 'ESTEBAN'

import pygame
from drawable import Drawable
import random


class Cloud(Drawable):
    def __init__(self, assetfile, x, y, speed):
        Drawable.__init__(self, assetfile, x, y, 132, 78, 0, 108, 0)
        self.lastupdate = pygame.time.get_ticks()
        self.speed = -speed
        self.opacity = random.randint(20, 255)

    def update(self, level):
        ticks = pygame.time.get_ticks()
        if ticks - self.lastupdate > 1/self.speed*100:
            self.position = self.position.move(self.speed, 0)
            self.lastupdate = ticks
            if self.position.right < 0:
                self.position.left = max(level.mario.position.right,level.camera.rect.width/2)  + level.camera.rect.width/2
                speed = random.randint(1, 2)
                self.position.top = random.randint(-50, 250)

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



