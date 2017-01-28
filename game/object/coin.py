__author__ = 'ESTEBAN'

import pygame
from pygame.locals import *
from drawable import Drawable
from asset import CoinAdded
import math
import random

class YellowCoin(Drawable):
    def __init__(self, image, x, y):
        Drawable.__init__(self, image, x, y, 16, 16, 4, 0, 0)
        self.value = 1

    def action(self, level):
        level.playsound('yellowcoin')
        level.mario.coins += self.value
        level.objects.remove(self)
        level.bonuses.remove(self)


class GreenCoin(Drawable):
    def __init__(self, image, x, y):
        Drawable.__init__(self, image, x, y, 16, 16, 4, 0, 16)
        self.value = 3

    def action(self, level):
        level.playsound('yellowcoin')
        level.mario.coins += self.value
        level.objects.remove(self)
        level.bonuses.remove(self)


class RedCoin(Drawable):
    def __init__(self, image, x, y):
        Drawable.__init__(self, image, x, y, 16, 16, 4, 0, 32)
        self.value = 3

    def action(self, level):
        level.playsound('yellowcoin')
        level.mario.coins += self.value
        level.objects.remove(self)
        level.bonuses.remove(self)


class YoshiCoin(Drawable):
    def __init__(self, image, x, y):
        Drawable.__init__(self, image, x, y, 16, 25, 5, 0, 216)
        self.value = 1

    def action(self, level):
        level.playsound('dragoncoin')
        level.mario.yoshicoins += self.value
        level.objects.remove(self)
        level.bonuses.remove(self)


class YellowRingCoin(Drawable):
    def __init__(self, image, x, y, w, h, nbcoins, radius, direction, nbframes):
        Drawable.__init__(self, image, x, y, w, h, nbframes, 0, 32)
        self.coins = []
        self.position = Rect(x, y, radius*2, radius*2)
        self.angle = 0.0
        self.radius = radius
        self.lastupdateframe = pygame.time.get_ticks()
        self.updateframetime = 10
        self.nbcoins = nbcoins
        self.direction = direction

        coinsize = 16
        for i in range(nbcoins):
            obj = YellowCoin(image, self.position.centerx-coinsize/2 + math.cos(self.angle) * radius, self.position.centery-coinsize/2 - math.sin(self.angle) * radius)
            self.coins.append(obj)
            self.angle += (2*math.pi)/nbcoins

    def update(self, level):
        ticks = pygame.time.get_ticks()
        if ticks - self.lastupdateframe > self.updateframetime:
            self.lastupdateframe = ticks
            self.angle += 0.04*self.direction.x  # regle le speed
            coinangle = self.angle
            for coin in self.coins:
                if coin.active:
                    coin.position.x = self.position.centerx-8 + math.cos(coinangle) * self.radius
                    coin.position.y = self.position.centery-8 - math.sin(coinangle) * self.radius
                    coin.update(level)
                coinangle += (2*math.pi)/self.nbcoins

    def draw(self, game):
        for coin in self.coins:
            if coin.active is True:
                coin.draw(game)

    def action(self, level):
        for i in (range(len(self.coins))):
            coin = self.coins[i]
            if coin is not None and level.mario.position.colliderect(coin.position):
                if self.coins[i].active is True:
                    level.mario.coins += self.coins[i].value
                    level.playsound('yellowcoin')
                self.coins[i].active = False

        for coin in self.coins:
            if coin.active:
                return True
        level.playsound('dragoncoin')

        level.bonuses.remove(self)
        level.objects.remove(self)


class BlockCoin(Drawable):
    def __init__(self, image, x, y):
        Drawable.__init__(self, image, x, y, 16, 16, 4, 0, 48)
        self.value = 1
        self.coins = random.randrange(3, 10)
        self.yorigin = y
        self.jump = False

    def update(self, level):
        if self.jump is True:
            self.position.top -= 2
        if self.position.top < (self.yorigin - 10):
            self.position.top = self.yorigin
            self.jump = False

        self.updateframe(level)

    def updateframe(self, level):
        if self.coins > 0:
            Drawable.updateframe(self, level)
        else:
            self.frame = 4

    def action(self, level):
        Xcenter = level.mario.position.left + level.mario.position.width/2
        if self.position.left <= Xcenter <= self.position.right:
            if self.coins > 0:
                self.jump = True
                level.mario.coins += self.value
                level.playsound('yellowcoin')
                self.coins -= 1
                obj = CoinAdded(self.image, self.position.left, self.position.top-16)
                level.objects.append(obj)







