__author__ = 'ESTEBAN'

from level import Level
import os
from game.object import *
from game.object.ennemy import *
from game.tools import Vector2
import random


class HauntedHouse(Level):
    def __init__(self, game, name):
        Level.__init__(self, game, name)
        self.speed = 1
        self.ytile = 32
        self.bgcolor = (8, 40, 56)

    def loadcontent(self):
        Level.loadcontent(self)
        self.imageBG = pygame.image.load("game\\assets\\sprites\\bghouse.bmp").convert_alpha()
        self.fond = Background(self.imageBG, 0, 0, 0, 0, 256, 434, 1, 2)

    def start(self, mario):
        Level.start(self, mario)
        musicfilepath = "game\\assets\\musics\\hautedhouse.mp3".format(self.name)
        if os.path.exists(musicfilepath):
            pygame.mixer.music.load(musicfilepath)
            pygame.mixer.music.play()

    def draw(self, game):
        game.screen.fill(self.bgcolor)
        self.fond.draw(self)
        Level.draw(self, game)


class HauntedHouse01(HauntedHouse):
    def __init__(self, game, name):
        HauntedHouse.__init__(self, game, name)

    def loadcontent(self):
        HauntedHouse.loadcontent(self)
        obj = RingGhost(self.imageSprites, 700, 250, 16, 100, Vector2(1, 0))
        self.objects.append(obj)
        self.ennemies.append(obj)

        for i in range(0, 0):
            obj = LittleGhost(self.imageSprites, random.randrange(0, 2000), random.randrange(0, 150))
            self.objects.append(obj)
            self.ennemies.append(obj)

        x = len(self.tilemap[0])*16 - 200 + 64
        obj = LevelEndBar(self.imageSprites, 100, 230, 1, (230, 352))
        self.objects.append(obj)
        self.bonuses.append(obj)

