__author__ = 'ESTEBAN'

import pygame
from pygame.locals import *
from datetime import datetime


class State:
    def __init__(self):
        self.image = pygame.image.load("game\\assets\\sprites\\menu.bmp").convert_alpha()
        self.surfacecoin = pygame.Surface((16, 16))
        self.surfacecoin.set_colorkey(Color(255, 0, 255, 255), RLEACCEL)
        self.surfaceyoshicoin = pygame.Surface((16, 25))
        self.surfaceyoshicoin.set_colorkey(Color(255, 0, 255, 255), RLEACCEL)
        self.surfacelife = pygame.Surface((16, 16))
        self.surfacelife.set_colorkey(Color(255, 0, 255, 255), RLEACCEL)
        self.surfaceenergy = pygame.Surface((16, 16))
        self.surfaceenergy.set_colorkey(Color(255, 0, 255, 255), RLEACCEL)
        self.screenfont = pygame.font.SysFont("Segoe Print", 12, True)
        self.screenfontsmall = pygame.font.SysFont("Segoe Print", 10, True)

        self.imagelogo = pygame.image.load("game\\assets\\sprites\\logo.bmp").convert_alpha()
        self.surfacelogo = pygame.Surface((194, 66))
        self.surfacelogo .set_colorkey(Color(255, 0, 255, 255), RLEACCEL)
        self.surfacelogo.blit(self.imagelogo, (0, 0), (0, 0, 194, 66))

    def draw(self, level):
        textcolor = (40, 40, 40)
        self.surfacecoin.blit(self.image, (0, 0), (0, 0, 16, 16))
        self.surfacelife.blit(self.image, (0, 0), (0, 16, 16, 16))
        self.surfaceyoshicoin.blit(self.image, (0, 0), (0, 32, 16, 28))
        self.surfaceenergy.blit(self.image, (0, 0), (0, 57, 16, 16))
        screen = pygame.display.get_surface()
        y = 10
        screen.blit(self.surfacelife, (16, y))
        label = self.screenfont.render(" x {}".format(level.mario.life), 1, textcolor)
        screen.blit(label, (32, y))

        screen.blit(self.surfacecoin, (16, y+20))
        label = self.screenfont.render(" x {}".format(level.mario.coins), 1, textcolor)
        screen.blit(label, (32, y+20))

        for i in range(0, level.mario.energy):
            screen.blit(self.surfaceenergy, (16 + i*16, y+40))

        screen.blit(self.surfaceyoshicoin, (570, y))
        label = self.screenfont.render(" x {}".format(level.mario.yoshicoins), 1, textcolor)
        screen.blit(label, (586, y))

        label = self.screenfont.render("Score : {}".format(level.mario.score), 1, textcolor)
        screen.blit(label, (300, y))

        elapsedtime = (datetime.utcnow() - level.starttime).total_seconds()
        value = int(level.timelimit - elapsedtime)
        if value < 30:
            label = self.screenfontsmall.render("Time : {}s".format(value), 1, (200, 0, 0))
        else:
            label = self.screenfontsmall.render("Time : {}s".format(value), 1, textcolor)
        screen.blit(label, (300, y+20))

    def drawtransition(self, game):
        screen = pygame.display.get_surface()
        screen.fill((0, 0, 0))
        screen.blit(self.surfacelogo, (game.width/2-self.surfacelogo.get_width()/2, game.height/2-self.surfacelogo.get_height()/2))
        label = self.screenfont.render("Level {}".format(game.levelidx), 1, (255, 255, 255))
        screen.blit(label, (300, 300))
        pygame.display.flip()