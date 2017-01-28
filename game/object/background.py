__author__ = 'ESTEBAN'

from character import Character
from drawable import Drawable
import pygame


class Background(Drawable):
    def __init__(self, image, x, y, blitx, blity, w, h, nbframes, zindex):
        Drawable.__init__(self, image, x, y, w, h, nbframes, blitx, blity)
        self.zindex = zindex

    def draw(self, level):
        self.surface.blit(self.image, (0, 0), (self.frame*self.position.width + self.blitx, self.blity, self.position.width, self.position.height))

        xcam = level.camera.rect.left / self.zindex
        ycam = level.camera.rect.top
        screen = pygame.display.get_surface()
        pos = self.position.move(-xcam, -ycam)
        for i in range(0, len(level.tilemap[0])*16/self.position.width):
            screen.blit(self.surface, pos)
            pos.x += self.position.width