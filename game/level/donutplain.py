__author__ = 'ESTEBAN'

from level import Level
import random
from game.object import *
from game.tools import Vector2
from level import TILESIZE


class DebugLevel(Level):
    def __init__(self, game, name):
        Level.__init__(self, game, name)
        self.speed = 1

    def loadcontent(self):
        Level.loadcontent(self)

        for i in range(0, 10):
            obj = Goomba(self.imageSprites, 300 + i*50, 200)
            self.objects.append(obj)
            self.ennemies.append(obj)


class DonutPlain(Level):
    def __init__(self, game, name):
        Level.__init__(self, game, name)
        self.speed = 1
        self.bgcolor = (40, 60, 85)

    def loadcontent(self):
        Level.loadcontent(self)
        self.imageBG = pygame.image.load("game\\assets\\sprites\\backgroundhd.bmp").convert_alpha()
        self.fond = Background(self.imageBG, 0, 0, 0, 0, 874, 363, 1, 2)
        #self.fond2 = Background(self.imageBG, 0, 250, 0, 133, 256, 120, 1, 3)

    def draw(self, game):
        game.screen.fill(self.bgcolor)
        #self.fond2.draw(self)
        self.fond.draw(self)
        Level.draw(self, game)


class DonutPlain00(DonutPlain):
    def __init__(self, game, name):
        DonutPlain.__init__(self, game, name)
        self.speed = 1

    def loadcontent(self):
        DonutPlain.loadcontent(self)

        x = len(self.tilemap[0])*16 - 200
        obj = LevelEndBar(self.imageSprites, x, 192, 1, (192, 352))
        self.objects.append(obj)
        self.bonuses.append(obj)

        obj = YellowRingCoin(self.imageSprites, 200, 200, 16, 16, 10, 50, Vector2(-1, 0), 4)
        self.objects.append(obj)
        self.bonuses.append(obj)

        obj = Ghost(self.imageSprites, 1800, 100)
        self.objects.append(obj)
        self.ennemies.append(obj)

        for i in range(0, 5):
            x = random.randint(0, 1000)
            y = random.randint(-50, 250)
            speed = random.randint(1, 2)
            obj = Cloud(self.imageSprites, x, y, speed)
            self.topobjects.append(obj)


class DonutPlain01(DonutPlain):
    def __init__(self, game, name):
        DonutPlain.__init__(self, game, name)
        self.speed = 1

    def loadcontent(self):
        DonutPlain.loadcontent(self)
        for i in range(0, 5):
            x = random.randint(0, 1000)
            y = random.randint(-50, 250)
            speed = random.randint(1, 2)
            obj = Cloud(self.imageSprites, x, y, speed)
            self.topobjects.append(obj)

        obj = LevelEndBar(self.imageSprites, 1500, 240, 1, (240, 390))
        self.objects.append(obj)
        self.bonuses.append(obj)

        obj = YellowRingCoin(self.imageSprites, 480, 200, 16, 16, 16, 50, Vector2(1, 0), 4)
        self.objects.append(obj)
        self.bonuses.append(obj)

        obj = YellowRingCoin(self.imageSprites, 430, 150, 16, 16, 32, 100, Vector2(-1, 0), 4)
        self.objects.append(obj)
        self.bonuses.append(obj)

        for i in range(0, 3):
            obj = BlockCoin(self.imageSprites, 160 + i*16, 316, 16, 16, 4)
            self.objects.append(obj)
            self.bonuses.append(obj)
            self.objects.append(obj)
            self.platforms.append(Plateform(obj.position, 1))
            self.blocks.append(obj.position)

        for i in range(1, 1):
            if i % 3 == 0:
                obj = TortoiseJumpy(self.imageSprites, 200+i*16, 300)
            elif i % 2 == 0:
                obj = Tortoise(self.imageSprites, 50+i*16, 300)
            else:
                obj = Taupe(self.imageSprites, 1000+i*100, 300, 32, 32, 2)
            self.objects.append(obj)
            self.ennemies.append(obj)


class DonutPlain02(DonutPlain):
    def __init__(self, game, name):
        DonutPlain.__init__(self, game, name)
        self.speed = 1

    def loadcontent(self):
        DonutPlain.loadcontent(self)
        ground = 25*16

        for i in range(0, 100):
            x = random.randrange(0, 100)
            y = random.randrange(18, 22)

            if x % 2 == 0:
                obj = YellowCoin(self.imageSprites, 300 + x*16, y*16)
            elif x % 3 == 0:
                obj = GreenCoin(self.imageSprites, 300 + x*16, y*16)
            else:
                obj = RedCoin(self.imageSprites, 300 + x*16, y*16)
            self.objects.append(obj)
            self.bonuses.append(obj)

    def updatecamera(self):
        if self.camera.rect.right < len(self.tilemap[0]) * TILESIZE - self.camera.rect.width / 2:
            self.camera.rect.centerx += self.speed
            if self.camera.rect.centerx > 500:
                self.speed = 2
            if self.camera.rect.centerx > 700:
                self.speed = 3


class DonutPlain03(DonutPlain):
    def __init__(self, game, name):
        DonutPlain.__init__(self, game, name)
        self.speed = 1

    def loadcontent(self):
        DonutPlain.loadcontent(self)
        for i in range(0, 20):
            obj = Taupe(self.imageSprites, 200 + 50*i, 100, 32, 32, 2)
            self.objects.append(obj)
            self.ennemies.append(obj)
