__author__ = 'ESTEBAN'
from level import Level
import pygame


class WorldMap(Level):
    def __init__(self, game, name):
        Level.__init__(self, game, name)
        self.speed = 1

    def loadcontent(self):
        pass

    def update(self):
        pass

    def draw(self, game):
        game.screen.fill((0, 116, 166))
        self.drawtilemap(game)
        pygame.display.flip()