__author__ = 'ESTEBAN'

import pygame
from drawable import Drawable
from game.tools import Vector2
import random
from asset import Tumb, Impact


class Character(Drawable):
    def __init__(self, image, x, y, w, h, nbframes, blitx, blity):
        Drawable.__init__(self, image, x, y, w, h, nbframes, blitx, blity)
        self.speed = 1
        self.originalspeed = 1
        self.upspeed = 0
        self.gravity = 6
        self.speedy = 0
        self.life = 1
        self.direction = Vector2(-1, 0)
        self.updateframetime = 200
        self.lastupdatejump = pygame.time.get_ticks()
        self.ismoving = False
        self.randomevent = random.randint(1000, 5000)
        self.score = 1
        self.isattacking = False
        self.isdying = False

    def ckeckblockscollision(self, level):
        for block in level.blocks:
            if self.position.colliderect(block):
                return True

    def jump(self, value, ticks):
        self.lastupdatejump = ticks
        self.speedy = value
        self.direction.y = 1
        self.ismoving = True

    def update(self, level):
        Drawable.update(self, level)
        ticks = pygame.time.get_ticks()
        if self.isdying is True:
            self.position = self.position.move(0, 5)
            if self.position.y > level.camera.rect.height:
                level.objects.remove(self)
        else:
            if self.isattacking:
                if level.mario.position.x < self.position.x:
                    self.direction.x = -1
                else:
                    self.direction.x = 1

            lastposition = self.position
            self.position = self.position.move(self.direction.x * self.speed, self.direction.y)
            if self.ckeckblockscollision(level) is True:
                if self.isattacking is True:
                    self.position = lastposition
                else:
                    self.direction.x *= -1

            if self.position.left <= 0 or self.position.right >= len(level.tilemap[0]) * 16:
                self.direction.x *= -1

            self.apply_physics(level, ticks)

    def updateframe(self, level):
        if self.isdying:
            return

        ticks = pygame.time.get_ticks()
        if ticks - self.lastupdateframe > self.updateframetime:
            self.lastupdateframe = ticks
            if self.direction.x >= 0:
                if self.frame == self.nbframes*2-1:
                    self.frame = 2
                else:
                    self.frame += 1
            else:
                if self.frame >= self.nbframes - 1:
                    self.frame = 0
                else:
                    self.frame += 1

    def apply_physics(self, level, ticks):
        # level limits
        if self.position.left <= 0:
            self.position.left = 0
        if self.position.right > (len(level.tilemap[0])) * 16:
            self.position.right = (len(level.tilemap[0])) * 16

        self.position = self.position.move(0, self.speedy + self.gravity)
        if self.speedy != 0 and ticks - self.lastupdatejump > 100:
            # on ralentit l'ascension
            self.lastupdatejump = ticks
            self.speedy += 2

        x = self.position.left + self.position.width/2
        plateforms = filter(lambda p: abs((p.rect.left+p.rect.width/2) - self.position.left) < (p.rect.width + self.position.width)
        and abs((p.rect.top+p.rect.height/2) - self.position.top) < (p.rect.height + self.position.height) , level.platforms)

        for g in range(-self.gravity - self.speed-1, 0):
            y = self.position.bottom + g
            if (self.speedy + self.gravity) <= 0:
                return

            for plateform in plateforms:
                if plateform.type == 666:
                    if (self.speedy + self.gravity) > 0 and abs(plateform.rect.top - self.position.bottom) <= (self.gravity + 5):
                        if self.position.right > plateform.rect.left and self.position.left <= plateform.rect.right:
                            self.position.bottom = plateform.rect.top
                            self.direction.y = 0
                            self.speed = self.originalspeed
                            return

                if plateform.type == 15:
                    if plateform.rect.inflate(1, 1).collidepoint(x, y):
                        offsetX = x - plateform.rect.left
                        self.position.bottom = plateform.rect.bottom - offsetX
                        self.direction.y = 0
                        if self.direction.x > 0:
                            self.speed = max(1, self.originalspeed - 1)
                        else:
                            self.speed = self.originalspeed + 1
                        return
                elif plateform.type == 27:
                    if plateform.rect.inflate(1, 1).collidepoint(x, y):
                        offsetX = x - plateform.rect.left
                        self.position.bottom = plateform.rect.bottom - 16 + offsetX
                        self.direction.y = 0
                        if self.direction.x < 0:
                            self.speed = max(1, self.originalspeed - 1)
                        else:
                            self.speed = self.originalspeed + 1
                        return
                else:
                    if (self.speedy + self.gravity) > 0 and abs(plateform.rect.top - self.position.bottom) <= (self.gravity + 1):
                        if self.position.right > plateform.rect.left and self.position.left <= plateform.rect.right:
                            self.position.bottom = plateform.rect.top
                            self.direction.y = 0
                            self.speed = self.originalspeed
                            return

    def action(self, level):
        level.mario.score += self.score
        self.life -= level.mario.power
        if self.life <= 0:
            self.isdying = True
            level.playsound('turtle')
            self.frame = self.nbframes*2
            #obj = Tumb(level.imageSprites, self.position.left, self.position.bottom-48, 23, 48, 9)
            obj = Impact(level.imageSprites, self.position.left+self.position.width/2, self.position.top)
            level.objects.insert(0, obj)
