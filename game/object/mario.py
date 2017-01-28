__author__ = 'ESTEBAN'

import pygame
from pygame.locals import *
from character import Character
from game.tools import Message
from game.tools import Vector2


class Mario(Character):
    def __init__(self, image, x, y, w, h, nbframes):
        Character.__init__(self, image, x, y, w, h, nbframes, 0, 59)

        self.speed = 2
        self.originalspeed = 2
        self.power = 1
        self.frame = 4
        self.direction = Vector2(0, 0)
        self.lastdirection = Vector2(0, 0)
        self.coins = 0
        self.yoshicoins = 0
        self.life = 5
        self.energy = 3
        self.score = 0
        self.ishurt = False
        self.lasthurttime = pygame.time.get_ticks()
        self.bdraw = True
        self.isbig = False
        self.lastkeys = pygame.key.get_pressed()

    def update(self, level):
        keys = pygame.key.get_pressed()
        ticks = pygame.time.get_ticks()

        if self.ishurt and (ticks - self.lasthurttime) > 1000:
            self.lasthurttime = ticks
            self.ishurt = False
            print "hurt = false"

        self.lastdirection.x = self.direction.x
        self.lastdirection.y = self.direction.y

        if self.direction.y == 0:
            self.ismoving = False

        lastposition = self.position

        if keys[K_RIGHT]:
            self.position = self.position.move(self.speed+self.upspeed, 0)
            self.direction.x = 1
            self.ismoving = True
        if keys[K_LEFT]:
            self.position = self.position.move(-(self.speed+self.upspeed), 0)
            self.direction.x = -1
            self.ismoving = True
        if keys[K_UP]:
            self.direction.y = 1
            self.ismoving = True
        if keys[K_LSHIFT]:
            self.upspeed = 1
        else:
            self.upspeed = 0

        # ON DESCEND  =  (self.speedy + self.gravity)
        if self.direction.y == 0 and keys[K_SPACE] and not self.lastkeys[K_SPACE]:
            if keys[K_DOWN]:
                self.position.bottom += self.gravity
                self.lastupdatejump = ticks
                self.ismoving = True
                print "DOWN"
                return
            else:
                self.jump(-10, ticks)
                level.playsound('mariojump')

        self.lastkeys = keys

        self.updateframe(level)
        res = self.checkcollision(level, ticks)
        if res is Message.TERMINATELEVEL:
        # sortie du niveau
            return res

        collide = self.ckeckblockscollision(level)
        if collide is True:
            if self.speedy < 0:
                # on saute, on va essayer de 'glisser' contre la paroie bloquante
                self.position.x = lastposition.x
                collide = self.ckeckblockscollision(level)

        if collide is True:
            self.position = lastposition
            self.speedy = 0

        if self.position.bottom >= len(level.tilemap)*16:
            # you shall die, mortal !
            self.life -= 1
            level.reset()
        self.apply_physics(level, ticks)

    def updateframe(self, level):
        if self.ismoving is False:
            if self.direction.x > 0:
                self.frame = 5
            else:
                self.frame = 4
            return

        ticks = pygame.time.get_ticks()
        rate = 200 / self.speed
        if (self.lastdirection.x != self.direction.x) or (ticks - self.lastupdateframe > rate):
            self.lastupdateframe = ticks
            if self.direction.iszero():
                self.frame = 5
            elif self.direction.y > 0:
                if self.direction.x > 0:
                    self.frame = 9
                else:
                    self.frame = 0
            else:
                if self.direction.x > 0:
                    self.frame += 1
                    if self.frame > 8:
                        self.frame = 5
                if self.direction.x < 0:
                    self.frame -= 1
                    if self.frame < 1:
                        self.frame = 3

    def checkcollision(self, level, ticks):
        for bonus in reversed(level.bonuses):
            if self.position.colliderect(bonus.position):
                res = bonus.action(level)
                if res == Message.TERMINATELEVEL:
                    return res

        jvalue = -10
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            jvalue = -12

        nbkills = 0

        for ennemy in level.ennemies:
            if self.position.right > ennemy.position.left and self.position.left < ennemy.position.right:
                rectcol = pygame.Rect(ennemy.position)
                rectcol.top += 8
                rectcol.height -= 8

                if (self.speedy + self.gravity) > 0 and abs(rectcol.top - self.position.bottom) <= self.gravity:
                    # on descend et est au dessus
                    print "Die ! "
                    nbkills += 1
                    ennemy.action(level)
                elif self.ishurt is False and self.position.colliderect(rectcol):
                    print "Ouch !"
                    level.playsound('cough')
                    if self.isbig:
                        self.setBig(False)
                    else:
                        self.energy -= 1
                    self.ishurt = True
                    self.lasthurttime = ticks
                    if self.energy <= 0:
                        level.reset()
                    break
        if nbkills > 0:
            self.jump(jvalue, ticks)
        return True

    def setBig(self, big=True):
        if big is True:
            self.position.top -= 10
            self.position.height = 31
            self.blity = 22
        else:
            self.position.top += 10
            self.position.height = 22
            self.blity = 0

        self.surface = pygame.Surface((self.position.width, self.position.height))
        self.surface.set_colorkey(Color(255, 0, 255, 255), RLEACCEL)
        self.isbig = big

    def draw(self, level):
        if self.ishurt is True:
            if self.bdraw:
                Character.draw(self, level)
            self.bdraw = not self.bdraw
        else:
            Character.draw(self, level)


